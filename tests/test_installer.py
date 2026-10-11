import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from install_profile import install, planned_sources


class InstallerTests(unittest.TestCase):
    def test_default_is_dry_run(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            result = install("minimal", "codex", project)
            self.assertTrue(result)
            self.assertFalse((project / ".agents").exists())

    def test_installs_claude_skills_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            result = install("minimal", "claude", project, apply=True)
            self.assertTrue(all((p / "SKILL.md").exists() for p in result))
            with self.assertRaises(FileExistsError):
                install("minimal", "claude", project, apply=True)

    def test_rejects_unknown_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                install("missing", "codex", Path(temp))

    def test_can_install_explicit_provider_without_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            planned = install(None, "codex", project, skills=["shadcn-ui", "ui-component-research"])
            self.assertEqual([p.name for p in planned], ["shadcn-ui", "ui-component-research"])
            self.assertFalse((project / ".agents").exists())

    def test_profile_and_extra_skill_deduplicate(self):
        result = planned_sources("web-app", ROOT, ["ui-library-selection", "mantine"])
        self.assertEqual(sum(p.name == "ui-library-selection" for p in result), 1)
        self.assertIn("mantine", [p.name for p in result])

    def test_unknown_skill_rejected(self):
        with self.assertRaises(ValueError):
            planned_sources(None, ROOT, ["does-not-exist"])

    def test_no_profile_traversal(self):
        with self.assertRaises(ValueError):
            planned_sources("../private", ROOT)


if __name__ == "__main__":
    unittest.main()
