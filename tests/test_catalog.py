import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from toolkit.catalog import load_catalog, load_profile, search, suggest_workflow, tokenize
from toolkit.cli import main


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)

    def test_casefold_and_french_accents(self):
        self.assertIn("securite", tokenize("La SÉCURITÉ d'une application"))

    def test_no_match_on_noise_or_empty_query(self):
        self.assertEqual(search("", self.catalog), [])
        self.assertEqual(search("zzzzxxxyyy", self.catalog), [])

    def test_rank_specific_cloud(self):
        found = search("audit AWS S3 permissions", self.catalog, limit=3)
        self.assertTrue(found)
        self.assertIn("aws", found[0].skill.name)

    def test_restrict_to_profile(self):
        allowed = load_profile("minimal", ROOT)
        matches = search("design cloud AWS", self.catalog, allowed=allowed)
        self.assertTrue(all(m.skill.name in allowed for m in matches))

    def test_free_text_workflow_abstains(self):
        for query in ("update documentation", "build backend API",
                      "migrate production database permissions"):
            self.assertEqual(suggest_workflow(query)[0], "unclassified")

    def test_cli_list_and_recommend(self):
        self.assertEqual(main(["--root", str(ROOT), "profiles"]), 0)
        self.assertEqual(main(["--root", str(ROOT), "recommend", "AWS IAM review"]), 0)


if __name__ == "__main__":
    unittest.main()
