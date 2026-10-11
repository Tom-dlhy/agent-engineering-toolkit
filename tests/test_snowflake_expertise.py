"""Snowflake experts: deterministic catalog, reference and routing regression.

No Snowflake account access, warehouse use, SQL mutation or model calls.
Held-out agent/Snowflake validation remains a distinct future activity.
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

SNOWFLAKE = {
    "snowflake-query-performance",
    "snowflake-data-pipelines",
    "snowflake-snowpark-ml",
    "snowflake-cortex-ai",
    "snowflake-security-governance",
}


class SnowflakeExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.scenarios = yaml.safe_load(
            (ROOT / "evals/snowflake-routing.yaml").read_text(encoding="utf-8")
        )

    def test_inventory_and_data_domain_not_duplicated(self):
        self.assertEqual(len(self.catalog), 171)
        self.assertEqual(len({s.domain for s in self.catalog.values()}), 14)
        actual = {n for n, s in self.catalog.items() if s.domain == "data-platforms"}
        self.assertEqual(actual, SNOWFLAKE)
        self.assertEqual(len(list((ROOT / "skills").glob("*/**/references/*.md"))), 397)
        cross_domain_owners = (
            "lakehouse-engineering", "analytics-modeling",
            "data-pipeline-quality", "streaming-cdc-engineering",
            "llm-evaluation", "rag-engineering", "aws-bedrock",
            "cloud-provider-selection", "finops-engineering",
        )
        for name in cross_domain_owners:
            self.assertIn(name, self.catalog)

    def test_each_specialist_three_complete_selective_references(self):
        for name in sorted(SNOWFLAKE):
            with self.subTest(skill=name):
                skill = self.catalog[name]
                self.assertEqual(skill.path, f"skills/data-platforms/{name}")
                self.assertIn("Use when", skill.description)
                self.assertIn("Do not", skill.description)
                root_body = (ROOT / skill.path / "SKILL.md").read_text(encoding="utf-8")
                self.assertGreater(len(root_body), 2500)
                self.assertIn("## ", root_body)
                refs = indexed_references(skill, ROOT)
                self.assertEqual(len(refs), 3)
                for ref in refs:
                    leaf = read_reference(skill, ref, ROOT)
                    self.assertTrue(leaf.startswith("# "))
                    self.assertIn("Read when:", leaf[:220])
                    self.assertGreater(len(leaf), 1900, (name, ref))
                    self.assertIn("https://docs.snowflake.com/", leaf)
                    self.assertIn("## ", leaf)
                for forbidden in (
                    "SKILL.md", "../SKILL.md", "references/../SKILL.md",
                    "references/absent.md",
                ):
                    with self.assertRaises(ValueError):
                        read_reference(skill, forbidden, ROOT)

    def test_positive_specific_snowflake_routing(self):
        for case in self.scenarios["selection"]:
            with self.subTest(case=case["id"]):
                hits = search(case["query"], self.catalog, limit=5)
                self.assertTrue(hits, case)
                self.assertEqual(hits[0].skill.name, case["expected"], case)

    def test_no_hijack_of_existing_specialists(self):
        for case in self.scenarios["negative_neighbors"]:
            with self.subTest(case=case["id"]):
                hits = search(case["query"], self.catalog, limit=5)
                self.assertTrue(hits, case)
                self.assertEqual(hits[0].skill.name, case["expected"], case)

    def test_no_automatic_profile_growth_or_agent_overload(self):
        profiles = sorted((ROOT / "profiles").glob("*.yaml"))
        self.assertEqual(len(profiles), 20)
        for path in profiles:
            with self.subTest(profile=path.stem):
                names = load_profile(path.stem, ROOT)
                self.assertFalse(set(names) & SNOWFLAKE)
                tokens, count = estimate(path.stem, ROOT)
                self.assertLessEqual(count, 20)
                self.assertLessEqual(tokens, 2500)

    def test_unrun_behavioral_scenarios_have_guardrails(self):
        self.assertEqual(self.scenarios.get("status"), "unexecuted")
        cases = self.scenarios["behavior"]
        self.assertEqual({x["expected"] for x in cases}, SNOWFLAKE)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["ask"])
                self.assertGreaterEqual(len(case["must"]), 2)
                self.assertTrue(case["must_not"])

    def test_offline_fixture_and_governance_docs_constrain_claims(self):
        audit = (ROOT / "docs/snowflake-platform-audit.md").read_text()
        for name in SNOWFLAKE:
            self.assertIn(name, audit)
        for term in (
            "owner's-rights", "TARGET_LAG", "LightGBM",
            "Enterprise Edition", "unexecuted",
        ):
            self.assertIn(term.lower(), audit.lower())
        source = (ROOT / "examples/snowflake/temporal_replay_contract.py").read_text()
        self.assertIn("available_at", source)
        self.assertIn("source_version", source)
        self.assertNotIn("snowflake.connector", source)

    def test_complete_repo_contract(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
