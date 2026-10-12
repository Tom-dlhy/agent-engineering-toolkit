"""Build verifiable, selective Codex/Claude native plugin marketplaces offline.

A distribution is self-contained, immutable by convention, and never executes
the scripts shipped with individual skills.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
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
          skills: tuple[str, ...] = (), version: str | None = None,
          name: str = PLUGIN) -> dict:
    """Create a fresh marketplace tree. Refuse any pre-existing output."""
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", name):
        raise InstallError("invalid plugin name")
    source = root.resolve(strict=True)
    available, revision = _source(source)
    selected = _requested(source, profile, skills)
    if not selected:
        raise InstallError("plugin package requires --profile or --skill")
    unknown = set(selected) - set(available)
    if unknown:
        raise InstallError("unknown skills: " + ", ".join(sorted(unknown)))
    if revision.startswith("dirty-"):
        raise InstallError("source checkout is dirty; commit changes before packaging")
    version = version or ("0.0.0-g" + revision[:12] if revision != "snapshot" else "0.0.0-dev")
    if not VERSION.fullmatch(version):
        raise InstallError(f"not a SemVer version: {version}")
    if output.exists() or output.is_symlink():
        raise InstallError(f"output exists; refusing overwrite: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        plugin = output / "plugins" / name
        skills_dir = plugin / "skills"
        skills_dir.mkdir(parents=True)
        for name_skill in selected:
            source_files = _files(available[name_skill])
            target = skills_dir / name_skill
            target.mkdir()
            for rel, expected_sha in source_files.items():
                data = (available[name_skill] / rel).read_bytes()
                if _digest(data) != expected_sha:
                    raise InstallError("source changed during packaging: " + name_skill)
                path = target / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                if os.name != "nt":
                    source_mode = (available[name_skill] / rel).stat().st_mode
                    path.chmod(0o755 if source_mode & 0o111 else 0o644)
        desc = "Curated vendor-neutral agent engineering skills (no automatic hooks)."
        marketplace = name + "-local"
        _write(plugin / "plugin.json", {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": name, "version": version, "description": desc,
            "repository": "https://github.com/Tom-dlhy/agent-engineering-toolkit",
            "license": "MIT",
        })
        _write(plugin / ".codex-plugin" / "plugin.json", {
            "name": name, "version": version, "description": desc,
            "skills": "./skills/",
        })
        _write(plugin / ".claude-plugin" / "plugin.json", {
            "name": name, "version": version, "description": desc,
            "author": {"name": "Agent Engineering Toolkit"},
        })
        _write(output / ".agents/plugins/marketplace.json", {
            "name": marketplace, "interface": {"displayName": "Agent Engineering Toolkit"},
            "plugins": [{"name": name, "source": {
                "source": "local", "path": "./plugins/" + name},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Developer Tools"}],
        })
        _write(output / ".claude-plugin/marketplace.json", {
            "name": marketplace, "owner": {"name": "Agent Engineering Toolkit"},
            "plugins": [{"name": name, "source": "./plugins/" + name,
                         "description": desc, "version": version}],
        })
        (output / "README.md").write_text(
            "# Agent Engineering Toolkit — native distribution\n\n"
            "This directory is generated. Do not edit skill files in place.\n\n"
            "Claude Code: register the directory containing .claude-plugin/marketplace.json\n"
            "with 'claude plugin marketplace add /absolute/path/to/this-directory',\n"
            "then 'claude plugin install " + name + "@" + marketplace + "'.\n\n"
            "Codex: 'codex plugin marketplace add /absolute/path/to/this-directory';\n"
            "install via the host's plugin directory or configured marketplace.\n\n"
            "These native plugins are managed by the host, not by the AET copy installer.\n"
            "Do not install the same skills by both mechanisms in one agent scope.\n"
            "The manifests contain no hooks or MCP servers. Bundled skill scripts\n"
            "are data until a user explicitly authorizes their execution.\n",
            encoding="utf-8",
        )
        ledger = {"schema": PACKAGE_SCHEMA, "plugin": name, "version": version, "revision": revision,
                  "selected": selected, "files": _inventory(output)}
        _write(output / "aet-distribution.json", ledger)
        return {"path": str(output), "plugin": name, "version": version, "revision": revision,
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
        plugin_name = state.get("plugin", PLUGIN)
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", plugin_name):
            raise InstallError("invalid plugin identity")
        plugin = output / "plugins" / plugin_name
        expected_marketplace = plugin_name + "-local"
        for location in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            marketplace_data = json.loads((output / location).read_text(encoding="utf-8"))
            if marketplace_data.get("name") != expected_marketplace:
                raise InstallError("marketplace identity mismatch")
            entries = marketplace_data.get("plugins")
            if not isinstance(entries, list) or len(entries) != 1 or entries[0].get("name") != plugin_name:
                raise InstallError("marketplace entry mismatch")
            source = entries[0].get("source")
            if location.startswith(".agents"):
                if not isinstance(source, dict) or source.get("path") != "./plugins/" + plugin_name:
                    raise InstallError("Codex plugin source mismatch")
            elif source != "./plugins/" + plugin_name:
                raise InstallError("Claude plugin source mismatch")
        for manifest in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            parsed = json.loads((plugin / manifest).read_text(encoding="utf-8"))
            if parsed["name"] != plugin_name or parsed["version"] != state["version"]:
                raise InstallError("plugin manifest mismatch")
        if any((plugin / "skills" / name / "SKILL.md").is_file() is False
               for name in state["selected"]):
            raise InstallError("packaged skill missing SKILL.md")
        return {"valid": True, "version": state["version"],
                "skills": len(state["selected"]), "files": len(files)}
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise InstallError(f"invalid distribution: {exc}") from exc


def archive(output: Path, zip_path: Path) -> str:
    """Build deterministic ZIP with canonical internal root, preserving modes."""
    verify(output)
    if zip_path.exists() or zip_path.is_symlink():
        raise InstallError("archive already exists")
    temporary = zip_path.with_name(zip_path.name + ".staging")
    if temporary.exists() or temporary.is_symlink():
        raise InstallError("staging archive exists; inspect/remove it manually")
    try:
        with zipfile.ZipFile(temporary, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for path in sorted(output.rglob("*")):
                if not path.is_file():
                    continue
                info = zipfile.ZipInfo("aet-distribution/" + path.relative_to(output).as_posix())
                info.date_time = (2020, 1, 1, 0, 0, 0)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (0o755 if path.stat().st_mode & 0o111 else 0o644) << 16
                z.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        with zipfile.ZipFile(temporary) as z:
            bad = z.testzip()
            if bad:
                raise InstallError("archive CRC verification failed: " + bad)
        if zip_path.exists():
            raise InstallError("archive destination appeared during packaging")
        os.replace(temporary, zip_path)
        return _digest(zip_path.read_bytes())
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("build", "verify"))
    p.add_argument("--source", type=Path, default=ROOT)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--profile")
    p.add_argument("--skill", action="append", default=[])
    p.add_argument("--version")
    p.add_argument("--name", default=PLUGIN, help="Unique slug per curated native variant")
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
            result = build(a.source, a.output, a.profile, tuple(a.skill), a.version, a.name)
            if a.zip:
                result["archive_sha256"] = archive(a.output, a.output.with_suffix(".zip"))
        print(json.dumps(result, indent=2))
        return 0
    except (InstallError, OSError) as exc:
        p.error(str(exc))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
