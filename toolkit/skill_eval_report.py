"""Offline aggregation of *reported* paired native-agent evaluations.

No host execution, token estimation, security certification or model calls.
This tool validates record shape and pair comparability only.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any


class EvalInputError(ValueError):
    """Malformed, incomplete or incomparable evaluation evidence."""


def _exact_int(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise EvalInputError(f"{field} must be a nonnegative integer")
    return value


_ACTIVATION_CATEGORIES = ("correct_activation", "correct_non_activation", "missed_activation",
                          "false_activation", "unknown", "not_run")


def _activation(rec: dict[str, Any]) -> str:
    if rec["status"] == "NOT_RUN":
        return "not_run"
    # Legacy positive names remain reported observations, not verified telemetry.
    # Legacy null is unknown: it never proves that no skill was activated.
    observed = rec.get("activation_observed", rec["activated_skill"] is not None)
    if not observed:
        return "unknown"
    expected, actual = rec["expected_skill"], rec["activated_skill"]
    if actual is None:
        return "missed_activation" if expected is not None else "correct_non_activation"
    return "correct_activation" if actual == expected else "false_activation"


def compare_pairs(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Report task outcomes only for comparable baseline/candidate pairs.

    Inputs are EXTERNAL observations and may still be false. The caller
    must independently verify the referenced run IDs, transcripts/tests
    and recorded critical violations before using a GO/NO-GO conclusion.
    """
    if not isinstance(records, list) or not records:
        raise EvalInputError("nonempty list of observations is required")
    by_task: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    required = ("task_id", "variant", "run_id", "input_sha", "host", "model",
                "tool_config", "skill_sha", "status", "expected_skill",
                "critical_violation", "review_calls")
    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            raise EvalInputError(f"record {i} must be an object")
        missing = [key for key in required if key not in rec]
        if missing:
            raise EvalInputError(f"record {i} missing: {', '.join(missing)}")
        if "activated_skill" not in rec and rec.get("activation_observed") is True:
            raise EvalInputError("observed absence requires explicit activated_skill: null")
        # Normalize a copy; never alter the caller's historical records.
        rec = {"activated_skill": None, **rec}
        if not isinstance(rec["task_id"], str) or not rec["task_id"].strip():
            raise EvalInputError("task_id must be a nonempty string")
        if rec["variant"] not in ("baseline", "candidate"):
            raise EvalInputError("variant must be baseline or candidate")
        for key in ("run_id", "input_sha", "host", "model", "tool_config", "skill_sha"):
            if not isinstance(rec[key], str) or not rec[key].strip():
                raise EvalInputError(f"{key} must be a nonempty string")
        if rec["status"] not in ("PASS", "FAIL", "NOT_RUN", "BLOCKED"):
            raise EvalInputError("status must be PASS/FAIL/NOT_RUN/BLOCKED")
        if rec["expected_skill"] is not None and not isinstance(rec["expected_skill"], str):
            raise EvalInputError("expected_skill must be string or null")
        if rec["activated_skill"] is not None and not isinstance(rec["activated_skill"], str):
            raise EvalInputError("activated_skill must be string or null")
        for key in ("expected_skill", "activated_skill"):
            if isinstance(rec[key], str) and not rec[key].strip():
                raise EvalInputError(f"{key} must be nonempty string or null")
        if "activation_observed" in rec and type(rec["activation_observed"]) is not bool:
            raise EvalInputError("activation_observed must be boolean when supplied")
        if type(rec["critical_violation"]) is not bool:
            raise EvalInputError("critical_violation must be boolean")
        _exact_int(rec["review_calls"], "review_calls")
        if rec.get("tokens") is not None:
            _exact_int(rec["tokens"], "tokens")
        if rec.get("latency_ms") is not None:
            _exact_int(rec["latency_ms"], "latency_ms")
        if rec["variant"] in by_task[rec["task_id"]]:
            raise EvalInputError(f"duplicate {rec['variant']} for {rec['task_id']}")
        by_task[rec["task_id"]][rec["variant"]] = rec

    pairs: list[dict[str, Any]] = []
    for task_id, pair in sorted(by_task.items()):
        if set(pair) != {"baseline", "candidate"}:
            raise EvalInputError(f"incomplete pair for {task_id}")
        b, c = pair["baseline"], pair["candidate"]
        for field in ("input_sha", "host", "model", "tool_config", "expected_skill"):
            if b[field] != c[field]:
                raise EvalInputError(f"incomparable {task_id}: {field} differs")
        if b["run_id"] == c["run_id"]:
            raise EvalInputError(f"same run ID used for both variants: {task_id}")
        if b["skill_sha"] == c["skill_sha"]:
            raise EvalInputError(f"identical old/candidate skill SHA: {task_id}")
        baseline_activation, candidate_activation = _activation(b), _activation(c)
        pairs.append({
            "task_id": task_id,
            "provenance": {variant: {key: source[key] for key in
                                      ("run_id", "input_sha", "host", "model", "tool_config", "skill_sha")}
                           for variant, source in (("baseline", b), ("candidate", c))},
            "baseline": b["status"],
            "candidate": c["status"],
            "baseline_critical": b["critical_violation"],
            "candidate_critical": c["critical_violation"],
            "baseline_activation": baseline_activation,
            "candidate_activation": candidate_activation,
            "baseline_false_activation": baseline_activation == "false_activation",
            "candidate_false_activation": candidate_activation == "false_activation",
            "baseline_legacy_activation_mismatch": b["activated_skill"] != b["expected_skill"],
            "candidate_legacy_activation_mismatch": c["activated_skill"] != c["expected_skill"],
            "baseline_activation_observed": b.get("activation_observed", b["activated_skill"] is not None),
            "candidate_activation_observed": c.get("activation_observed", c["activated_skill"] is not None),
            "baseline_expected_skill": b["expected_skill"],
            "candidate_expected_skill": c["expected_skill"],
            "baseline_activated_skill": b["activated_skill"],
            "candidate_activated_skill": c["activated_skill"],
            "review_calls_delta": c["review_calls"] - b["review_calls"],
            "tokens_delta": (c["tokens"] - b["tokens"]
                             if b.get("tokens") is not None and c.get("tokens") is not None
                             else None),
            "latency_ms_delta": (c["latency_ms"] - b["latency_ms"]
                                 if b.get("latency_ms") is not None and c.get("latency_ms") is not None
                                 else None),
        })
    n = len(pairs)
    tokens_complete = all(p["tokens_delta"] is not None for p in pairs)
    latency_complete = all(p["latency_ms_delta"] is not None for p in pairs)
    counts: dict[str, int] = {}
    for variant in ("baseline", "candidate"):
        for category in _ACTIVATION_CATEGORIES:
            label = category.removesuffix("_activation") + "_activations"
            counts[f"{variant}_{label}"] = sum(p[f"{variant}_activation"] == category for p in pairs)
        counts[f"{variant}_legacy_activation_mismatches"] = sum(p[f"{variant}_legacy_activation_mismatch"] for p in pairs)
    return {
        "schema_version": 2,
        **counts,
        "evidence": "unverified external execution records; validate trace/artifact provenance",
        "paired_tasks": n,
        "baseline_pass": sum(p["baseline"] == "PASS" for p in pairs),
        "candidate_pass": sum(p["candidate"] == "PASS" for p in pairs),
        "candidate_critical_violations": sum(p["candidate_critical"] for p in pairs),
        "new_critical_regressions": sum(p["candidate_critical"] and not p["baseline_critical"]
                                        for p in pairs),
        "review_calls_delta": sum(p["review_calls_delta"] for p in pairs),
        "tokens_delta_total": sum(p["tokens_delta"] for p in pairs) if tokens_complete else None,
        "latency_ms_delta_total": sum(p["latency_ms_delta"] for p in pairs) if latency_complete else None,
        "tokens_measurement": "actual host-reported counts only" if tokens_complete else "not comparable or missing",
        "paired_results": pairs,
    }
