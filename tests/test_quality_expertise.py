"""Quality category refactor: reference safety, lexical routing, uniform standard."""
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

EXPECTED = {
    "test-strategy", "secure-code-review", "dependency-supply-chain",
    "performance-profiling", "release-readiness", "git-pr-workflow",
    "external-skill-audit",
}


class QualityRefactorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.fixtures = yaml.safe_load(
            (ROOT / "evals" / "quality-routing.yaml").read_text(encoding="utf-8")
        )

    def test_exactly_seven_quality_skills(self):
        self.assertEqual(
            {s.name for s in self.catalog.values() if s.domain == "quality"},
            EXPECTED,
        )
        self.assertEqual(len(self.catalog), 119)

    def test_uniform_quality_without_maturity_tiers(self):
        entries = yaml.safe_load((ROOT / "registry" / "skills.yaml").read_text())["skills"]
        self.assertEqual(len(entries), 119)
        self.assertFalse(any("maturity" in e for e in entries))

    def test_references_have_real_content_and_selective_triggers(self):
        count = 0
        for name in EXPECTED:
            skill = self.catalog[name]
            with self.subTest(name=name):
                self.assertIn("Use when", skill.description)
                self.assertIn("Do not", skill.description)
                self.assertIn("## ", (ROOT / skill.path / "SKILL.md").read_text())
                refs = indexed_references(skill, ROOT)
                self.assertEqual(len(refs), 3)
                for path in refs:
                    leaf = read_reference(skill, path, ROOT)
                    self.assertGreater(len(leaf), 1400, (name, path))
                    self.assertTrue(leaf.startswith("# "))
                    self.assertIn("Read when:", leaf[:600])
                    self.assertIn("## ", leaf)
                    self.assertIn("https://", leaf)
                    count += 1
        self.assertEqual(count, 21)

    def test_positive_routing(self):
        for item in self.fixtures["selection"]:
            with self.subTest(query=item["query"]):
                found = search(item["query"], self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, item["expected"])

    def test_negative_neighbour_routing(self):
        for item in self.fixtures["negative_neighbors"]:
            with self.subTest(query=item["query"]):
                found = search(item["query"], self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, item["expected"])

    def test_nonsense_or_empty_does_not_activate(self):
        for query in self.fixtures["no_match"]:
            self.assertEqual(search(query, self.catalog), [])

    def test_reference_traversal_and_context_budget(self):
        skill = self.catalog["test-strategy"]
        self.assertIn(
            "references/risk-matrix-and-test-design.md", indexed_references(skill, ROOT)
        )
        for invalid in ("../SKILL.md", "references/../../AGENTS.md",
                        "references/not-listed.md"):
            with self.subTest(path=invalid), self.assertRaises(ValueError):
                read_reference(skill, invalid, ROOT)
        minimal = load_profile("minimal", ROOT)
        self.assertIn("test-strategy", minimal)
        self.assertNotIn("dependency-supply-chain", minimal)
        base, _ = estimate("minimal", ROOT)
        active, _ = estimate("minimal", ROOT, ("test-strategy",))
        leaf, _ = estimate(
            "minimal", ROOT, ("test-strategy",),
            ("test-strategy:references/risk-matrix-and-test-design.md",),
        )
        self.assertLessEqual(base, 2500)
        self.assertLess(base, active)
        self.assertLess(active, leaf)
        with self.assertRaises(ValueError):
            estimate(
                "minimal", ROOT, (),
                ("test-strategy:references/risk-matrix-and-test-design.md",),
            )

    def test_source_audit(self):
        text = (ROOT / "docs" / "quality-refactor-audit.md").read_text()
        for phrase in ("OWASP", "pytest", "SLSA", "GitHub", "k6", "NIST"):
            self.assertIn(phrase, text)

    def test_no_executable_imports_in_quality_skills(self):
        for name in EXPECTED:
            self.assertEqual(list((ROOT / self.catalog[name].path).rglob("*.py")), [])

    def test_repo_structure_still_valid(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
