"""Offline Stack decision guardrail. This is not a cloud/provider benchmark."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples" / "stacks-selection" / "decision_contract.py"
spec = importlib.util.spec_from_file_location("stack_decision_contract", SOURCE)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class StackDecisionContractTests(unittest.TestCase):
    def test_hard_veto_overrides_high_preference(self):
        options = [
            mod.Candidate("sexy-edge-stack", {"data_residency": False, "server_auth": True}, {"easy": 5}),
            mod.Candidate("boring-current-stack", {"data_residency": True, "server_auth": True}, {"easy": 2}),
        ]
        result = mod.evaluate_candidates(options, ("data_residency", "server_auth"), {"easy": 1})
        self.assertEqual([x.name for x in result], ["boring-current-stack", "sexy-edge-stack"])
        self.assertFalse(result[1].eligible)
        self.assertIsNone(result[1].score)
        self.assertEqual(result[1].vetoes, ("data_residency",))

    def test_unknown_must_is_not_assumed_safe(self):
        result = mod.evaluate_candidates([
            mod.Candidate("unverified", {"db_transactions": None}, {"easy": 5}),
        ], ("db_transactions",), {"easy": 1})
        self.assertFalse(result[0].eligible)
        self.assertEqual(result[0].unknown_hard_checks, ("db_transactions",))
        self.assertIsNone(result[0].score)

    def test_absent_must_is_unknown(self):
        result = mod.evaluate_candidates([
            mod.Candidate("not-tested", {}, {"easy": 4}),
        ], ("server_auth",), {"easy": 1})
        self.assertFalse(result[0].eligible)
        self.assertEqual(result[0].unknown_hard_checks, ("server_auth",))

    def test_explicit_weights_only_rank_viable_choices(self):
        options = [
            mod.Candidate("cost-first", {"safe": True}, {"cost": 5, "maintain": 1}),
            mod.Candidate("ops-first", {"safe": True}, {"cost": 2, "maintain": 5}),
        ]
        choices = mod.evaluate_candidates(options, ("safe",), {"cost": 1, "maintain": 2})
        self.assertEqual(choices[0].name, "ops-first")
        self.assertAlmostEqual(choices[0].score, 4.0)

    def test_reject_invalid_weights_and_subjective_grades(self):
        c = mod.Candidate("a", {"safe": True}, {"ease": 6})
        with self.assertRaises(ValueError):
            mod.evaluate_candidates([c], ("safe",), {"ease": 1})
        with self.assertRaises(ValueError):
            mod.evaluate_candidates([c], ("safe",), {"ease": float("nan")})
        with self.assertRaises(ValueError):
            mod.evaluate_candidates([c], ("safe",), {"ease": 0})
        with self.assertRaises(ValueError):
            mod.evaluate_candidates([c, c], ("safe",), {"ease": 1})

    def test_decision_does_not_change_project_or_install_anything(self):
        text = SOURCE.read_text()
        for dangerous in ("subprocess", "pip install", "npm install", "boto3", "requests.", "open("):
            self.assertNotIn(dangerous, text)


if __name__ == "__main__":
    unittest.main()
