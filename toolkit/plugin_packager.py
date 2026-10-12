"""Build verifiable, selective Codex/Claude native plugin marketplaces offline.

A distribution is self-contained, immutable by convention, and never executes
the scripts shipped with individual skills.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

from toolkit.managed_installer import (
    ROOT, InstallError, _digest, _files, _requested, _safe_relative, _source,
)

PLUGIN = "agent-engineering-toolkit"
PACKAGE_SCHEMA = "aet.plugin.v1"
VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _inventory(root: Path) -> dict[str, str]:
    result = {}
    for item in sorted(root.rglob("*")):
        if item.is_symlink():
            raise InstallError(f"plugin contains symlink: {item}")
        if item.is_file():
            result[_safe_relative(item.relative_to(root).as_posix())] = _digest(item.read_bytes())
        elif not item.is_dir():
            raise InstallError(f"plugin contains non-regular entry: {item}")
    return result


def build(root: Path, output: Path, profile: str | None = None,
          skills: tuple[str, ...] = (), version: str | None = None) -> dict:
    """Create a fresh marketplace tree. Refuse any pre-existing output."""
    source = root.resolve(strict=True)
    available, revision = _source(source)
    selected = _requested(source, profile, skills)
    if not selected:
        raise InstallError("plugin package requires --profile or --skill")
    unknown = set(selected) - set(available)
    if unknown:
        raise InstallError("unknown skills: " + ", ".join(sorted(unknown)))
    version = version or ("0.0.0-g" + revision[:12] if revision != "snapshot" else "0.0.0-dev")
    if not VERSION.fullmatch(version):
        raise InstallError(f"not a SemVer version: {version}")
    if output.exists() or output.is_symlink():
        raise InstallError(f"output exists; refusing overwrite: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        plugin = output / "plugins" / PLUGIN
        skills_dir = plugin / "skills"
        skills_dir.mkdir(parents=True)
        for name in selected:
            source_files = _files(available[name])
            target = skills_dir / name
            target.mkdir()
            for rel, expected_sha in source_files.items():
                data = (available[name] / rel).read_bytes()
                if _digest(data) != expected_sha:
                    raise InstallError("source changed during packaging: " + name)
                path = target / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        desc = "Curated vendor-neutral agent engineering skills (no automatic hooks)."
        _write(plugin / "plugin.json", {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": PLUGIN, "version": version, "description": desc,
            "repository": "https://github.com/Tom-dlhy/agent-engineering-toolkit",
            "license": "MIT",
        })
        _write(plugin / ".codex-plugin" / "plugin.json", {
            "name": PLUGIN, "version": version, "description": desc,
            "skills": "./skills/",
        })
        _write(plugin / ".claude-plugin" / "plugin.json", {
            "name": PLUGIN, "version": version, "description": desc,
            "author": {"name": "Agent Engineering Toolkit"},
        })
        _write(output / ".agents/plugins/marketplace.json", {
            "name": "aet-local", "interface": {"displayName": "Agent Engineering Toolkit"},
            "plugins": [{"name": PLUGIN, "source": {
                "source": "local", "path": "./plugins/" + PLUGIN},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Developer Tools"}],
        })
        _write(output / ".claude-plugin/marketplace.json", {
            "name": "aet-local", "owner": {"name": "Agent Engineering Toolkit"},
            "plugins": [{"name": PLUGIN, "source": "./plugins/" + PLUGIN,
                         "description": desc, "version": version}],
        })
        (output / "README.md").write_text(
            "# Agent Engineering Toolkit — native distribution\n\n"
            "This directory is generated. Do not edit skill files in place.\n\n"
            "Claude Code: register the directory containing .claude-plugin/marketplace.json\n"
            "with 'claude plugin marketplace add /absolute/path/to/this-directory',\n"
            "then 'claude plugin install agent-engineering-toolkit@aet-local'.\n\n"
            "Codex: 'codex plugin marketplace add /absolute/path/to/this-directory';\n"
            "install via the host's plugin directory or configured marketplace.\n\n"
            "These native plugins are managed by the host, not by the AET copy installer.\n"
            "Do not install the same skills by both mechanisms in one agent scope.\n"
            "The manifests contain no hooks or MCP servers. Bundled skill scripts\n"
            "are data until a user explicitly authorizes their execution.\n",
            encoding="utf-8",
        )
        ledger = {"schema": PACKAGE_SCHEMA, "version": version, "revision": revision,
                  "selected": selected, "files": _inventory(output)}
        _write(output / "aet-distribution.json", ledger)
        return {"path": str(output), "version": version, "revision": revision,
                "skills": selected, "files": len(ledger["files"])}
    except BaseException:
        if output.exists():
            shutil.rmtree(output)
        raise


def verify(output: Path) -> dict:
    if output.is_symlink() or not output.is_dir():
        raise InstallError("distribution root must be a regular directory")
    file_path = output / "aet-distribution.json"
    if file_path.is_symlink() or not file_path.is_file():
        raise InstallError("missing distribution manifest")
    try:
        state = json.loads(file_path.read_text(encoding="utf-8"))
        if state["schema"] != PACKAGE_SCHEMA or not VERSION.fullmatch(state["version"]):
            raise InstallError("invalid distribution schema/version")
        files = state["files"]
        if not isinstance(files, dict) or not files:
            raise InstallError("invalid distribution inventory")
        for rel, sha in files.items():
            _safe_relative(rel)
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
                raise InstallError("invalid package SHA")
        current = _inventory(output)
        current.pop("aet-distribution.json", None)
        if files != current:
            raise InstallError("distribution drift: extra, missing or edited file")
        plugin = output / "plugins" / PLUGIN
        for manifest in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            parsed = json.loads((plugin / manifest).read_text(encoding="utf-8"))
            if parsed["name"] != PLUGIN or parsed["version"] != state["version"]:
                raise InstallError("plugin manifest mismatch")
        if any((plugin / "skills" / name / "SKILL.md").is_file() is False
               for name in state["selected"]):
            raise InstallError("packaged skill missing SKILL.md")
        return {"valid": True, "version": state["version"],
                "skills": len(state["selected"]), "files": len(files)}
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise InstallError(f"invalid distribution: {exc}") from exc


def archive(output: Path, zip_path: Path) -> None:
    verify(output)
    if zip_path.exists():
        raise InstallError("archive already exists")
    with zipfile.ZipFile(zip_path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(output.rglob("*")):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo(output.name + "/" + path.relative_to(output).as_posix())
            info.date_time = (2020, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("build", "verify"))
    p.add_argument("--source", type=Path, default=ROOT)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--profile")
    p.add_argument("--skill", action="append", default=[])
    p.add_argument("--version")
    p.add_argument("--zip", action="store_true")
    p.add_argument("--apply", action="store_true", help="Write the package (otherwise preview)")
    a = p.parse_args(argv)
    try:
        if a.command == "verify":
            result = verify(a.output)
        elif not a.apply:
            available, revision = _source(a.source.resolve(strict=True))
            selected = _requested(a.source, a.profile, tuple(a.skill))
            if not selected or any(n not in available for n in selected):
                raise InstallError("specify existing --profile or --skill")
            result = {"dry_run": True, "output": str(a.output), "skills": selected,
                      "revision": revision}
        else:
            result = build(a.source, a.output, a.profile, tuple(a.skill), a.version)
            if a.zip:
                archive(a.output, a.output.with_suffix(".zip"))
        print(json.dumps(result, indent=2))
        return 0
    except (InstallError, OSError) as exc:
        p.error(str(exc))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
