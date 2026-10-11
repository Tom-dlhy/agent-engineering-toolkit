"""Executable educational negative cases; no network or external dependencies."""
import unittest

from examples.quality_fixtures.application import (
    AccessDenied,
    ExampleLedger,
    IdempotencyConflict,
)


class QualityFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = ExampleLedger()

    def test_authorized_success(self) -> None:
        out = self.ledger.apply(
            authenticated_tenant="A", target_tenant="A",
            request_id="first", amount=100,
        )
        self.assertEqual(out.amount, 100)
        self.assertEqual(self.ledger.effects, 1)

    def test_same_key_replay_does_not_repeat_effect(self) -> None:
        params = dict(
            authenticated_tenant="A", target_tenant="A",
            request_id="same", amount=100,
        )
        first = self.ledger.apply(**params)
        second = self.ledger.apply(**params)
        self.assertIs(first, second)
        self.assertEqual(self.ledger.effects, 1)

    def test_same_key_changed_payload_fails_without_mutation(self) -> None:
        args = dict(authenticated_tenant="A", target_tenant="A", request_id="same")
        self.ledger.apply(**args, amount=100)
        with self.assertRaises(IdempotencyConflict):
            self.ledger.apply(**args, amount=200)
        self.assertEqual(self.ledger.effects, 1)

    def test_wrong_tenant_does_not_change_state(self) -> None:
        with self.assertRaises(AccessDenied):
            self.ledger.apply(
                authenticated_tenant="B", target_tenant="A",
                request_id="secret", amount=100,
            )
        self.assertEqual(self.ledger.effects, 0)

    def test_tenant_key_isolated(self) -> None:
        for tenant in ("A", "B"):
            self.ledger.apply(
                authenticated_tenant=tenant, target_tenant=tenant,
                request_id="same", amount=100,
            )
        self.assertEqual(self.ledger.effects, 2)

    def test_invalid_amount_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.ledger.apply(
                authenticated_tenant="A", target_tenant="A",
                request_id="first", amount=0,
            )
        self.assertEqual(self.ledger.effects, 0)


if __name__ == "__main__":
    unittest.main()
