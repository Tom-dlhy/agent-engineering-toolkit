import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from context_budget import estimate
from toolkit.catalog import load_catalog, load_profile


class BudgetTests(unittest.TestCase):
    def test_all_profiles_keep_bounded_metadata(self):
        for file in sorted((ROOT / "profiles").glob("*.yaml")):
            with self.subTest(profile=file.stem):
                estimate_tokens, count = estimate(file.stem, ROOT)
                self.assertGreater(count, 0)
                self.assertLessEqual(count, 20)
                self.assertLessEqual(estimate_tokens, 2500)

    def test_full_body_only_if_activated(self):
        profile = "minimal"
        base, count = estimate(profile, ROOT)
        body, active_count = estimate(profile, ROOT, ("systematic-debugging",))
        self.assertEqual(count, active_count)
        self.assertGreater(body, base)

    def test_cannot_activate_skill_outside_profile(self):
        with self.assertRaises(ValueError):
            estimate("minimal", ROOT, ("terraform-iac",))

    def test_descriptions_are_distinct_and_brief(self):
        skills = load_catalog(ROOT)
        self.assertEqual(len(skills), 141)
        descriptions = [s.description for s in skills.values()]
        self.assertEqual(len(descriptions), len(set(descriptions)))
        self.assertTrue(all(35 <= len(d) <= 750 for d in descriptions))

    def test_profile_skill_members_are_unique(self):
        for path in sorted((ROOT / "profiles").glob("*.yaml")):
            skills = load_profile(path.stem, ROOT)
            self.assertEqual(len(skills), len(set(skills)))


if __name__ == "__main__":
    unittest.main()
