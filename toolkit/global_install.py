"""Global, one-skill native gateway backed by the complete AET library.

Creates a temporary *synthetic source* for the existing signed, transactional
ManagedInstaller. This keeps all library guides accessible without exposing
178 native skill descriptions or requiring AET files in target projects.
No scripts or model calls are executed.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import tempfile

import yaml

from toolkit.catalog import load_catalog
from toolkit.managed_installer import (
    ROOT, InstallError, ManagedInstaller, _digest, _files, _safe_name, _source,
)

GATEWAY = "aet"
AGENTS = ("codex", "claude")
TEMPLATE = "templates/aet-global/SKILL.md"


def build_source(root: Path, destination: Path) -> dict:
    """Create one native AET skill with a browsable, on-demand library.

    The 178 underlying SKILL.md files are stored as GUIDE.md in nested
    directories so only the gateway has a native SKILL.md.
    """
    root = root.resolve(strict=True)
    available, revision = _source(root)
    catalog = load_catalog(root)
    if set(catalog) != set(available):
        raise InstallError("catalog and installable skill inventory disagree")
    gateway = destination / "skills/core/aet"
    gateway.mkdir(parents=True)
    template = root / TEMPLATE
    if template.is_symlink() or not template.is_file():
        raise InstallError("missing or unsafe AET gateway template")
    gateway.joinpath("SKILL.md").write_bytes(template.read_bytes())

    by_domain: dict[str, list] = defaultdict(list)
    for skill in catalog.values():
        domain, name = _safe_name(skill.domain), _safe_name(skill.name)
        by_domain[domain].append(skill)
        origin = available[name]
        inventory = _files(origin)
        target = gateway / "library" / domain / name
        for rel, sha in inventory.items():
            path = Path(rel)
            if path.name == "SKILL.md" and rel != "SKILL.md":
                raise InstallError("nested SKILL.md in specialist: " + name)
            copied = target / ("GUIDE.md" if rel == "SKILL.md" else rel)
            data = (origin / rel).read_bytes()
            if _digest(data) != sha:
                raise InstallError("source changed during bundle creation: " + name)
            copied.parent.mkdir(parents=True, exist_ok=True)
            copied.write_bytes(data)
            if (origin / rel).stat().st_mode & 0o111:
                copied.chmod(0o755)

    index = ["# AET domain index", "",
             "Open only the domains that match the task. Each domain index",
             "contains skill triggers and links to on-demand guides.", ""]
    for domain, skills in sorted(by_domain.items()):
        index.append(f"- [{domain}]({domain}.md) — {len(skills)} specialist guides")
        lines = [f"# {domain} — AET specialist index", "",
                 "Descriptions are taken from the skills' existing frontmatter.",
                 "Use the user's task and project context; check exclusions.",
                 "Read only selected guides, then specific local references.", ""]
        for skill in sorted(skills, key=lambda item: item.name):
            description = " ".join(skill.description.split())
            lines.append(
                f"- **[{skill.name}](../library/{domain}/{skill.name}/GUIDE.md)**"
                f" — {description}"
            )
        page = gateway / "index" / (domain + ".md")
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (gateway / "index/INDEX.md").write_text(
        "\n".join(index) + "\n", encoding="utf-8"
    )
    (gateway / "index/SOURCE.json").write_text(
        json.dumps({"schema": "aet.global-index.v1", "source_revision": revision,
                    "specialist_count": len(catalog), "domains": len(by_domain)},
                   sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    registry = destination / "registry/skills.yaml"
    registry.parent.mkdir(parents=True)
    registry.write_text(yaml.safe_dump({
        "version": 1, "skills": [{
            "name": GATEWAY, "domain": "core", "path": "skills/core/aet",
            "keywords": ["aet"],
        }],
    }, sort_keys=False), encoding="utf-8")
    return {"specialists": len(catalog), "domains": len(by_domain),
            "source_revision": revision}


def run(command: str, agents: tuple[str, ...], *, source: Path = ROOT,
        home: Path | None = None, apply: bool = False) -> tuple[dict, int]:
    """Plan all hosts before writing any. Updates/uninstalls respect ownership."""
    if any(agent not in AGENTS for agent in agents) or not agents:
        raise InstallError("unknown agent")
    if command not in ("plan", "install", "update", "doctor", "uninstall"):
        raise InstallError("unknown command")
    with tempfile.TemporaryDirectory(prefix="aet-global-") as temp:
        metadata = None
        origin = source
        if command in ("plan", "install", "update"):
            origin = Path(temp)
            metadata = build_source(source, origin)
        managers = {agent: ManagedInstaller(origin, agent, "user", home=home)
                    for agent in agents}
        if command == "doctor":
            result = {agent: manager.inspect() for agent, manager in managers.items()}
            for data in result.values():
                data["gateway_installed"] = data["installed"].get(GATEWAY) == "clean"
            code = 0 if all(x["gateway_installed"] and not x["pending_recovery"]
                            for x in result.values()) else 2
            return {"agents": result, "applied": False}, code

        operation = "install" if command == "plan" else command
        plans = {}
        for agent, manager in managers.items():
            if operation != "uninstall":
                previous = manager._state()["selected"]
                if any(skill != GATEWAY for skill in previous):
                    raise InstallError(
                        f"{agent}: existing user-scope managed skills {previous}; "
                        "migrate explicitly with the existing manage_install.py "
                        "uninstall --scope user --agent <agent> --apply; "
                        "this command does not remove them automatically"
                    )
            plan = manager.plan(operation, skills=(GATEWAY,))
            conflicts = [op for op in plan["operations"]
                         if op["action"].startswith("conflict")]
            if conflicts:
                raise InstallError(
                    f"{agent}: existing files require review; no changes made: "
                    + json.dumps(conflicts)
                )
            plans[agent] = plan

        if apply and command != "plan":
            for agent, manager in managers.items():
                manager.apply(operation, skills=(GATEWAY,))
        result = {
            "command": command, "applied": bool(apply and command != "plan"),
            "gateway": GATEWAY, "bundle": metadata,
            "agents": {
                agent: {
                    "native_skill_path": str(manager.target / GATEWAY),
                    "operations": [
                        {"skill": op["skill"], "action": op["action"]}
                        for op in plans[agent]["operations"]
                    ],
                }
                for agent, manager in managers.items()
            },
        }
        return result, 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install one native AET gateway globally, with full on-demand library."
    )
    parser.add_argument("command", choices=("plan", "install", "update", "doctor", "uninstall"))
    parser.add_argument("--agent", choices=(*AGENTS, "both"), default="both")
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--apply", action="store_true", help="Required to modify files")
    args = parser.parse_args(argv)
    agents = AGENTS if args.agent == "both" else (args.agent,)
    try:
        result, code = run(args.command, agents, source=args.source,
                           apply=args.apply)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return code
    except (OSError, InstallError, ValueError, yaml.YAMLError) as error:
        parser.error(str(error))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
