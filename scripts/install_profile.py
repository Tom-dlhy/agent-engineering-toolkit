"""Safely copy first-party skills into an EXISTING project; dry-run by default."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = {"codex": ".agents/skills", "claude": ".claude/skills", "generic": ".agents/skills"}


def planned_sources(profile: str, root: Path = ROOT) -> list[Path]:
    if not profile or not all(c.islower() or c.isdigit() or c == "-" for c in profile):
        raise ValueError("invalid profile name")
    path = root / "profiles" / f"{profile}.yaml"
    if not path.is_file():
        raise ValueError(f"unknown profile: {profile}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    catalog = yaml.safe_load((root / "registry" / "skills.yaml").read_text(encoding="utf-8"))
    sources = {item["name"]: root / item["path"] for item in catalog["skills"]}
    return [sources[name] for name in data["skills"]]


def _reject_symlinks(root: Path) -> None:
    if root.is_symlink() or any(item.is_symlink() for item in root.rglob("*")):
        raise ValueError(f"skill includes a symlink; manual audit required: {root}")


def install(profile: str, agent: str, project: Path, apply: bool = False, root: Path = ROOT) -> list[Path]:
    if agent not in AGENTS:
        raise ValueError(f"unsupported agent: {agent}")
    if not project.expanduser().is_dir():
        raise ValueError(f"target project must be an existing directory: {project}")
    project_root = project.expanduser().resolve()
    target = project_root / AGENTS[agent]
    if any(p.is_symlink() for p in (target, target.parent)):
        raise ValueError(f"installation destination uses a symlink: {target}")
    sources = planned_sources(profile, root)
    if not sources or any(not (p / "SKILL.md").is_file() for p in sources):
        raise ValueError("profile contains missing or invalid skills")
    for source in sources:
        _reject_symlinks(source)
    destinations = [target / source.name for source in sources]
    existing = [p for p in destinations if p.exists() or p.is_symlink()]
    if existing:
        raise FileExistsError("refusing to overwrite existing skills: " + ", ".join(map(str, existing)))
    if apply:
        target.mkdir(parents=True, exist_ok=True)
        created = []
        try:
            for source, destination in zip(sources, destinations):
                shutil.copytree(source, destination, symlinks=False)
                created.append(destination)
        except (OSError, shutil.Error):
            for destination in reversed(created):
                shutil.rmtree(destination)
            raise
    return destinations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--agent", choices=sorted(AGENTS), required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Copy files (default: preview only)")
    args = parser.parse_args()
    try:
        destinations = install(args.profile, args.agent, args.project, args.apply)
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
