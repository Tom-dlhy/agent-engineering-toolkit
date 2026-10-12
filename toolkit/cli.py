"""Small model-free CLI for skill discovery, recommendations and profile listing."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from toolkit.catalog import ROOT, load_catalog, load_profile, discover, workflow_advice
from toolkit.knowledge import indexed_references, read_reference


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skillctl", description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Toolkit root")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List catalog entries with concise descriptions")
    profiles = commands.add_parser("profiles", help="Show available profiles and their sizes")
    query = commands.add_parser("search", help="Rank likely skills without loading skill bodies")
    query.add_argument("query", help="User task or keywords")
    query.add_argument("--profile", help="Restrict candidates to installed profile")
    query.add_argument("--limit", type=int, default=3)
    query.add_argument("--json", action="store_true", help="Machine-readable results")
    query.add_argument("--explain", action="store_true", help="Include exclusions, uncertainty and checks")
    recommend = commands.add_parser("recommend", help="Advisory workflow level + up to 3 skill names")
    recommend.add_argument("query")
    recommend.add_argument("--profile")
    recommend.add_argument("--limit", type=int, default=3)
    recommend.add_argument("--json", action="store_true", help="Machine-readable recommendation")
    recommend.add_argument("--explain", action="store_true", help="Include exclusions, uncertainty and checks")
    show = commands.add_parser("show", help="Read one selected skill, without scanning other bodies")
    show.add_argument("name")
    refs = commands.add_parser("references", help="List declared leaf paths for a single skill (no leaf bodies)")
    refs.add_argument("name")
    read = commands.add_parser("read-ref", help="Read one allowlisted reference for an activated skill")
    read.add_argument("name")
    read.add_argument("path")
    args = parser.parse_args(argv)
    try:
        catalog = load_catalog(args.root)
        if args.command == "list":
            for skill in catalog.values():
                print(f"{skill.name:36} {skill.domain:14} {skill.description}")
        elif args.command == "profiles":
            for path in sorted((args.root / "profiles").glob("*.yaml")):
                print(f"{path.stem:20} {len(load_profile(path.stem, args.root))} skills")
        elif args.command in ("search", "recommend"):
            allowed = load_profile(args.profile, args.root) if args.profile else None
            discovery = discover(args.query, catalog, allowed=allowed, limit=args.limit)
            advice = workflow_advice(args.query)
            rows = [
                {"name": m.skill.name, "domain": m.skill.domain,
                 "path": m.skill.path + "/SKILL.md", "score": m.score,
                 "reason": "; ".join(m.reasons)}
                for m in discovery.candidates
            ]
            if args.json:
                # Preserve the established search --json list; expanded shape is
                # explicitly opt-in. recommend --json is a new interface.
                if args.explain or args.command == "recommend":
                    for row, match in zip(rows, discovery.candidates):
                        row.update(favorable=list(match.reasons), unfavorable=list(match.unfavorable))
                    report = {"candidates": rows,
                              "excluded": [{"name": e.skill.name, "reasons": list(e.reasons)} for e in discovery.excluded],
                              "uncertainty": discovery.uncertainty,
                              "required_checks": list(discovery.required_checks)}
                    if args.command == "recommend":
                        report["workflow"] = asdict(advice)
                    print(json.dumps(report, ensure_ascii=False, indent=2))
                else:
                    print(json.dumps(rows, ensure_ascii=False, indent=2))
            else:
                if args.command == "recommend":
                    print(f"Suggested workflow: {advice.workflow} ({'; '.join(advice.rationale)}; risk: {advice.risk})")
                    print("Advisory only: verify complexity, permissions and user intent.")
                for match in discovery.candidates:
                    print(f"{match.skill.name}: {match.skill.path}/SKILL.md | score={match.score} | {', '.join(match.reasons)}")
                    if match.unfavorable:
                        print("  Check: " + "; ".join(match.unfavorable))
                if not discovery.candidates:
                    print("No confident lexical match; ask for context or choose manually; zero skills is valid.")
                if args.explain:
                    print("Uncertainty: " + discovery.uncertainty)
                    for exclusion in discovery.excluded:
                        print("Excluded " + exclusion.skill.name + ": " + "; ".join(exclusion.reasons))
                    for check in discovery.required_checks + (advice.required_checks if args.command == "recommend" else ()):
                        print("Required check: " + check)
        elif args.command in ("references", "read-ref"):
            if args.name not in catalog:
                raise ValueError("unknown skill: " + args.name)
            if args.command == "references":
                for path in indexed_references(catalog[args.name], args.root):
                    print(path)
            else:
                print(read_reference(catalog[args.name], args.path, args.root))
        elif args.command == "show":
            if args.name not in catalog:
                raise ValueError("unknown skill: " + args.name)
            print((args.root / catalog[args.name].path / "SKILL.md").read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
