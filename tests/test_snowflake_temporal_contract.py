"""Pure deterministic examples: no Snowflake account required."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples" / "snowflake" / "temporal_replay_contract.py"
spec = importlib.util.spec_from_file_location("snowflake_temporal_contract", SOURCE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def time(day: int, hour: int = 0) -> datetime:
    return datetime(2026, 1, day, hour, tzinfo=timezone.utc)


class TemporalContractTests(unittest.TestCase):
    def test_temporal_join_blocks_backfilled_feature_leakage(self):
        past = module.FeatureVersion("C1", time(1), time(2), 1, 10.0)
        late = module.FeatureVersion("C1", time(1), time(5), 2, 999.0)
        self.assertEqual(
            module.asof_feature("C1", time(3), [past, late]), past
        )
        self.assertEqual(
            module.asof_feature("C1", time(6), [past, late]), late
        )

    def test_event_time_after_observation_never_eligible(self):
        future_event = module.FeatureVersion("C1", time(5), time(2), 3, 42.0)
        self.assertIsNone(module.asof_feature("C1", time(3), [future_event]))

    def test_missing_feature_and_entity_isolation(self):
        one = module.FeatureVersion("C1", time(1), time(2), 1, 1.0)
        self.assertIsNone(module.asof_feature("C2", time(3), [one]))
        self.assertIsNone(module.asof_feature("C1", time(1), [one]))

    def test_timezone_naive_timestamp_fails_closed(self):
        row = module.FeatureVersion("C1", time(1), time(2), 1, 1.0)
        with self.assertRaises(ValueError):
            module.asof_feature("C1", datetime(2026, 1, 3), [row])

    def test_duplicate_file_replay_and_order_does_not_change_state(self):
        a = module.SourceChange("orderA", 1, 10.0)
        a2 = module.SourceChange("orderA", 2, 12.0)
        b = module.SourceChange("orderB", 1, 7.0)
        desired = {"orderA": 12.0, "orderB": 7.0}
        self.assertEqual(module.published_values([a, b, a, a2]), desired)
        self.assertEqual(module.published_values([a2, a, b, a]), desired)

    def test_tombstone_and_late_old_version_do_not_resurrect(self):
        old = module.SourceChange("orderA", 1, 10.0)
        deleted = module.SourceChange("orderA", 3, None, True)
        self.assertEqual(module.published_values([deleted, old, deleted]), {})

    def test_conflicting_same_version_is_an_error(self):
        first = module.SourceChange("orderA", 2, 10.0)
        conflict = module.SourceChange("orderA", 2, 15.0)
        with self.assertRaisesRegex(ValueError, "conflicting"):
            module.replay_changes([first, conflict])

    def test_invalid_delete_and_identity_are_errors(self):
        with self.assertRaises(ValueError):
            module.replay_changes([module.SourceChange("", 0, 3.0)])
        with self.assertRaises(ValueError):
            module.replay_changes([module.SourceChange("order", -1, 3.0)])
        with self.assertRaises(ValueError):
            module.replay_changes([module.SourceChange("order", 1, 1.0, True)])

    def test_example_has_no_provider_or_external_actions(self):
        src = SOURCE.read_text()
        for marker in ("subprocess", "requests.", "snowflake.connector", "boto3",
                       "DROP TABLE", "CREATE OR REPLACE", "os.environ"):
            self.assertNotIn(marker, src)


if __name__ == "__main__":
    unittest.main()
