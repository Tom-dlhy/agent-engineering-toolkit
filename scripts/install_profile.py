"""Safely copy first-party skills into a project; dry-run by default."""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = {"codex": ".agents/skills", "claude": ".claude/skills", "generic": ".agents/skills"}
SAFE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def planned_sources(profile: str | None, root: Path = ROOT, skills: list[str] | None = None) -> list[Path]:
    """Resolve a curated profile and/or explicitly requested skills, without duplicates."""
    if profile is None and not skills:
        raise ValueError("provide --profile and/or --skill")
    catalog = yaml.safe_load((root / "registry" / "skills.yaml").read_text(encoding="utf-8"))
    sources = {item["name"]: root / item["path"] for item in catalog["skills"]}
    selected: list[str] = []
    if profile is not None:
        if not SAFE_NAME.fullmatch(profile):
            raise ValueError(f"invalid profile: {profile}")
        path = root / "profiles" / f"{profile}.yaml"
        if not path.is_file():
            raise ValueError(f"unknown profile: {profile}")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
            raise ValueError(f"invalid profile: {profile}")
        selected.extend(data["skills"])
    selected.extend(skills or [])
    resolved: list[Path] = []
    seen: set[str] = set()
    for name in selected:
        if not isinstance(name, str) or name not in sources:
            raise ValueError(f"unknown skill: {name}")
        if name not in seen:
            resolved.append(sources[name])
            seen.add(name)
    return resolved


def install(
    profile: str | None,
    agent: str,
    project: Path,
    apply: bool = False,
    root: Path = ROOT,
    skills: list[str] | None = None,
) -> list[Path]:
    if agent not in AGENTS:
        raise ValueError(f"unsupported agent: {agent}")
    target = project.expanduser().resolve() / AGENTS[agent]
    sources = planned_sources(profile, root, skills)
    if not sources or any(not (p / "SKILL.md").is_file() for p in sources):
        raise ValueError("selection contains missing or invalid skills")
    destinations = [target / source.name for source in sources]
    existing = [p for p in destinations if p.exists() or p.is_symlink()]
    if existing:
        raise FileExistsError("refusing to overwrite existing skills: " + ", ".join(map(str, existing)))
    if apply:
        target.mkdir(parents=True, exist_ok=True)
        for source, destination in zip(sources, destinations):
            shutil.copytree(source, destination, symlinks=False)
    return destinations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", help="Optional curated profile")
    parser.add_argument("--skill", action="append", default=[], help="Explicit skill name (repeatable)")
    parser.add_argument("--agent", choices=sorted(AGENTS), required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Copy files (default: preview only)")
    args = parser.parse_args()
    if args.profile is None and not args.skill:
        parser.error("provide --profile and/or --skill")
    try:
        destinations = install(args.profile, args.agent, args.project, args.apply, skills=args.skill)
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    print(("Installed" if args.apply else "Would install") + f" {len(destinations)} skills:")
    for path in destinations:
        print(" ", path)
    if not args.apply:
        print("Dry-run only; pass --apply to copy. Existing skills are never overwritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
