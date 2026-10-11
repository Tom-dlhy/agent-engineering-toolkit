"""UI V2: opt-in specialists with path-safe, selective deep references."""
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
from install_profile import planned_sources, install
from validate_skills import validate_repository


class UIExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = load_catalog(ROOT)
        cls.providers = {
            name for name, skill in cls.skills.items()
            if skill.domain == "ui" and name != "ui-component-research"
        }

    def test_exact_provider_count_and_deduplicated_selector(self):
        self.assertEqual(len(self.providers), 35)
        self.assertEqual(len(self.skills), 141)
        self.assertEqual(self.skills["ui-library-selection"].path,
                         "skills/stacks/ui-library-selection")

    def test_every_provider_has_two_real_local_leaves(self):
        for name in sorted(self.providers):
            with self.subTest(provider=name):
                refs = indexed_references(self.skills[name], ROOT)
                self.assertEqual(len(refs), 2)
                for path in refs:
                    text = read_reference(self.skills[name], path, ROOT)
                    self.assertGreater(len(text), 1700)
                    self.assertIn("Read when:", text[:300])
                    self.assertIn("https://", text)
                    self.assertIn("## ", text)

    def test_shared_component_research_is_targeted(self):
        refs = indexed_references(self.skills["ui-component-research"], ROOT)
        self.assertEqual(len(refs), 4)
        self.assertTrue(all(len(read_reference(self.skills["ui-component-research"], r, ROOT)) > 1600
                            for r in refs))
        self.assertEqual(len(indexed_references(self.skills["ui-library-selection"], ROOT)), 1)

    def test_provider_selection_and_negative_routing(self):
        cases = {
            "shadcn ui components.json registry": "shadcn-ui",
            "MUI DataGrid material sx": "mui",
            "radix primitives aschild": "radix-primitives",
            "base ui render headless": "base-ui",
            "vuetify v-data-table": "vuetify",
            "primeng p-table": "primeng",
            "bits ui svelte select": "bits-ui",
            "flutter cupertino navigation": "flutter-cupertino",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                matches = search(query, self.skills, limit=3)
                self.assertTrue(matches)
                self.assertEqual(matches[0].skill.name, expected)
        self.assertEqual(search("FastAPI Pydantic endpoint", self.skills, limit=1)[0].skill.name,
                         "fastapi-service")

    def test_provider_not_installed_by_default(self):
        self.assertNotIn("mui", load_profile("web-app", ROOT))
        self.assertNotIn("mui", load_profile("fullstack", ROOT))
        self.assertIn("shadcn-ui", load_profile("ui-shadcn", ROOT))
        self.assertLessEqual(len(load_profile("fullstack", ROOT)), 20)

    def test_reference_context_requires_explicit_activation(self):
        baseline, _ = estimate("ui-shadcn", ROOT)
        activated, _ = estimate("ui-shadcn", ROOT, ("shadcn-ui",))
        leaf, _ = estimate("ui-shadcn", ROOT, ("shadcn-ui",),
            ("shadcn-ui:references/component-patterns.md",))
        self.assertLess(baseline, activated)
        self.assertLess(activated, leaf)
        with self.assertRaises(ValueError):
            estimate("ui-shadcn", ROOT, (),
                ("shadcn-ui:references/component-patterns.md",))

    def test_single_vendor_install_copies_references(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            files = install(None, "codex", target, apply=True, skills=("mui",))
            self.assertEqual(len(files), 1)
            self.assertTrue((files[0] / "references" / "component-patterns.md").exists())
            self.assertEqual(len(planned_sources(None, skills=("mui", "mui"))), 1)

    def test_repository_validation(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
