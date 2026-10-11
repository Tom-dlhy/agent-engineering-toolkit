"""Growth source and routing contracts. Static tests do not measure real rankings or campaigns."""
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

GROWTH = {
    "technical-seo": 4,
    "content-strategy": 4,
    "ai-search-visibility": 4,
    "growth-experimentation": 3,
    "lifecycle-retention": 3,
}


class GrowthExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.growth = {name: s for name, s in cls.catalog.items() if s.domain == "growth"}

    def test_exact_catalog_and_no_duplicate_growth_responsibility(self):
        self.assertEqual(len(self.catalog), 166)
        self.assertEqual(set(self.growth), set(GROWTH))
        self.assertEqual(sum(len(indexed_references(s, ROOT)) for s in self.growth.values()), 18)
        for adjacent in ("analytics-modeling", "landing-page-design", "technical-seo",
                         "content-design", "llm-evaluation", "ui-component-research"):
            self.assertIn(adjacent, self.catalog)

    def test_every_growth_reference_is_selective_and_substantial(self):
        for name, count in GROWTH.items():
            with self.subTest(skill=name):
                s = self.growth[name]
                body = (ROOT / s.path / "SKILL.md").read_text()
                self.assertIn("Use when", s.description)
                self.assertIn("Do not", s.description)
                self.assertIn("## ", body)
                refs = indexed_references(s, ROOT)
                self.assertEqual(len(refs), count)
                for ref in refs:
                    content = read_reference(s, ref, ROOT)
                    self.assertTrue(content.startswith("# "))
                    self.assertIn("Read when:", content[:550])
                    self.assertIn("## ", content)
                    self.assertIn("https://", content)
                    self.assertGreater(len(content), 1600, (name, ref))
                for invalid in ("../SKILL.md", "SKILL.md", "references/no.md",
                                "references/../SKILL.md"):
                    with self.assertRaises(ValueError):
                        read_reference(s, invalid, ROOT)

    def test_positive_and_negative_provider_routing(self):
        queries = {
            "SEO canonical robots sitemap index crawl": "technical-seo",
            "technical SEO JavaScript SSR rendering robots canonical": "technical-seo",
            "editorial content strategy calendar topic planning": "content-strategy",
            "AI search citations GEO attribution visibility": "ai-search-visibility",
            "growth experiment abtest randomization srm guardrail": "growth-experimentation",
            "lifecycle retention reengagement unsubscribe suppression": "lifecycle-retention",
            "FastAPI Pydantic endpoint": "fastapi-service",
            "shadcn UI components.json registry": "shadcn-ui",
            "bento grid tile spans": "bento-grid",
            "dbt analytics mart star schema": "analytics-modeling",
        }
        for query, expected in queries.items():
            with self.subTest(query=query):
                match = search(query, self.catalog, limit=3)
                self.assertTrue(match, query)
                self.assertEqual(match[0].skill.name, expected)

    def test_opt_in_profiles_and_budget(self):
        profile = load_profile("growth-marketing", ROOT)
        self.assertEqual(len(profile), len(set(profile)))
        self.assertTrue(set(GROWTH).issubset(profile))
        for profile_name in ("web-app", "minimal", "ui-ux-design"):
            self.assertNotIn("lifecycle-retention", load_profile(profile_name, ROOT))
            self.assertNotIn("growth-experimentation", load_profile(profile_name, ROOT))
        baseline, _ = estimate("growth-marketing", ROOT)
        active, _ = estimate("growth-marketing", ROOT, ("growth-experimentation",))
        leaf, _ = estimate("growth-marketing", ROOT, ("growth-experimentation",),
                           ("growth-experimentation:references/experiment-diagnostics-and-decisions.md",))
        self.assertLess(baseline, active)
        self.assertLess(active, leaf)
        self.assertLessEqual(baseline, 2500)

    def test_no_invented_google_ai_seo_requirements(self):
        leaf = read_reference(self.growth["ai-search-visibility"],
            "references/engine-boundaries-and-policies.md", ROOT).lower()
        self.assertIn("no", leaf)
        self.assertIn("llms.txt", leaf)
        self.assertIn("https://developers.google.com/search/docs/appearance/ai-features", leaf)
        srm = read_reference(self.growth["growth-experimentation"],
            "references/experiment-diagnostics-and-decisions.md", ROOT)
        self.assertIn("SRM", srm)
        self.assertIn("peeking", srm.lower())
        permissions = read_reference(self.growth["lifecycle-retention"],
            "references/permission-and-deliverability.md", ROOT)
        self.assertIn("CNIL", permissions)
        self.assertIn("ICO", permissions)
        self.assertIn("unsubscribe", permissions.lower())

    def test_manual_evals_are_specified_not_claimed_completed(self):
        fixture = yaml.safe_load((ROOT / "evals/growth-routing.yaml").read_text())
        cases = fixture["scenarios"]
        self.assertGreaterEqual(len(cases), 12)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        for case in cases:
            self.assertTrue(case["must"])
            if "expected" in case:
                self.assertIn(case["expected"], self.catalog)
                self.assertIn(case["leaf"],
                    indexed_references(self.catalog[case["expected"]], ROOT))
            else:
                for name in case["expected_not"]:
                    self.assertIn(name, self.catalog)

    def test_repo_integrity(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
