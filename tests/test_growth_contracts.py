"""Executable, offline Growth fixture tests; not integration with analytics/CRM providers."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "examples" / "growth-contracts" / "contract_checks.py"
spec = importlib.util.spec_from_file_location("growth_contracts", MODULE)
assert spec is not None and spec.loader is not None
import sys
growth = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = growth
spec.loader.exec_module(growth)


class GrowthContractChecksTests(unittest.TestCase):
    def test_healthy_allocation_dedupes_repeated_exposure_logs(self):
        events = [(f"c{i}", "control") for i in range(50)]
        events += [(f"t{i}", "treatment") for i in range(50)]
        events += [("c1", "control"), ("c1", "control")]
        got = growth.check_two_arm_allocation(events)
        self.assertEqual(got.unique_units, 100)
        self.assertEqual(got.duplicate_logs, 2)
        self.assertEqual((got.control, got.treatment), (50, 50))
        self.assertFalse(got.srm_flagged)
        self.assertAlmostEqual(got.srm_pvalue, 1.0)

    def test_severe_srm_detected_without_making_lift_claims(self):
        events = [(f"c{i}", "control") for i in range(95)]
        events += [(f"t{i}", "treatment") for i in range(5)]
        got = growth.check_two_arm_allocation(events)
        self.assertTrue(got.srm_flagged)
        self.assertLess(got.srm_pvalue, 0.001)

    def test_small_sample_does_not_claim_srm_clear(self):
        self.assertIsNone(growth.check_two_arm_allocation(
            [("c1", "control"), ("t1", "treatment")]
        ).srm_flagged)

    def test_cross_variant_assignment_fails(self):
        with self.assertRaisesRegex(ValueError, "changed variants"):
            growth.check_two_arm_allocation([
                ("u1", "control"), ("u1", "treatment")
            ])

    def test_invalid_experiment_parameters_fail(self):
        for share in (0, 1, -0.1, 1.5):
            with self.subTest(share=share), self.assertRaises(ValueError):
                growth.check_two_arm_allocation([], expected_control_share=share)
        with self.assertRaises(ValueError):
            growth.check_two_arm_allocation([], srm_threshold=0)

    def test_marketing_requires_live_permission(self):
        base = dict(permission_current=True, recipient_suppressed=False,
                    account_active=True, journey_complete=False,
                    frequency_cap_reached=False, trigger_expired=False)
        state = growth.MarketingEligibility(**base)
        self.assertEqual(growth.evaluate_marketing_send(state), (True, "eligible"))
        for field, value, reason in (
            ("permission_current", False, "permission_missing"),
            ("recipient_suppressed", True, "suppressed"),
            ("account_active", False, "account_inactive"),
            ("journey_complete", True, "journey_completed"),
            ("frequency_cap_reached", True, "frequency_cap"),
            ("trigger_expired", True, "trigger_expired"),
        ):
            with self.subTest(block=field):
                changed = {**base, field: value}
                self.assertEqual(growth.evaluate_marketing_send(
                    growth.MarketingEligibility(**changed)
                ), (False, reason))

    def test_unsubscribe_precedence_even_if_other_fields_valid(self):
        state = growth.MarketingEligibility(True, True, True, False, False, False)
        self.assertEqual(growth.evaluate_marketing_send(state), (False, "suppressed"))


if __name__ == "__main__":
    unittest.main()
