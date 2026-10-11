"""Databricks specialist static contracts. No Databricks account or model usage."""
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

DATABRICKS = {
    "databricks-spark-delta",
    "databricks-lakeflow-pipelines",
    "databricks-unity-catalog",
    "databricks-mlflow-mlops",
    "databricks-automation-bundles",
    "databricks-ai-governance",
}


class DatabricksExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.cases = yaml.safe_load(
            (ROOT / "evals/databricks-routing.yaml").read_text(encoding="utf-8")
        )

    def test_catalog_invariants_and_distinct_provider_scope(self):
        self.assertEqual(len(self.catalog), 177)
        self.assertEqual(len({s.domain for s in self.catalog.values()}), 14)
        platform = {n for n,s in self.catalog.items() if s.domain == "data-platforms"}
        self.assertEqual(len(platform), 11)
        self.assertEqual({n for n in platform if n.startswith("databricks-")}, DATABRICKS)
        self.assertEqual(len({n for n in platform if n.startswith("snowflake-")}), 5)
        self.assertEqual(len(list((ROOT / "skills").glob("*/**/references/*.md"))), 415)

    def test_each_specialist_has_independent_deep_refs_and_factual_sources(self):
        for name in sorted(DATABRICKS):
            with self.subTest(name=name):
                skill = self.catalog[name]
                self.assertEqual(skill.path, f"skills/data-platforms/{name}")
                self.assertEqual(skill.domain, "data-platforms")
                self.assertIn("Use when", skill.description)
                self.assertIn("Do not", skill.description)
                text = (ROOT / skill.path / "SKILL.md").read_text(encoding="utf-8")
                self.assertGreater(len(text), 3000)
                self.assertIn("## ", text)
                refs = indexed_references(skill, ROOT)
                self.assertEqual(len(refs), 3)
                for ref in refs:
                    leaf = read_reference(skill, ref, ROOT)
                    self.assertTrue(leaf.startswith("# "))
                    self.assertIn("Read when:", leaf[:250])
                    self.assertGreater(len(leaf), 1900, (name,ref))
                    self.assertIn("https://docs.databricks.com/", leaf)
                    self.assertIn("## ", leaf)
                for bad in ("../SKILL.md", "references/absent.md",
                            "references/../SKILL.md"):
                    with self.assertRaises(ValueError):
                        read_reference(skill, bad, ROOT)

    def test_all_positive_databricks_routes(self):
        for case in self.cases["selection"]:
            with self.subTest(case=case["id"]):
                found = search(case["query"], self.catalog, limit=5)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, case["expected"])

    def test_existing_skill_routes_remain_unchanged(self):
        for case in self.cases["negative_neighbors"]:
            with self.subTest(case=case["id"]):
                found = search(case["query"], self.catalog, limit=5)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, case["expected"])

    def test_six_skills_are_opt_in_and_20_profiles_unchanged(self):
        paths = sorted((ROOT / "profiles").glob("*.yaml"))
        self.assertEqual(len(paths), 20)
        for p in paths:
            with self.subTest(profile=p.stem):
                self.assertTrue(DATABRICKS.isdisjoint(load_profile(p.stem, ROOT)))
                budget, count = estimate(p.stem, ROOT)
                self.assertLessEqual(budget, 2500)
                self.assertLessEqual(count, 20)

    def test_behavioral_evals_are_explicitly_unexecuted(self):
        self.assertEqual(self.cases["status"], "unexecuted")
        behaviors = self.cases["behavior"]
        self.assertEqual({c["expected"] for c in behaviors}, DATABRICKS)
        for case in behaviors:
            self.assertTrue(case["ask"])
            self.assertGreaterEqual(len(case["must"]), 2)
            self.assertTrue(case["must_not"])

    def test_offline_evidence_limits_and_governance(self):
        text = (ROOT / "docs/databricks-platform-audit.md").read_text().lower()
        for name in DATABRICKS:
            self.assertIn(name, text)
        for word in ("lakeflow", "abac", "unity gateway", "mlflow 3",
                     "declarative automation bundles", "unexecuted"):
            self.assertIn(word, text)
        src = (ROOT / "examples/databricks/cdc_replay_contract.py").read_text()
        self.assertIn("source sequence", src)
        self.assertNotIn("databricks.sdk", src)

    def test_validator(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
