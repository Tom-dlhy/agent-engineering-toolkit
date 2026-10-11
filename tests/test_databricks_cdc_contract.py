"""Check source ordering and business-key semantics without Databricks access."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples/databricks/cdc_replay_contract.py"
spec = importlib.util.spec_from_file_location("databricks_cdc_contract", SOURCE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class DatabricksCDCContractTests(unittest.TestCase):
    def test_scd1_is_order_independent_and_idempotent(self):
        one = module.Change("k", 1, 10)
        two = module.Change("k", 2, 20)
        other = module.Change("x", 1, 7)
        expected = {"k": 20, "x": 7}
        self.assertEqual(module.scd1([two, one, other, one]), expected)
        self.assertEqual(module.scd1([other, one, two]), expected)

    def test_late_old_update_does_not_resurrect_deleted_entity(self):
        prior = module.Change("k", 1, 10)
        erased = module.Change("k", 3, None, deleted=True)
        self.assertEqual(module.scd1([erased, prior, prior]), {})

    def test_scd2_uses_source_order_and_nonoverlapping_intervals(self):
        rows = module.scd2([
            module.Change("k", 9, None, deleted=True),
            module.Change("k", 2, 10),
            module.Change("k", 5, 15),
        ])
        self.assertEqual([(x.valid_from, x.valid_to) for x in rows],
                         [(2, 5), (5, 9), (9, None)])
        self.assertTrue(rows[-1].deleted)

    def test_duplicate_same_version_with_identical_content_is_stable(self):
        e = module.Change("k", 1, 10)
        self.assertEqual(len(module.scd2([e, e, e])), 1)

    def test_conflicting_equal_source_sequences_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "conflicting"):
            module.scd1([module.Change("k", 1, 10),
                         module.Change("k", 1, 11)])

    def test_missing_key_and_negative_sequence_are_invalid(self):
        with self.assertRaises(ValueError):
            module.scd1([module.Change("", 0, 5)])
        with self.assertRaises(ValueError):
            module.scd2([module.Change("k", -1, 5)])

    def test_tombstone_cannot_contain_business_value(self):
        with self.assertRaises(ValueError):
            module.scd1([module.Change("k", 1, 10, deleted=True)])

    def test_no_provider_api_or_destructive_query(self):
        source = SOURCE.read_text(encoding="utf-8")
        for forbidden in ("databricks.sdk", "pyspark", "requests.", "subprocess",
                          "DROP TABLE", "bundle destroy", "os.environ"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
