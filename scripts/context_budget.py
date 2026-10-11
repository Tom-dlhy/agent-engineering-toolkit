"""Approximate metadata and selective-activation context footprint.

These are deliberately rough characters/4 estimates, NOT model token counts,
billing data, context windows or quota measurements.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from toolkit.catalog import ROOT, load_catalog, load_profile


def estimate(
    profile: str, root: Path = ROOT, activated: tuple[str, ...] = (),
) -> tuple[int, int]:
    catalog = load_catalog(root)
    names = load_profile(profile, root)
    metadata = (root / "AGENTS.md").read_text(encoding="utf-8")
    for name in names:
        skill = catalog[name]
        metadata += "\n" + skill.metadata()
    for name in activated:
        if name not in names:
            raise ValueError(f"skill {name!r} is not installed in profile {profile!r}")
        metadata += (root / catalog[name].path / "SKILL.md").read_text(encoding="utf-8")
    return (len(metadata) + 3) // 4, len(names)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="minimal")
    parser.add_argument("--all", action="store_true", help="Audit all installation profiles")
    parser.add_argument("--activated", action="append", default=[], help="Include the full body of an activated skill")
    parser.add_argument("--budget", type=int, default=None, help="Upper limit on approximate context estimate")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.all and args.activated:
        parser.error("--activated cannot be combined with --all")
    profiles = [p.stem for p in sorted((ROOT / "profiles").glob("*.yaml"))] if args.all else [args.profile]
    try:
        rows = []
        for name in profiles:
            approx, count = estimate(name, ROOT, tuple(args.activated))
            rows.append({"profile": name, "installed_skills": count, "estimated_tokens": approx})
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            print(f"{row['profile']}: {row['installed_skills']} installed skills, ~{row['estimated_tokens']} tokens")
        print("Proxy only: chars/4; excludes real tokenizer, tools, caching and additional reference files.")
    if args.budget is not None and any(row["estimated_tokens"] > args.budget for row in rows):
        print(f"FAIL: at least one profile exceeds approximate budget of {args.budget}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
