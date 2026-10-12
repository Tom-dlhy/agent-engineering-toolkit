"""Focused tests for V2 design craft, growth and safe external skill discovery."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference
from context_budget import estimate
from install_profile import install
from validate_skills import validate_repository


class DesignGrowthV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.new_skills = (
            "requirements-discovery",
            "brand-identity-visualization",
            "content-strategy",
            "technical-seo",
            "ai-search-visibility",
        )
        cls.extended = (
            "interaction-motion",
            "frontend-design",
            "ux-audit",
            "design-system",
            "typography-layout",
            "external-skill-audit",
        )

    def test_catalog_and_existing_provider_are_preserved(self):
        self.assertEqual(len(self.catalog), 178)
        self.assertEqual(self.catalog["requirements-discovery"].domain, "core")
        self.assertEqual(self.catalog["technical-seo"].domain, "growth")
        self.assertEqual(self.catalog["ui-library-selection"].path, "skills/stacks/ui-library-selection")
        self.assertEqual(self.catalog["shadcn-ui"].path, "skills/ui/shadcn-ui")
        self.assertIn("aws-bedrock", self.catalog)

    def test_deep_refs_are_locally_indexed_and_targeted(self):
        for name in self.new_skills + self.extended:
            with self.subTest(skill=name):
                skill = self.catalog[name]
                refs = indexed_references(skill, ROOT)
                minimum = 4 if name == "interaction-motion" else 2
                self.assertGreaterEqual(len(refs), minimum)
                for path in refs:
                    leaf = read_reference(skill, path, ROOT)
                    self.assertTrue(leaf.startswith("# "))
                    self.assertIn("Read when:", leaf[:500])
                    self.assertIn("## ", leaf)
                    self.assertIn("https://", leaf)
                    self.assertGreater(len(leaf), 1200)

    def test_reference_read_rejects_unlisted_paths(self):
        skill = self.catalog["technical-seo"]
        for path in ("../SKILL.md", "references/../SKILL.md", "references/unknown.md", "SKILL.md"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                read_reference(skill, path, ROOT)

    def test_specialists_are_not_mistaken_for_other_tasks(self):
        cases = {
            "SEO canonical robots sitemap index crawl": "technical-seo",
            "AI search citations GEO attribution visibility": "ai-search-visibility",
            "editorial content strategy calendar topic planning": "content-strategy",
            "brand identity logo board visualization": "brand-identity-visualization",
            "grill requirements discovery clarify ambiguous specification": "requirements-discovery",
            "animation motion easing transitions": "interaction-motion",
            "find external skills import provenance audit": "external-skill-audit",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                matches = search(query, self.catalog, limit=3)
                self.assertTrue(matches, query)
                self.assertEqual(matches[0].skill.name, expected)
        self.assertEqual(search("FastAPI Pydantic endpoint", self.catalog, limit=1)[0].skill.name,
                         "fastapi-service")

    def test_exact_requested_shortcut_intents(self):
        aliases = {
            "/seo": "technical-seo",
            "/ai-seo": "ai-search-visibility",
            "/content-strategy": "content-strategy",
            "/grill-me": "grill-master",
            "/anti-ai-slop": "frontend-design",
            "/find-skills": "external-skill-audit",
        }
        for query, expected in aliases.items():
            with self.subTest(query=query):
                matches = search(query, self.catalog, limit=3)
                self.assertTrue(matches)
                self.assertEqual(matches[0].skill.name, expected)

    def test_only_explicit_profiles_include_growth_or_brand_artifact(self):
        self.assertNotIn("technical-seo", load_profile("minimal", ROOT))
        self.assertNotIn("brand-identity-visualization", load_profile("web-app", ROOT))
        self.assertIn("ai-search-visibility", load_profile("growth-marketing", ROOT))
        self.assertIn("interaction-motion", load_profile("design-craft", ROOT))
        self.assertLessEqual(len(load_profile("design-craft", ROOT)), 20)
        self.assertLessEqual(len(load_profile("growth-marketing", ROOT)), 20)

    def test_context_is_incremental_only_after_reference_selected(self):
        base, _ = estimate("design-craft", ROOT)
        active, _ = estimate("design-craft", ROOT, ("interaction-motion",))
        leaf, _ = estimate("design-craft", ROOT, ("interaction-motion",),
                           ("interaction-motion:references/motion-decisions.md",))
        self.assertLess(base, active)
        self.assertLess(active, leaf)
        with self.assertRaises(ValueError):
            estimate("design-craft", ROOT, (), ("interaction-motion:references/motion-decisions.md",))

    def test_opt_in_install_contains_deep_references(self):
        with tempfile.TemporaryDirectory() as d:
            dst = Path(d)
            paths = install(None, "codex", dst, apply=True, skills=("technical-seo",))
            self.assertEqual(len(paths), 1)
            self.assertTrue((paths[0] / "references" / "crawl-index-and-routing.md").is_file())
            self.assertFalse((dst / ".claude").exists())
            with self.assertRaises(FileExistsError):
                install(None, "codex", dst, apply=True, skills=("technical-seo",))

    def test_intake_is_reference_only(self):
        doc = (ROOT / "docs" / "design-growth-source-review.md").read_text()
        self.assertIn("No scripts", doc)
        self.assertIn("Caveman", doc)
        self.assertIn("EXTEND", doc)
        for skill_name in self.new_skills:
            path = ROOT / self.catalog[skill_name].path
            self.assertEqual(list(path.rglob("*.py")), [])

    def test_static_validation(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
