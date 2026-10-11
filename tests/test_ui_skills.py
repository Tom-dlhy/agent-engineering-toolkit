"""Verify the UI catalog is comprehensive, narrowly routed and installed on demand."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "skills" / "ui"


class UISkillsTests(unittest.TestCase):
    def test_ui_provider_skill_coverage(self):
        catalog = yaml.safe_load((ROOT / "registry" / "skills.yaml").read_text(encoding="utf-8"))
        ui_skills = [entry for entry in catalog["skills"] if entry["domain"] == "ui"]
        providers = [entry for entry in ui_skills if entry["name"] not in {"ui-library-selection", "ui-component-research"}]
        self.assertEqual(len(providers), 35)
        self.assertEqual(len({entry["name"] for entry in ui_skills}), 37)
        for entry in providers:
            text = (ROOT / entry["path"] / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("**Official documentation:** https://", text)
            self.assertIn("version-compatible official docs", text)
            self.assertIn("Component specialties", text)

    def test_default_profiles_do_not_eager_install_every_provider(self):
        for name in ("web-app", "fullstack"):
            profile = yaml.safe_load((ROOT / "profiles" / f"{name}.yaml").read_text(encoding="utf-8"))
            self.assertIn("ui-library-selection", profile["skills"])
            self.assertIn("ui-component-research", profile["skills"])
            self.assertNotIn("shadcn-ui", profile["skills"])
            self.assertNotIn("mui", profile["skills"])

    def test_shadcn_profile_is_narrow(self):
        profile = yaml.safe_load((ROOT / "profiles" / "ui-shadcn.yaml").read_text(encoding="utf-8"))
        self.assertIn("shadcn-ui", profile["skills"])
        self.assertNotIn("mui", profile["skills"])

    def test_component_references_available(self):
        files = sorted((UI_DIR / "ui-component-research" / "references").glob("*.md"))
        self.assertGreaterEqual(len(files), 4)


if __name__ == "__main__":
    unittest.main()
