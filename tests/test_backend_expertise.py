"""Backend refactor: source-based references and negative routing.

These checks validate catalog integrity, not real agent behavior or cloud access.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference
from context_budget import estimate
from validate_skills import validate_repository

BACKEND = {
    "modern-python": 6,
    "fastapi-service": 6,
    "python-http-clients": 5,
    "python-persistence": 5,
    "python-observability": 3,
    "background-jobs": 4,
    "typescript-api": 4,
}


class BackendExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.cases = yaml.safe_load((ROOT / "evals/backend-routing.yaml").read_text())

    def test_catalog_remains_148_and_backend_7(self):
        self.assertEqual(len(self.catalog), 171)
        self.assertEqual({v.name for v in self.catalog.values() if v.domain == "backend"},
                         set(BACKEND))

    def test_seven_skills_have_independently_triggered_deep_leaves(self):
        total = 0
        for name, number in BACKEND.items():
            with self.subTest(name=name):
                skill = self.catalog[name]
                self.assertIn("Use when", skill.description)
                self.assertIn("Do not", skill.description)
                refs = indexed_references(skill, ROOT)
                self.assertEqual(len(refs), number)
                for path in refs:
                    body = read_reference(skill, path, ROOT)
                    self.assertTrue(body.startswith("# "))
                    self.assertIn("Read when:", body[:500])
                    self.assertGreater(len(body), 1400)
                    self.assertIn("https://", body)
                    self.assertIn("## ", body)
                    total += 1
        self.assertEqual(total, 33)

    def test_no_maturity_labels(self):
        entries = yaml.safe_load((ROOT / "registry/skills.yaml").read_text())["skills"]
        self.assertFalse(any("maturity" in row for row in entries))

    def test_positive_routes(self):
        for case in self.cases["selection"]:
            with self.subTest(query=case["query"]):
                found = search(case["query"], self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, case["expected"])

    def test_negative_neighbor_routes(self):
        for case in self.cases["negative_neighbors"]:
            with self.subTest(query=case["query"]):
                found = search(case["query"], self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, case["expected"])

    def test_unmatched_not_forced(self):
        for phrase in self.cases["no_match"]:
            self.assertEqual(search(phrase, self.catalog), [])

    def test_refs_are_explicit_and_safe(self):
        skill = self.catalog["typescript-api"]
        good = "references/runtime-schema-and-security.md"
        self.assertIn(good, indexed_references(skill, ROOT))
        for invalid in ("../SKILL.md", "references/../../README.md",
                        "references/unknown.md"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                read_reference(skill, invalid, ROOT)
        base, _ = estimate("python-backend", ROOT)
        active, _ = estimate("python-backend", ROOT, ("fastapi-service",))
        expanded, _ = estimate("python-backend", ROOT, ("fastapi-service",),
                               ("fastapi-service:references/security-and-trust-boundaries.md",))
        self.assertLess(base, active)
        self.assertLess(active, expanded)
        self.assertLess(base, 2500)

    def test_no_typescript_auto_install_in_python_profile(self):
        self.assertNotIn("typescript-api", load_profile("python-backend", ROOT))
        self.assertNotIn("typescript-api", load_profile("minimal", ROOT))

    def test_primary_docs_and_caveats_in_audit(self):
        body = (ROOT / "docs/backend-refactor-audit.md").read_text()
        for word in ("HTTPX", "SQLAlchemy", "FastAPI", "Celery", "Node", "uv", "SOTA"):
            self.assertIn(word, body)

    def test_valid_repo(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
