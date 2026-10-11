import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from install_profile import install


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


if __name__ == "__main__":
    unittest.main()
