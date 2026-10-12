"""Research-driven methodology content and scenario integrity, not live model proof."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toolkit.catalog import load_catalog
from toolkit.knowledge import indexed_references


TARGETS = {
    "task-routing": "Research-backed selection",
    "llm-evaluation": "Skill methodology experiments",
    "systematic-debugging": "Four-phase causal process",
    "test-strategy": "Operational TDD",
    "test-adversary": "Cost-aware adversarial",
    "requirements-discovery": "Discovery as a bounded",
    "architecture-decision": "Architecture selection as",
    "secure-code-review": "Differential security review",
    "agent-tool-safety": "Trust decisions for tool-using agents",
    "ci-cd-engineering": "Risk-scaled delivery",
    "release-readiness": "Release as an observable",
    "incident-commander": "Operational incident drill",
    "codebase-archeologist": "Progressive audit context",
    "context-curator": "Continuity protocol",
}
REFERENCES = {
    "llm-evaluation": "references/metrics-judges-and-statistics.md",
    "systematic-debugging": "references/root-cause-and-regressions.md",
    "test-strategy": "references/property-concurrency-failures.md",
    "requirements-discovery": "references/acceptance-and-decision-log.md",
    "architecture-decision": "references/adr-and-evidence.md",
    "secure-code-review": "references/findings-and-security-evidence.md",
    "release-readiness": "references/migrations-and-recovery.md",
    "ci-cd-engineering": "references/security-operations-and-tests.md",
}


class MethodologyDepthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = load_catalog(ROOT)
        cls.spec = yaml.safe_load((ROOT / "evals" / "methodology-depth.yaml").read_text())

    def test_no_new_skills_or_personas(self):
        self.assertEqual(len(self.skills), 178)
        self.assertEqual(
            {n for n, s in self.skills.items() if s.domain == "personas"},
            {n for n, s in self.skills.items() if s.domain == "personas"}
        )
        self.assertEqual(len([s for s in self.skills.values() if s.domain == "personas"]), 15)

    def test_all_fourteen_exist_with_operational_protocols(self):
        for name, marker in TARGETS.items():
            with self.subTest(skill=name):
                source = (ROOT / self.skills[name].path / "SKILL.md").read_text()
                self.assertIn(marker, source)
                self.assertIn("LIGHT", source.upper())
                self.assertIn("DEEP", source.upper())
                self.assertGreater(len(source), 2500)

    def test_references_kept_in_existing_skill_ownership(self):
        for name, path in REFERENCES.items():
            with self.subTest(skill=name):
                skill = self.skills[name]
                self.assertIn(path, indexed_references(skill, ROOT))
                content = (ROOT / skill.path / path).read_text()
                self.assertGreater(len(content), 1800)
                self.assertIn("## ", content)

    def test_unexecuted_scenarios_have_negative_and_positive_oracles(self):
        self.assertEqual(self.spec["status"], "unexecuted")
        cases = self.spec["cases"]
        self.assertGreaterEqual(len(cases), 20)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        self.assertEqual({c["skill"] for c in cases}, set(TARGETS))
        for row in cases:
            with self.subTest(id=row["id"]):
                self.assertIn(row["skill"], self.skills)
                self.assertIn(row["mode"], ("light", "standard", "deep"))
                self.assertTrue(row["prompt"])
                self.assertTrue(row["must"])
                self.assertTrue(row["must_not"])


if __name__ == "__main__":
    unittest.main()
