"""Design refactor: deterministic checks only; agent/browser evaluations are separate."""
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


REFS = {
    "accessibility-wcag": (
        "references/wcag22-audit-and-triage.md",
        "references/accessible-interaction-contracts.md",
        "references/manual-a11y-verification.md",
    ),
    "dark-mode-theming": (
        "references/theme-state-and-tokens.md",
        "references/theme-contrast-and-assets.md",
    ),
    "landing-page-design": (
        "references/narrative-and-evidence.md",
        "references/conversion-and-verification.md",
    ),
    "responsive-visual-qa": (
        "references/viewport-and-state-matrix.md",
        "references/screenshot-baselines-and-triage.md",
    ),
    "bento-grid": ("references/semantic-responsive-bento.md",),
    "glassmorphism": ("references/translucency-fallback-and-qa.md",),
}


class DesignRefactorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.design = {name: skill for name, skill in cls.catalog.items()
                      if skill.domain == "design"}

    def test_all_twelve_existing_skills_and_catalog_preserved(self):
        self.assertEqual(len(self.catalog), 151)
        self.assertEqual(len(self.design), 16)
        self.assertTrue(set(REFS).issubset(self.design))
        self.assertIn("frontend-design", self.design)
        self.assertIn("design-system", self.design)
        self.assertIn("ux-audit", self.design)

    def test_technical_leaves_are_present_and_explicitly_selected(self):
        total = 0
        for name, expected in REFS.items():
            with self.subTest(skill=name):
                skill = self.catalog[name]
                refs = indexed_references(skill, ROOT)
                self.assertEqual(refs, expected)
                for ref in refs:
                    text = read_reference(skill, ref, ROOT)
                    self.assertTrue(text.startswith("# "))
                    self.assertIn("Read when:", text[:450])
                    self.assertIn("## ", text)
                    self.assertIn("https://", text)
                    self.assertGreater(len(text), 1200, (name, ref))
                    total += 1
        self.assertEqual(total, 11)

    def test_design_full_reference_count_and_read_is_path_safe(self):
        self.assertEqual(sum(len(indexed_references(skill, ROOT))
                             for skill in self.design.values()), 38)
        for text in ("../SKILL.md", "references/../SKILL.md",
                     "references/nope.md", "SKILL.md"):
            with self.subTest(path=text), self.assertRaises(ValueError):
                read_reference(self.design["accessibility-wcag"], text, ROOT)

    def test_style_effects_are_explicit_opt_in_not_default_profile(self):
        general = load_profile("ui-ux-design", ROOT)
        self.assertNotIn("bento-grid", general)
        self.assertNotIn("glassmorphism", general)
        self.assertIn("frontend-design", general)
        self.assertIn("accessibility-wcag", general)
        self.assertIn("dark-mode-theming", general)
        self.assertIn("bento-grid", self.catalog)
        self.assertIn("glassmorphism", self.catalog)
        self.assertLessEqual(estimate("ui-ux-design", ROOT)[0], 2500)

    def test_specific_routing_matches_dedicated_skills(self):
        cases = {
            "WCAG accessibility keyboard screenreader focus": "accessibility-wcag",
            "dark mode theme hydration system": "dark-mode-theming",
            "responsive visual qa screenshots viewport": "responsive-visual-qa",
            "landing page conversion cta": "landing-page-design",
            "bento grid tile spans": "bento-grid",
            "frosted glass backdrop blur": "glassmorphism",
            "FastAPI Pydantic endpoint": "fastapi-service",
            "/anti-ai-slop": "frontend-design",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                found = search(query, self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, expected)

    def test_behavioral_scenarios_exist_but_are_not_claimed_executed(self):
        src = yaml.safe_load((ROOT / "evals/design-routing.yaml").read_text())
        scenarios = src["scenarios"]
        self.assertGreaterEqual(len(scenarios), 8)
        self.assertEqual(len({case["id"] for case in scenarios}), len(scenarios))
        for case in scenarios:
            self.assertIn("acceptance", case)
            if "expected" in case:
                self.assertIn(case["expected"], self.catalog)
                if "leaf" in case:
                    self.assertIn(case["leaf"],
                                  indexed_references(self.catalog[case["expected"]], ROOT))
            else:
                self.assertIn("expected_not", case)

    def test_source_contracts_do_not_overpromise_conformance(self):
        a11y = read_reference(self.design["accessibility-wcag"],
                              REFS["accessibility-wcag"][0], ROOT)
        self.assertIn("2.4.11", a11y)
        self.assertIn("2.4.13", a11y)
        self.assertIn("AAA", a11y)
        self.assertIn("24x24", a11y)
        glass = read_reference(self.design["glassmorphism"],
                               REFS["glassmorphism"][0], ROOT)
        self.assertIn("prefers-reduced-transparency", glass)
        self.assertIn("not universally supported", glass)

    def test_static_repository_validation(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
