"""Stacks domain coverage, safe routing, references and catalog compatibility."""
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

STACKS = {
    "stack-advisor": 3,
    "database-selection": 3,
    "ui-library-selection": 3,
    "authentication-solution-selection": 3,
}


class StacksExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.stacks = {n: s for n, s in cls.catalog.items() if s.domain == "stacks"}

    def test_domain_inventory_no_provider_duplication(self):
        self.assertEqual(len(self.catalog), 178)
        self.assertEqual(set(self.stacks), set(STACKS))
        self.assertEqual(sum(len(indexed_references(x, ROOT)) for x in self.stacks.values()), 12)
        self.assertEqual(len([x for x in self.catalog.values() if x.domain == "ui"]), 36)
        for existing in ("cloud-provider-selection", "technology-tradeoffs",
                         "database-design", "schema-migrations", "aws-iam-security",
                         "cloudflare-access-security", "secure-code-review"):
            self.assertIn(existing, self.catalog)

    def test_all_refs_are_on_demand_safe_substantial(self):
        for name, expected in STACKS.items():
            with self.subTest(name=name):
                s = self.stacks[name]
                refs = indexed_references(s, ROOT)
                self.assertEqual(len(refs), expected)
                self.assertIn("Use when", s.description)
                self.assertIn("Do not", s.description)
                body = (ROOT / s.path / "SKILL.md").read_text()
                for ref in refs:
                    text = read_reference(s, ref, ROOT)
                    self.assertTrue(text.startswith("# "))
                    self.assertGreater(len(text), 1600)
                    self.assertIn("Read when:", text[:500] + text[:500].replace("**", ""))
                    self.assertIn("https://", text)
                for bad in ("SKILL.md", "../SKILL.md", "references/../SKILL.md",
                            "references/missing.md"):
                    with self.assertRaises(ValueError):
                        read_reference(s, bad, ROOT)

    def test_existing_ui_map_preserved_and_no_new_provider_engine(self):
        s = self.stacks["ui-library-selection"]
        leaf = read_reference(s, "references/library-map.md", ROOT)
        for name in ("shadcn-ui", "base-ui", "mui", "react-aria-components",
                     "flutter-material"):
            self.assertIn(name, leaf)
        self.assertIn("Base UI", read_reference(s,
            "references/compatibility-and-license-gates.md", ROOT))
        self.assertEqual(len([x for x in self.catalog.values() if x.domain == "ui"]), 36)

    def test_positive_and_negative_provider_routing(self):
        queries = {
            "stack advisor saas tech compatibility tco": "stack-advisor",
            "database selection postgres sqlite transactions consistency": "database-selection",
            "ui library selection shadcn mui licensing": "ui-library-selection",
            "authentication solution selection identity login oidc sso sessions": "authentication-solution-selection",
            "AWS IAM STS trust policy permission": "aws-iam-security",
            "Cloudflare Access JWT application policy": "cloudflare-access-security",
            "design database keys unique constraints RLS tenant": "database-design",
            "shadcn ui components.json registry": "shadcn-ui",
            "SQLAlchemy session rollback persistence": "python-persistence",
            "FastAPI Pydantic endpoint": "fastapi-service",
        }
        for query, expected in queries.items():
            with self.subTest(query=query):
                hits = search(query, self.catalog, limit=3)
                self.assertTrue(hits)
                self.assertEqual(hits[0].skill.name, expected)

    def test_identity_is_explicitly_opt_in_no_profile_bloat(self):
        for name in ("fullstack", "web-app", "minimal", "ui-ux-design", "cloud-engineering"):
            self.assertNotIn("authentication-solution-selection", load_profile(name, ROOT))
        self.assertIn("stack-advisor", load_profile("web-app", ROOT))
        self.assertIn("ui-library-selection", load_profile("web-app", ROOT))
        for path in (ROOT / "profiles").glob("*.yaml"):
            tokens, count = estimate(path.stem, ROOT)
            self.assertLessEqual(count, 20)
            self.assertLessEqual(tokens, 2500)

    def test_held_out_spec_is_not_real_agent_evidence(self):
        rows = yaml.safe_load((ROOT / "evals/stacks-routing.yaml").read_text())["scenarios"]
        self.assertGreaterEqual(len(rows), 10)
        self.assertEqual(len({r["id"] for r in rows}), len(rows))
        for row in rows:
            self.assertTrue(row["accept"])
            if "expected" in row:
                self.assertIn(row["expected"], self.catalog)
                self.assertIn(row["reference"],
                    indexed_references(self.catalog[row["expected"]], ROOT))
            else:
                for name in row["expected_not"]:
                    self.assertIn(name, self.catalog)

    def test_catalog_and_install_validation(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
