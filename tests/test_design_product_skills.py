"""Provider-neutral Design specialists: static safety/routing contracts, not user studies."""
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

NEW = {
    "data-visualization-design": 3,
    "interaction-flow-design": 3,
    "information-architecture": 3,
    "content-design": 3,
}


class DesignProductSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)

    def test_catalog_size_and_independent_owners(self):
        self.assertEqual(len(self.catalog), 150)
        design = {n: s for n, s in self.catalog.items() if s.domain == "design"}
        self.assertEqual(len(design), 16)
        self.assertEqual(set(NEW) & set(design), set(NEW))
        self.assertEqual(sum(len(indexed_references(s, ROOT)) for s in design.values()), 38)
        self.assertIn("shadcn-ui", self.catalog)
        self.assertIn("base-ui", self.catalog)
        self.assertIn("ui-library-selection", self.catalog)
        self.assertIn("analytics-modeling", self.catalog)

    def test_deep_local_leaves_are_explicit_and_not_generic_empty_links(self):
        for name, size in NEW.items():
            with self.subTest(name=name):
                skill = self.catalog[name]
                refs = indexed_references(skill, ROOT)
                self.assertEqual(len(refs), size)
                body = (ROOT / skill.path / "SKILL.md").read_text()
                self.assertIn("## ", body)
                for ref in refs:
                    leaf = read_reference(skill, ref, ROOT)
                    self.assertTrue(leaf.startswith("# "))
                    self.assertIn("Read when:", leaf[:350])
                    self.assertIn("## ", leaf)
                    self.assertIn("https://", leaf)
                    self.assertGreater(len(leaf), 900)
                for bad in ("../SKILL.md", "SKILL.md", "references/nope.md"):
                    with self.assertRaises(ValueError):
                        read_reference(skill, bad, ROOT)

    def test_provider_first_contract_does_not_invent_chart_engines(self):
        p = self.catalog["data-visualization-design"]
        body = (ROOT / p.path / "SKILL.md").read_text()
        handoff = read_reference(p, "references/provider-reuse-and-accessibility.md", ROOT)
        for term in ("analytics-modeling", "shadcn-ui", "ui/base-ui", "ui/mui",
                     "ui-library-selection", "Recharts", "provider"):
            self.assertIn(term, body + handoff)
        for term in ("@base-ui/react", "not a guaranteed chart", "Do not",
                     "Reuse the same chart package", "https://ui.shadcn.com",
                     "https://mui.com/x/react-charts"):
            self.assertIn(term, handoff)
        self.assertNotIn("npm install ", body)

    def test_selective_profiles_and_context(self):
        general = load_profile("ui-ux-design", ROOT)
        self.assertTrue({"content-design", "interaction-flow-design",
                         "information-architecture"}.issubset(general))
        self.assertNotIn("data-visualization-design", general)
        self.assertNotIn("data-visualization-design", load_profile("web-app", ROOT))
        self.assertIn("content-design", load_profile("product-launch", ROOT))
        self.assertLessEqual(estimate("ui-ux-design", ROOT)[0], 2500)
        self.assertLessEqual(estimate("product-launch", ROOT)[0], 2500)

    def test_positive_route_and_provider_negative_examples(self):
        cases = {
            "chart dashboard axes visualization": "data-visualization-design",
            "multi step onboarding user flow recovery": "interaction-flow-design",
            "taxonomy navigation information architecture": "information-architecture",
            "microcopy labels errors terminology": "content-design",
            "shadcn ui components.json registry": "shadcn-ui",
            "shadcn Chart tooltip Recharts": "shadcn-ui",
            "MUI X Charts implementation": "mui",
            "Base UI Dialog render": "base-ui",
            "dbt analytics mart star schema": "analytics-modeling",
            "FastAPI Pydantic endpoint": "fastapi-service",
            "frosted glass backdrop blur": "glassmorphism",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                hits = search(query, self.catalog, limit=3)
                self.assertTrue(hits, query)
                self.assertEqual(hits[0].skill.name, expected)

    def test_behavioral_cases_are_evaluation_plan_not_results(self):
        cases = yaml.safe_load((ROOT / "evals/design-product-routing.yaml").read_text())["scenarios"]
        self.assertGreaterEqual(len(cases), 8)
        self.assertEqual(len({row["id"] for row in cases}), len(cases))
        for case in cases:
            self.assertIn("accept", case)
            for ref in case.get("references", []):
                self.assertIn(ref, indexed_references(self.catalog[case["expected"]], ROOT))
            for expected in case.get("expected_not", []):
                self.assertIn(expected, self.catalog)

    def test_catalog_and_profile_integrity(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
