import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from install_profile import install


class InstallerSecurityTests(unittest.TestCase):
    def test_missing_project_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                install("minimal", "codex", Path(temp) / "does-not-exist", apply=True)

    def test_symlink_destination_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            outside = Path(temp) / "outside"
            project.mkdir()
            outside.mkdir()
            (project / ".agents").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                install("minimal", "codex", project, apply=True)
            self.assertEqual(list(outside.iterdir()), [])

    def test_symlinked_skill_input_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            project.mkdir()
            # Use an isolated toolkit copy with symlink-containing skill.
            fake = Path(temp) / "toolkit"
            source = fake / "skills" / "core" / "task-routing"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("test", encoding="utf-8")
            (source / "leak").symlink_to(project, target_is_directory=True)
            # Before reaching the profile-level copy, symlinks must be visible
            # to the direct safety scanner.
            from install_profile import _reject_symlinks
            with self.assertRaises(ValueError):
                _reject_symlinks(source)


if __name__ == "__main__":
    unittest.main()
