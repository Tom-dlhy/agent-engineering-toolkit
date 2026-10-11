"""Deterministic source-revision and delete semantics, no network or DB."""
from __future__ import annotations

import unittest
from examples.data_quality_replay.upsert import Change, live_values, reduce_changes


class DataReplayContractTests(unittest.TestCase):
    def test_duplicate_exact_replay_is_idempotent(self) -> None:
        e = Change("A", "order1", 7, "upsert", 100)
        self.assertEqual(live_values([e, e, e]), {("A", "order1"): 100})

    def test_late_older_update_cannot_override_newer_state(self) -> None:
        recent = Change("A", "order1", 9, "upsert", 200)
        stale = Change("A", "order1", 8, "upsert", 100)
        self.assertEqual(live_values([recent, stale]), {("A", "order1"): 200})

    def test_tombstone_prevents_stale_resurrection(self) -> None:
        events = [
            Change("A", "order1", 4, "upsert", 100),
            Change("A", "order1", 6, "delete", None),
            Change("A", "order1", 5, "upsert", 150),
        ]
        self.assertEqual(live_values(events), {})
        self.assertEqual(reduce_changes(events)[("A","order1")].revision, 6)

    def test_tenants_with_same_source_key_remain_separate(self) -> None:
        events = [Change("A","1",1,"upsert",10), Change("B","1",1,"upsert",20)]
        self.assertEqual(len(live_values(events)), 2)

    def test_same_revision_conflicting_payload_fails(self) -> None:
        with self.assertRaises(ValueError):
            live_values([Change("A","1",5,"upsert",10),
                         Change("A","1",5,"upsert",99)])

    def test_reject_invalid_amount_and_operation(self) -> None:
        with self.assertRaises(ValueError):
            live_values([Change("A","1",1,"upsert",-1)])
        with self.assertRaises(ValueError):
            live_values([Change("A","1",1,"delete",5)])
        with self.assertRaises(ValueError):
            live_values([Change("A","1",1,"unexpected",None)])

    def test_order_independence_for_different_source_revisions(self) -> None:
        events = [Change("A","1",1,"upsert",10),
                  Change("A","1",3,"upsert",30),
                  Change("A","1",2,"upsert",20)]
        self.assertEqual(live_values(events), live_values(list(reversed(events))))


if __name__ == "__main__":
    unittest.main()
