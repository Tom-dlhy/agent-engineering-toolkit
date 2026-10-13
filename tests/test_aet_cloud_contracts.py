"""Targeted documentary regression gates for selected cloud AET guidance.

No fake test here establishes Azure, D1 replica or production SLO behavior.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def leaf(name: str) -> str:
    return (ROOT / "skills" / "cloud" / name / "references" /
            ("selection-and-implementation.md" if name == "observability-sre"
             else "operations-and-recovery.md")).read_text(encoding="utf-8")


class AETCloudContractTests(unittest.TestCase):
    def test_azure_service_bus_uses_durable_recovery_not_lock_as_exactly_once(self) -> None:
        text = leaf("azure-service-bus")
        for concept in ("PeekLock", "ReceiveAndDelete", "detected",
                        "failed Complete is not a rollback", "redelivery",
                        "stable", "external idempotency", "receiver connection open"):
            self.assertIn(concept.lower(), text.lower())
        self.assertIn("no new business effect", text)
        self.assertIn("does not provide", text)

    def test_d1_sessions_require_bookmark_continuity_and_auth(self) -> None:
        text = leaf("cloudflare-d1-database")
        for token in ('withSession("first-primary")', "first-unconstrained",
                      "session.getBookmark()", "withSession(bookmark)",
                      "authentication token", "tenant checks", "preview environment"):
            self.assertIn(token, text)
        self.assertIn("Do not replay a mutation", text)
        self.assertIn("not the replica's actual consistency", text)

    def test_request_burn_rate_arithmetic_and_both_window_policy(self) -> None:
        text = leaf("observability-sre")
        self.assertIn("burn_w = (bad_events_w / total_events_w) / (1 - s)", text)
        self.assertIn("BOTH windows breach", text)
        self.assertIn("UNKNOWN", text)
        self.assertIn("not a default", text)
        self.assertIn("not** success", text)
        self.assertIn("time-based/freshness", text)
        target = 0.999
        burn = (50 / 10000) / (1 - target)
        self.assertAlmostEqual(burn, 5.0)
        threshold = 4
        self.assertTrue(burn > threshold and 6 > threshold)
        self.assertFalse(burn > threshold and 2 > threshold)


if __name__ == "__main__":
    unittest.main()
