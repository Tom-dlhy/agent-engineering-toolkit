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
        r = compare_pairs([record("baseline"), record("candidate", activated="unwanted-skill")])
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


class ActivationEvidenceTests(unittest.TestCase):
    def report(self, **changes):
        return compare_pairs([record("baseline"), {**record("candidate"), **changes}])

    def test_legacy_null_is_unknown_not_false_or_missed(self):
        result = self.report(activated_skill=None)
        self.assertEqual(result["candidate_false_activations"], 0)
        self.assertEqual(result.get("candidate_unknown_activations"), 1)
        self.assertEqual(result.get("candidate_missed_activations"), 0)
        self.assertEqual(result.get("candidate_legacy_activation_mismatches"), 1)

    def test_observed_absence_is_missed(self):
        result = self.report(activated_skill=None, activation_observed=True)
        self.assertEqual(result["candidate_false_activations"], 0)
        self.assertEqual(result.get("candidate_missed_activations"), 1)

    def test_not_run_is_neither_failure_nor_observed_activation(self):
        result = self.report(status="NOT_RUN", activated_skill=None, activation_observed=True)
        self.assertEqual(result["candidate_false_activations"], 0)
        self.assertEqual(result.get("candidate_not_run_activations"), 1)
        self.assertEqual(result.get("candidate_missed_activations"), 0)

    def test_explicit_unobserved_named_activation_is_unknown(self):
        result = self.report(activation_observed=False)
        self.assertEqual(result.get("candidate_unknown_activations"), 1)
        self.assertEqual(result.get("candidate_correct_activations"), 0)

    def test_legacy_named_activation_remains_reported_observation(self):
        result = self.report()
        self.assertEqual(result.get("schema_version"), 2)
        self.assertEqual(result.get("candidate_correct_activations"), 1)

    def test_negative_control_observed_absence_and_unwanted_activation(self):
        for activated, category in ((None, "correct_non_activation"), ("widget", "false_activation")):
            b, c = record("baseline"), record("candidate", activated=activated)
            b.update(expected_skill=None, activated_skill=None, activation_observed=True)
            c.update(expected_skill=None, activation_observed=True)
            result = compare_pairs([b, c])
            self.assertEqual(result["paired_results"][0].get("candidate_activation"), category)

    def test_omitted_telemetry_is_unknown_without_mutating_records(self):
        b, c = record("baseline"), record("candidate")
        del c["activated_skill"]
        result = compare_pairs([b, c])
        self.assertEqual(result["candidate_unknown_activations"], 1)
        self.assertNotIn("activated_skill", c)

    def test_observed_absence_requires_explicit_null(self):
        b, c = record("baseline"), record("candidate")
        del c["activated_skill"]
        c["activation_observed"] = True
        with self.assertRaises(EvalInputError):
            compare_pairs([b, c])

    def test_blocked_without_telemetry_is_unknown(self):
        result = self.report(status="BLOCKED", activated_skill=None)
        self.assertEqual(result["candidate_unknown_activations"], 1)
        self.assertEqual(result["candidate_false_activations"], 0)

    def test_invalid_observation_flag_and_empty_skill_names_rejected(self):
        for changes in ({"activation_observed": 1}, {"activation_observed": None},
                        {"activated_skill": ""}, {"expected_skill": "  "}):
            with self.subTest(changes=changes), self.assertRaises(EvalInputError):
                self.report(**changes)


if __name__ == "__main__":
    unittest.main()
