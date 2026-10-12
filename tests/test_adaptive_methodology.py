"""Proportional review methodology: deterministic contracts, not model proof."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from toolkit.adaptive_policy import ChangeSignals, assess
from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference


class AdaptiveMethodologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = yaml.safe_load(
            (ROOT / "evals/adaptive-methodology.yaml").read_text(encoding="utf-8")
        )
        cls.catalog = load_catalog(ROOT)

    def test_policy_cases_are_explicitly_risk_aware(self):
        self.assertEqual(self.spec["status"], "unexecuted-host-behavior")
        seen = set()
        for item in self.spec["policy_cases"]:
            with self.subTest(item=item["id"]):
                self.assertNotIn(item["id"], seen)
                seen.add(item["id"])
                result = assess(ChangeSignals(**item["signals"]))
                expected = item["expected"]
                self.assertEqual(result.workflow, expected["workflow"])
                self.assertEqual(result.review, expected["review"])
                self.assertEqual(result.execution, expected["execution"])
                self.assertEqual(len(result.unmet_gates), expected["blockers"])
                self.assertTrue(result.rationale)

    def test_authority_and_unavailable_reviewer_are_distinct(self):
        d = assess(ChangeSignals(destructive_or_irreversible=True))
        self.assertFalse(d.ready_for_integration)
        self.assertEqual(len(d.unmet_gates), 2)
        d = assess(ChangeSignals(destructive_or_irreversible=True,
                                 destructive_authorized=True,
                                 reviewer_available=True))
        self.assertEqual(d.unmet_gates, ())
        self.assertEqual(d.review, "R2")  # still required even if authorized

    def test_policy_does_not_take_raw_text_as_evidence(self):
        with self.assertRaises(TypeError):
            assess("production deployment")
        with self.assertRaises(TypeError):
            assess(None)

    def test_routing_preserves_technical_neighbors(self):
        self.assertIn("implementation-planning", self.catalog)
        cases = (
            ("detailed implementation planning tasks dependency handoff", "implementation-planning"),
            ("FastAPI Pydantic endpoint", "fastapi-service"),
            ("AWS Bedrock Converse inference", "aws-bedrock"),
            ("debug traceback exception reproduce root cause", "systematic-debugging"),
            ("git pr branch merge ruleset review", "git-pr-workflow"),
        )
        for query, expected in cases:
            with self.subTest(query=query):
                self.assertEqual(search(query, self.catalog, limit=1)[0].skill.name,
                                 expected)

    def test_planning_is_opt_in_not_in_minimal(self):
        self.assertNotIn("implementation-planning", load_profile("minimal", ROOT))
        for profile in ("fullstack", "web-app", "python-backend", "devops"):
            self.assertIn("implementation-planning", load_profile(profile, ROOT))
        for persona in ("execution-orchestrator", "review-feedback-arbiter"):
            for profile in ("minimal", "fullstack", "web-app", "devops"):
                self.assertNotIn(persona, load_profile(profile, ROOT))

    def test_references_have_real_procedures_and_are_loaded_on_demand(self):
        expected = {
            "implementation-planning": 3,
            "task-routing": 3,
            "verification-before-done": 3,
            "git-pr-workflow": 6,
        }
        for name, minimum in expected.items():
            with self.subTest(skill=name):
                skill = self.catalog[name]
                refs = indexed_references(skill, ROOT)
                self.assertGreaterEqual(len(refs), minimum)
                for ref in refs:
                    leaf = read_reference(skill, ref, ROOT)
                    self.assertGreater(len(leaf), 1500)
                    self.assertIn("Read when:", leaf[:600])
                    self.assertIn("## ", leaf)
        for persona in ("execution-orchestrator", "review-feedback-arbiter"):
            self.assertEqual(indexed_references(self.catalog[persona], ROOT), ())

    def test_agents_workflows_and_host_eval_contracts(self):
        for workflow in ("light", "standard", "deep"):
            text = (ROOT / "workflows" / (workflow + ".md")).read_text()
            self.assertIn("## ", text)
            self.assertIn("R0" if workflow == "light" else ("R2" if workflow == "deep" else "R1"), text)
        for role in ("planner", "implementer", "reviewer"):
            text = (ROOT / "agents" / (role + ".md")).read_text()
            self.assertGreater(len(text), 1200)
        self.assertGreaterEqual(len(self.spec["behavioral_scenarios"]), 6)
        for case in self.spec["behavioral_scenarios"]:
            self.assertTrue(case["must"])
            self.assertTrue(case["must_not"])


if __name__ == "__main__":
    unittest.main()
