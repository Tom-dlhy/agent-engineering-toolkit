import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from context_budget import estimate
from install_profile import planned_sources
from validate_skills import validate_repository


class RepositoryTests(unittest.TestCase):
    def test_manifest_and_profiles(self):
        self.assertEqual(validate_repository(ROOT), [])

    def test_minimal_context_proxy_is_bounded(self):
        size, count = estimate("minimal", ROOT)
        self.assertLessEqual(count, 6)
        self.assertGreater(size, 0)
        self.assertLessEqual(size, 2500)

    def test_profiles_have_at_most_twenty_skills(self):
        for p in sorted((ROOT / "profiles").glob("*.yaml")):
            with self.subTest(name=p.stem):
                self.assertLessEqual(len(planned_sources(p.stem)), 20)


if __name__ == "__main__":
    unittest.main()
