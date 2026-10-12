"""Validate and summarize externally produced old-skill/candidate observations."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from toolkit.skill_eval_report import EvalInputError, compare_pairs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", required=True, type=Path,
                        help="JSON array of externally observed paired-run records")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.records.read_text(encoding="utf-8"))
        report = compare_pairs(data)
    except (OSError, json.JSONDecodeError, EvalInputError, TypeError) as exc:
        print(f"invalid evaluation records: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
