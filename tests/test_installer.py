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

    def test_single_skill_and_references_are_installed(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            installed = install(None, "codex", project, apply=True, skills=("shadcn-ui",))
            self.assertEqual(len(installed), 1)
            self.assertTrue((installed[0] / "SKILL.md").is_file())

    def test_profile_and_skill_dedup(self):
        selected = planned_sources("ui-shadcn", skills=("shadcn-ui", "mui"))
        self.assertEqual([p.name for p in selected].count("shadcn-ui"), 1)
        self.assertEqual([p.name for p in selected].count("mui"), 1)

    def test_invalid_skill_does_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            for skill in ("../../root", "SHADCN", "unknown-skill"):
                with self.subTest(skill=skill):
                    with self.assertRaises(ValueError):
                        install(None, "codex", project, apply=True, skills=(skill,))
            self.assertFalse((project / ".agents").exists())


if __name__ == "__main__":
    unittest.main()
