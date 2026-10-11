"""Estimate startup metadata footprint using characters / four (NOT actual tokens)."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from validate_skills import read_skill

ROOT = Path(__file__).resolve().parents[1]


def estimate(profile: str, root: Path = ROOT) -> tuple[int, int]:
    data = yaml.safe_load((root / "profiles" / f"{profile}.yaml").read_text(encoding="utf-8"))
    catalog = yaml.safe_load((root / "registry" / "skills.yaml").read_text(encoding="utf-8"))
    by_name = {s["name"]: s for s in catalog["skills"]}
    text = (root / "AGENTS.md").read_text(encoding="utf-8")
    for name in data["skills"]:
        item = by_name[name]
        meta, _ = read_skill(root / item["path"] / "SKILL.md")
        text += "\n" + str(meta["name"]) + ": " + str(meta["description"])
    return (len(text) + 3) // 4, len(data["skills"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="minimal")
    parser.add_argument("--budget", type=int)
    args = parser.parse_args()
    try:
        approx, count = estimate(args.profile)
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    print(f"Profile {args.profile}: {count} installed skills")
    print(f"Approximate startup AGENTS.md + metadata: {approx} tokens (characters / 4)")
    print("Excludes loaded skill bodies, prompts, tools, subagents, model-specific tokenization and cache effects.")
    if args.budget is not None and approx > args.budget:
        print(f"Approximate budget exceeded: {approx} > {args.budget}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
