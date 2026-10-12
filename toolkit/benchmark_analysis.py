"""Three-arm A/B/C engineering benchmark analysis.

Unverified run data are *claims* until host transcripts, changed artifacts,
reviewers and tests have been independently inspected. Never auto-merge.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any
from .benchmark_model import VARIANTS, BenchmarkError


def analyze(records: list[dict[str, Any]], *, min_trials: int = 2,
            min_success_delta: float = 0.0, max_token_increase_pct: float | None = None) -> dict:
    if not isinstance(records, list) or not records:
        raise BenchmarkError("benchmark records must be a nonempty list")
    if type(min_trials) is not int or not 1 <= min_trials <= 20:
        raise BenchmarkError("min_trials must be 1..20")
    if not isinstance(min_success_delta, (int, float)) or not 0 <= min_success_delta <= 1:
        raise BenchmarkError("min_success_delta must be 0..1")
    if max_token_increase_pct is not None and (not isinstance(max_token_increase_pct, (int, float))
                                               or max_token_increase_pct < 0):
        raise BenchmarkError("max_token_increase_pct must be nonnegative")
    runs: dict[tuple[str, int, str], dict] = {}
    group: dict[tuple[str, int], dict] = defaultdict(dict)
    required = ("task_id", "trial", "variant", "fixture_sha256", "suite_sha256",
                "model", "host", "tool_config", "run_id", "test_status", "agent_status",
                "tokens", "human_review", "critical_violation")
    for r in records:
        if not isinstance(r, dict) or any(k not in r for k in required):
            raise BenchmarkError("missing required fields in run record")
        if not isinstance(r["task_id"], str) or not r["task_id"] or (
            type(r["trial"]) is not int or r["trial"] < 0 or r["trial"] >= 20
        ) or r["variant"] not in VARIANTS:
            raise BenchmarkError("invalid task/trial/variant")
        for s in ("fixture_sha256", "suite_sha256", "model", "host", "tool_config", "run_id"):
            if not isinstance(r[s], str) or not r[s]:
                raise BenchmarkError(f"missing run provenance {s}")
        if r["test_status"] not in ("PASS", "FAIL", "NOT_RUN", "BLOCKED") or (
            r["agent_status"] not in ("PASS", "FAIL", "NOT_RUN", "BLOCKED")
        ):
            raise BenchmarkError("invalid execution status")
        if r["human_review"] not in ("PASS", "FAIL", "NOT_REVIEWED"):
            raise BenchmarkError("invalid manual review outcome")
        if r["critical_violation"] is not None and type(r["critical_violation"]) is not bool:
            raise BenchmarkError("critical_violation must be boolean or null (unknown)")
        if r["tokens"] is not None and (type(r["tokens"]) is not int or r["tokens"] < 0):
            raise BenchmarkError("tokens must be observed nonnegative integer or null")
        key = (r["task_id"], r["trial"], r["variant"])
        if key in runs:
            raise BenchmarkError(f"duplicate run {key}")
        runs[key] = r
        group[key[:2]][key[-1]] = r
    if not group:
        raise BenchmarkError("no trials")
    for key, trio in group.items():
        if set(trio) != set(VARIANTS):
            raise BenchmarkError(f"incomplete A/B/C trial {key}")
        for field in ("fixture_sha256", "suite_sha256", "model", "host", "tool_config"):
            if len({v[field] for v in trio.values()}) != 1:
                raise BenchmarkError(f"incomparable trial {key}: {field}")
        if len({v["run_id"] for v in trio.values()}) != 3:
            raise BenchmarkError(f"reused run ID {key}")
    counts = {v: {"passes": 0, "failures": 0, "not_run": 0, "total_tokens": None,
                  "reviewed": 0} for v in VARIANTS}
    deltas = {}
    for v in VARIANTS:
        sample = [trio[v] for trio in group.values()]
        counts[v]["passes"] = sum(x["test_status"] == "PASS" and x["agent_status"] == "PASS"
                                  and x["human_review"] != "FAIL" for x in sample)
        counts[v]["failures"] = sum(x["test_status"] == "FAIL" or x["agent_status"] == "FAIL"
                                    or x["human_review"] == "FAIL" for x in sample)
        counts[v]["not_run"] = len(sample) - counts[v]["passes"] - counts[v]["failures"]
        counts[v]["reviewed"] = sum(x["human_review"] != "NOT_REVIEWED" for x in sample)
        counts[v]["total_tokens"] = (sum(x["tokens"] for x in sample)
                                      if all(x["tokens"] is not None for x in sample) else None)
    n = len(group)
    new_critical = sum(
        trio["full"]["critical_violation"] is True and trio["baseline"]["critical_violation"] is False
        for trio in group.values()
    )
    known_critical = any(r["critical_violation"] is True for r in records)
    unknown_critical = any(r["critical_violation"] is None for r in records)
    full_reviewed = all(r["human_review"] in ("PASS", "FAIL") for r in records)
    complete_tests = all(r["agent_status"] in ("PASS", "FAIL")
                         and r["test_status"] in ("PASS", "FAIL") for r in records)
    per_task = {k: sum(1 for task_id, _ in group if task_id == k)
                for k in sorted({task_id for task_id, _ in group})}
    enough = all(k >= min_trials for k in per_task.values())
    complete_tokens = all(counts[v]["total_tokens"] is not None for v in VARIANTS)
    token_pct = None
    if complete_tokens and counts["baseline"]["total_tokens"] > 0:
        token_pct = round(100 * (counts["full"]["total_tokens"] /
                                 counts["baseline"]["total_tokens"] - 1), 2)
    baseline_rate = counts["baseline"]["passes"] / n
    full_rate = counts["full"]["passes"] / n
    uplift = round(full_rate - baseline_rate, 4)
    if known_critical:
        recommendation = "NO_GO_CRITICAL_FINDING"
    elif not enough or not complete_tests or unknown_critical or not full_reviewed:
        recommendation = "INSUFFICIENT_EVIDENCE"
    elif uplift < min_success_delta:
        recommendation = "NO_GO_QUALITY_THRESHOLD"
    elif max_token_increase_pct is not None and (token_pct is None or token_pct > max_token_increase_pct):
        recommendation = "NO_GO_COST_THRESHOLD_OR_UNMEASURED"
    else:
        recommendation = "CANDIDATE_FOR_HUMAN_APPROVAL"
    return {
        "evidence": "externally reported results, integrity and impartial grading must be verified",
        "promotion": recommendation,
        "never_auto_promote": True,
        "n_trials": n,
        "per_task_trials": per_task,
        "arms": counts,
        "quality_uplift_full_vs_baseline": uplift,
        "new_critical_regressions_full_vs_baseline": new_critical,
        "token_change_pct_full_vs_baseline": token_pct,
        "all_token_usage_observed": complete_tokens,
        "human_reviews_complete": full_reviewed,
        "critical_violations_classified": not unknown_critical,
        "execution_checks_complete": complete_tests,
        "thresholds": {"min_trials": min_trials, "min_success_delta": min_success_delta,
                       "max_token_increase_pct": max_token_increase_pct},
    }
