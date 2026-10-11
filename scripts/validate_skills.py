"""Validate local Agent Skills, catalog and installation profiles."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL)


def load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def read_skill(path: Path) -> tuple[dict, str]:
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(content)
    if not match:
        raise ValueError("missing frontmatter")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return metadata, content[match.end():]


def validate_repository(root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    catalog_path = root / "registry" / "skills.yaml"
    try:
        catalog = load_yaml(catalog_path)
    except (OSError, yaml.YAMLError) as exc:
        return [f"{catalog_path}: {exc}"]
    if not isinstance(catalog, dict) or catalog.get("version") != 1:
        return ["registry/skills.yaml: invalid version"]
    entries = catalog.get("skills")
    if not isinstance(entries, list):
        return ["registry/skills.yaml: skills must be a list"]

    names: set[str] = set()
    declared_paths: set[str] = set()
    for item in entries:
        if not isinstance(item, dict):
            problems.append("registry: invalid skill entry")
            continue
        name, domain, relpath = (item.get(key) for key in ("name", "domain", "path"))
        if not all(isinstance(value, str) for value in (name, domain, relpath)):
            problems.append(f"registry: malformed skill entry {item!r}")
            continue
        if not SKILL_NAME.fullmatch(name) or not SKILL_NAME.fullmatch(domain):
            problems.append(f"registry: invalid skill name or domain: {name}")
        if name in names:
            problems.append(f"registry: duplicate skill name: {name}")
        names.add(name)
        expected = f"skills/{domain}/{name}"
        if relpath != expected:
            problems.append(f"registry: invalid skill path: {relpath}")
        declared_paths.add(relpath)
        path = root / relpath / "SKILL.md"
        if not path.is_file():
            problems.append(f"{relpath}: missing SKILL.md")
            continue
        try:
            meta, body = read_skill(path)
        except (ValueError, OSError, yaml.YAMLError) as exc:
            problems.append(f"{relpath}: {exc}")
            continue
        if meta.get("name") != name or meta.get("domain") != domain:
            problems.append(f"{relpath}: name/domain metadata mismatch")
        description = meta.get("description")
        if not isinstance(description, str) or not 35 <= len(description.strip()) <= 750:
            problems.append(f"{relpath}: description must contain 35..750 characters")
        elif "use when" not in description.lower():
            problems.append(f"{relpath}: description must state 'Use when'")
        if len(body.strip()) < 120:
            problems.append(f"{relpath}: skill body is too short")

    skill_dir = root / "skills"
    actual_paths = {
        p.parent.relative_to(root).as_posix()
        for p in skill_dir.rglob("SKILL.md")
    } if skill_dir.exists() else set()
    if not actual_paths:
        problems.append("no skills found")
    for path in sorted(actual_paths - declared_paths):
        problems.append(f"unregistered skill: {path}")
    for path in sorted(declared_paths - actual_paths):
        problems.append(f"registered skill not found: {path}")

    profile_dir = root / "profiles"
    profile_paths = sorted(profile_dir.glob("*.yaml")) if profile_dir.exists() else []
    if not profile_paths:
        problems.append("no profiles found")
    for path in profile_paths:
        try:
            profile = load_yaml(path)
        except (OSError, yaml.YAMLError) as exc:
            problems.append(f"{path.name}: {exc}")
            continue
        if not isinstance(profile, dict) or profile.get("name") != path.stem:
            problems.append(f"{path.name}: profile name mismatch")
            continue
        configured = profile.get("skills")
        if not isinstance(configured, list) or not configured:
            problems.append(f"{path.name}: missing skills")
            continue
        if len(configured) != len(set(map(str, configured))):
            problems.append(f"{path.name}: duplicate skill references")
        for name in configured:
            if name not in names:
                problems.append(f"{path.name}: unknown skill: {name}")
    return problems


def main() -> int:
    errors = validate_repository()
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    skills = len(list((ROOT / "skills").rglob("SKILL.md")))
    profiles = len(list((ROOT / "profiles").glob("*.yaml")))
    print(f"Validated {skills} skills and {profiles} profiles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
