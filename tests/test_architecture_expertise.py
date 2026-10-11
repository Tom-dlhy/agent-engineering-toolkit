"""Architecture research refactor: one standard, targeted references and routing.

Lexical tests are advisory only; real agent choice requires held-out host evals.
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

ARCH = {
    "api-contract-design", "architecture-decision",
    "event-driven-design", "hexagonal-architecture",
    "modular-monolith", "python-project-architecture",
    "python-ddd", "technology-tradeoffs",
}


class ArchitectureRefactorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.fixtures = yaml.safe_load(
            (ROOT / "evals/architecture-routing.yaml").read_text(encoding="utf-8")
        )

    def test_eight_independent_architecture_skills(self):
        self.assertEqual(
            {x.name for x in self.catalog.values() if x.domain == "architecture"}, ARCH
        )
        self.assertEqual(len(self.catalog), 148)

    def test_one_uniform_contract_no_maturity(self):
        reg = yaml.safe_load((ROOT / "registry/skills.yaml").read_text())
        self.assertFalse(any("maturity" in entry for entry in reg["skills"]))

    def test_all_eight_have_three_selectively_readable_references(self):
        count = 0
        for name in sorted(ARCH):
            with self.subTest(name=name):
                skill = self.catalog[name]
                self.assertIn("Use when", skill.description)
                self.assertIn("Do not", skill.description)
                content = (ROOT / skill.path / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("## ", content)
                refs = indexed_references(skill, ROOT)
                self.assertEqual(len(refs), 3)
                for ref in refs:
                    data = read_reference(skill, ref, ROOT)
                    self.assertGreater(len(data), 1400, (name, ref))
                    self.assertTrue(data.startswith("# "))
                    self.assertIn("Read when:", data[:600])
                    self.assertIn("## ", data)
                    self.assertIn("https://", data)
                    count += 1
        self.assertEqual(count, 24)

    def test_positive_specific_routing(self):
        for item in self.fixtures["selection"]:
            with self.subTest(query=item["query"]):
                found = search(item["query"], self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, item["expected"])

    def test_negative_interdomain_routing(self):
        for item in self.fixtures["negative_neighbors"]:
            with self.subTest(query=item["query"]):
                found = search(item["query"], self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, item["expected"])

    def test_no_match_does_not_force_activation(self):
        for query in self.fixtures["no_match"]:
            self.assertEqual(search(query, self.catalog), [])

    def test_opt_in_reference_loading_and_path_rejection(self):
        name = "event-driven-design"
        ref = "references/outbox-inbox-and-idempotency.md"
        skill = self.catalog[name]
        self.assertIn(ref, indexed_references(skill, ROOT))
        self.assertGreater(len(read_reference(skill, ref, ROOT)), 1600)
        for path in ("../SKILL.md", "references/../../README.md",
                     "references/unlisted.md"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                read_reference(skill, path, ROOT)
        allowed = load_profile("python-backend", ROOT)
        self.assertIn("python-project-architecture", allowed)
        self.assertIn("api-contract-design", allowed)
        base, _ = estimate("python-backend", ROOT)
        active, _ = estimate("python-backend", ROOT, ("api-contract-design",))
        leaf, _ = estimate(
            "python-backend", ROOT, ("api-contract-design",),
            ("api-contract-design:references/http-contracts-and-errors.md",)
        )
        self.assertLess(base, active)
        self.assertLess(active, leaf)
        self.assertLessEqual(base, 2500)

    def test_official_research_and_limitations_documented(self):
        text = (ROOT / "docs/architecture-refactor-audit.md").read_text()
        for phrase in ("RFC 9457", "OpenAPI 3.2", "AsyncAPI",
                       "AWS", "Microsoft", "SLO", "ADR", "SOTA"):
            self.assertIn(phrase, text)

    def test_repository_integrity(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
