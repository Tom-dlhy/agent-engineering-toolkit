"""Small model-free CLI for skill discovery, recommendations and profile listing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from toolkit.catalog import ROOT, load_catalog, load_profile, search, suggest_workflow, tokenize
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
    recommend = commands.add_parser("recommend", help="Advisory workflow level + up to 3 skill names")
    recommend.add_argument("query")
    recommend.add_argument("--profile")
    recommend.add_argument("--limit", type=int, default=3)
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
            results = search(args.query, catalog, allowed=allowed, limit=args.limit)
            if args.command == "recommend":
                mode, reason = suggest_workflow(args.query)
                print(f"Suggested workflow: {mode} ({reason})")
                print("Advisory only: verify complexity, permissions and user intent.")
            if getattr(args, "json", False):
                print(json.dumps([
                    {"name": m.skill.name, "domain": m.skill.domain,
                     "path": m.skill.path + "/SKILL.md", "score": m.score,
                     "reason": "; ".join(m.reasons)}
                    for m in results
                ], ensure_ascii=False, indent=2))
            else:
                for match in results:
                    print(f"{match.skill.name}: {match.skill.path}/SKILL.md | score={match.score} | {', '.join(match.reasons)}")
                if not results:
                    print("No confident lexical match; ask for context or choose manually.")
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
