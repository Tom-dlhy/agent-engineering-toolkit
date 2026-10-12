"""Offline evidence contracts; DOES NOT perform or certify native agent runs."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toolkit.skill_eval_report import EvalInputError, compare_pairs


def record(variant: str, *, task: str = "t1", tokens: int | None = 100,
           status: str = "PASS", activated: str | None = "test-strategy",
           critical: bool = False, run: str | None = None):
    return dict(task_id=task, variant=variant,
                run_id=run or variant, input_sha="input-1", host="claude-code",
                model="pinned-model", tool_config="read-test-only",
                skill_sha="old-skill-rev" if variant == "baseline" else "new-skill-rev",
                status=status, expected_skill="test-strategy",
                activated_skill=activated, critical_violation=critical,
                review_calls=1 if variant == "baseline" else 0,
                tokens=tokens, latency_ms=1000)


class PairedEvalTests(unittest.TestCase):
    def test_comparable_pair_measures_observed_deltas(self):
        result = compare_pairs([record("baseline"), record("candidate", tokens=80)])
        self.assertEqual(result["paired_tasks"], 1)
        self.assertEqual(result["candidate_pass"], 1)
        self.assertEqual(result["tokens_delta_total"], -20)
        self.assertEqual(result["review_calls_delta"], -1)
        self.assertEqual(result["candidate_false_activations"], 0)

    def test_missing_tokens_do_not_fake_cost_savings(self):
        report = compare_pairs([record("baseline"), record("candidate", tokens=None)])
        self.assertIsNone(report["tokens_delta_total"])
        self.assertIn("not comparable", report["tokens_measurement"])

    def test_critical_regression_is_visible_even_with_better_tokens(self):
        r = compare_pairs([record("baseline"), record("candidate", tokens=50,
                                                    critical=True, status="FAIL")])
        self.assertEqual(r["new_critical_regressions"], 1)
        self.assertEqual(r["candidate_pass"], 0)

    def test_wrong_skill_activation_is_counted(self):
        r = compare_pairs([record("baseline"), record("candidate", activated=None)])
        self.assertEqual(r["candidate_false_activations"], 1)

    def test_incomparable_runs_rejected(self):
        b, c = record("baseline"), record("candidate")
        for key, val in (("host", "different-host"), ("input_sha", "other-input"),
                         ("model", "other-model"), ("tool_config", "privileged"),
                         ("expected_skill", None), ("run_id", b["run_id"]),
                         ("skill_sha", b["skill_sha"])):
            changed = {**c, key: val}
            with self.subTest(field=key), self.assertRaises(EvalInputError):
                compare_pairs([b, changed])

    def test_partial_duplicate_and_invalid_records_rejected(self):
        b, c = record("baseline"), record("candidate")
        for input_data in ([], [b], [b, b, c], [{**b, "review_calls": -1}, c],
                           [{**b, "critical_violation": 1}, c],
                           [{**b, "tokens": -100}, c]):
            with self.subTest(value=str(input_data)[:100]), self.assertRaises(EvalInputError):
                compare_pairs(input_data)


if __name__ == "__main__":
    unittest.main()
