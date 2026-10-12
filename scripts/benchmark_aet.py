"""Prepare, optionally execute and compare bounded three-arm agent benchmarks.

PLAN is offline and free. RUN requires explicit paid, test-execution and
disposable-host opt-ins. ANALYZE consumes reported evidence without running AI.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toolkit.benchmark_model import BenchmarkError, load_suite, fixture_summary
from toolkit.benchmark_runner import execute, plan
from toolkit.benchmark_analysis import analyze


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("plan", "run", "analyze"))
    p.add_argument("--manifest", type=Path, help="Versioned JSON suite inside toolkit checkout")
    p.add_argument("--host", choices=("codex", "claude"))
    p.add_argument("--model", help="Explicit pinned host model name")
    p.add_argument("--trials", type=int, default=2)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output", type=Path, help="Fresh report directory; never overwrites")
    p.add_argument("--records", type=Path, help="Observed records.json for analysis")
    p.add_argument("--allow-paid-agent-run", action="store_true")
    p.add_argument("--allow-test-execution", action="store_true")
    p.add_argument("--trusted-disposable-host", action="store_true")
    p.add_argument("--max-runs", type=int, default=0,
                   help="Mandatory finite cap when running")
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--max-total-seconds", type=int, default=600)
    p.add_argument("--min-trials", type=int, default=2)
    p.add_argument("--min-success-delta", type=float, default=0)
    p.add_argument("--max-token-increase-pct", type=float)
    args = p.parse_args(argv)
    try:
        if args.command == "analyze":
            if not args.records:
                raise BenchmarkError("analyze needs --records")
            data = json.loads(args.records.read_text(encoding="utf-8"))
            result = analyze(data, min_trials=args.min_trials,
                             min_success_delta=args.min_success_delta,
                             max_token_increase_pct=args.max_token_increase_pct)
        else:
            if not args.manifest or not args.host or not args.model:
                raise BenchmarkError("plan/run need --manifest --host --model")
            suite = load_suite(args.manifest, ROOT)
            if args.command == "plan":
                result = plan(suite, ROOT, host=args.host, model=args.model,
                              trials=args.trials, seed=args.seed)
                result["tasks"] = fixture_summary(suite)
            else:
                if not args.output:
                    raise BenchmarkError("run requires --output")
                result = execute(
                    suite, ROOT, host=args.host, model=args.model, trials=args.trials,
                    output=args.output, allow_paid=args.allow_paid_agent_run,
                    allow_tests=args.allow_test_execution,
                    trusted_host=args.trusted_disposable_host,
                    max_runs=args.max_runs, timeout=args.timeout,
                    max_total_seconds=args.max_total_seconds, seed=args.seed)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (BenchmarkError, OSError, ValueError) as exc:
        print("benchmark error:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
