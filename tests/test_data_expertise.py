"""Data quality refactor regression tests: static integrity + lexical routing.

Real Postgres behavior is tested by the dedicated disposable database job.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference
from context_budget import estimate
from validate_skills import validate_repository

DATA = {
    "data-pipeline-quality": 4,
    "database-design": 3,
    "postgres-performance": 3,
    "schema-migrations": 3,
    "analytics-modeling": 3,
    "lakehouse-engineering": 3,
    "streaming-cdc-engineering": 3,
}


class DataExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.cases = yaml.safe_load(
            (ROOT / "evals/data-routing.yaml").read_text(encoding="utf-8")
        )

    def test_seven_distinct_data_skills_and_catalog_count(self):
        found = {s.name for s in self.catalog.values() if s.domain == "data"}
        self.assertEqual(found, set(DATA))
        self.assertEqual(len(self.catalog), 171)

    def test_single_quality_standard_with_no_maturity_rank(self):
        entries = yaml.safe_load(
            (ROOT / "registry/skills.yaml").read_text(encoding="utf-8")
        )["skills"]
        self.assertFalse(any("maturity" in entry for entry in entries))

    def test_22_source_annotated_local_refs(self):
        count = 0
        for name, expected in DATA.items():
            with self.subTest(name=name):
                skill = self.catalog[name]
                self.assertIn("Use when", skill.description)
                self.assertIn("Do not", skill.description)
                self.assertIn("## ", (ROOT / skill.path / "SKILL.md").read_text())
                refs = indexed_references(skill, ROOT)
                self.assertEqual(len(refs), expected)
                for ref in refs:
                    leaf = read_reference(skill, ref, ROOT)
                    self.assertGreater(len(leaf), 1500, (name, ref))
                    self.assertTrue(leaf.startswith("# "))
                    self.assertIn("Read when:", leaf[:600])
                    self.assertIn("## ", leaf)
                    self.assertIn("https://", leaf)
                    count += 1
        self.assertEqual(count, 22)

    def test_positive_routing(self):
        for case in self.cases["selection"]:
            with self.subTest(query=case["query"]):
                hits = search(case["query"], self.catalog, limit=3)
                self.assertTrue(hits)
                self.assertEqual(hits[0].skill.name, case["expected"])

    def test_negative_routing_does_not_hijack_other_domains(self):
        for case in self.cases["negative_neighbors"]:
            with self.subTest(query=case["query"]):
                hits = search(case["query"], self.catalog, limit=3)
                self.assertTrue(hits)
                self.assertEqual(hits[0].skill.name, case["expected"])

    def test_no_match_does_not_force_skill(self):
        for query in self.cases["no_match"]:
            self.assertEqual(search(query, self.catalog), [])

    def test_reference_security_and_opt_in_loading(self):
        skill = self.catalog["streaming-cdc-engineering"]
        ref = "references/debezium-cdc-and-wal.md"
        self.assertIn(ref, indexed_references(skill, ROOT))
        for invalid in ("../SKILL.md", "references/../../README.md",
                        "references/not-declared.md"):
            with self.subTest(path=invalid), self.assertRaises(ValueError):
                read_reference(skill, invalid, ROOT)
        base, _ = estimate("data-engineering", ROOT)
        active, _ = estimate("data-engineering", ROOT, ("streaming-cdc-engineering",))
        leaf, _ = estimate(
            "data-engineering", ROOT, ("streaming-cdc-engineering",),
            ("streaming-cdc-engineering:references/debezium-cdc-and-wal.md",),
        )
        self.assertLess(base, active)
        self.assertLess(active, leaf)
        self.assertLessEqual(base, 2500)

    def test_profile_opt_in_and_no_global_pollution(self):
        items = load_profile("data-engineering", ROOT)
        for name in DATA:
            self.assertIn(name, items)
        self.assertEqual(len(items), 15)
        self.assertNotIn("streaming-cdc-engineering", load_profile("minimal", ROOT))

    def test_official_source_audit_records_limits(self):
        text = (ROOT / "docs/data-refactor-audit.md").read_text()
        for word in ("PostgreSQL", "dbt", "Airflow", "Snowflake", "Iceberg",
                     "Flink", "Debezium", "BigQuery", "SOTA"):
            self.assertIn(word, text)

    def test_repository_integrity(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
