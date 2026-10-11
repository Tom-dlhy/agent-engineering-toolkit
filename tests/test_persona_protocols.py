"""Personas: self-contained opt-in methods, negative routing and safe installation.

These deterministic checks prove source and routing contracts, NOT model behavior.
Live agent adherence must be established with held-out conversations separately.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference
from install_profile import install, planned_sources
from context_budget import estimate
from validate_skills import validate_repository

PERSONAS = (
    "grill-master",
    "devils-advocate",
    "codebase-archeologist",
    "scope-guardian",
    "test-adversary",
    "execution-orchestrator",
    "product-sparring-partner",
    "review-feedback-arbiter",
    "context-curator",
    "incident-commander",
    "decision-arbiter",
    "learning-mentor",
    "head-of-engineering",
    "privacy-compliance-lead",
    "branding-lead",
)


class PersonaProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.examples = yaml.safe_load((ROOT / "evals" / "persona-routing.yaml").read_text())

    def test_15_independent_personas_and_unchanged_technical_leaves(self):
        self.assertEqual(len(self.catalog), 166)
        actual = {name for name, s in self.catalog.items() if s.domain == "personas"}
        self.assertEqual(actual, set(PERSONAS))
        self.assertEqual(len({s.domain for s in self.catalog.values()}), 13)
        self.assertEqual(
            len(list((ROOT / "skills").glob("*/**/references/*.md"))),
            382,
        )
        for name in PERSONAS:
            s = self.catalog[name]
            self.assertEqual(s.path, "skills/personas/" + name)
            self.assertEqual(s.domain, "personas")

    def test_each_protocol_substantial_operational_and_no_external_refs(self):
        for name in PERSONAS:
            with self.subTest(name=name):
                skill = self.catalog[name]
                text = (ROOT / skill.path / "SKILL.md").read_text(encoding="utf-8")
                desc = skill.description
                self.assertIn("Use when", desc)
                self.assertIn("Do not", desc)
                self.assertGreaterEqual(len(text), 4500, name)
                self.assertGreaterEqual(sum(line.startswith("## ") for line in text.splitlines()), 5)
                self.assertTrue(
                    any(term in text.lower() for term in ("example", "worked", "scenario")),
                    name,
                )
                self.assertTrue(
                    any(term in text.lower() for term in ("stop", "exit", "end when")),
                    name,
                )
                self.assertTrue(
                    any(term in text.lower() for term in ("fail", "negative", "anti-pattern")),
                    name,
                )
                self.assertEqual(indexed_references(skill, ROOT), ())
                self.assertFalse((ROOT / skill.path / "references").exists())
                self.assertNotIn("https://", text)
                self.assertNotIn("http://", text)
                with self.assertRaises(ValueError):
                    read_reference(skill, "references/imaginary.md", ROOT)

    def test_all_personas_opt_in_with_no_profile_metadata_growth(self):
        paths = sorted((ROOT / "profiles").glob("*.yaml"))
        self.assertEqual(len(paths), 20)
        for path in paths:
            with self.subTest(profile=path.stem):
                loaded = load_profile(path.stem, ROOT)
                self.assertTrue(set(loaded).isdisjoint(PERSONAS))
                tokens, count = estimate(path.stem, ROOT)
                self.assertLessEqual(count, 20)
                self.assertLessEqual(tokens, 2500)
        self.assertNotIn("grill-master", load_profile("minimal", ROOT))

    def test_single_persona_install_requires_explicit_apply_and_no_references(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)
            dry = install(None, "codex", p, skills=("grill-master",))
            self.assertEqual(len(dry), 1)
            self.assertFalse((p / ".agents").exists())
            installed = install(None, "codex", p, skills=("grill-master",), apply=True)
            target = p / ".agents" / "skills" / "grill-master"
            self.assertEqual(installed[0], target)
            self.assertEqual((target / "SKILL.md").read_bytes(),
                             (ROOT / self.catalog["grill-master"].path / "SKILL.md").read_bytes())
            self.assertFalse((target / "references").exists())
            with self.assertRaises(FileExistsError):
                install(None, "codex", p, skills=("grill-master",), apply=True)

    def test_persona_only_install_does_not_require_a_profile(self):
        srcs = planned_sources(None, skills=("learning-mentor", "scope-guardian"))
        self.assertEqual({p.name for p in srcs}, {"learning-mentor", "scope-guardian"})
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            result = install(None, "claude", p, skills=("learning-mentor",), apply=True)
            self.assertEqual(len(result), 1)
            self.assertTrue((p / ".claude" / "skills" / "learning-mentor" / "SKILL.md").is_file())

    def test_positive_explicit_persona_discovery(self):
        for name in PERSONAS:
            with self.subTest(name=name):
                # Explicit names should win without requiring reading all bodies.
                q = "use persona " + name.replace("-", " ")
                results = search(q, self.catalog, limit=3)
                self.assertTrue(results)
                self.assertEqual(results[0].skill.name, name)

    def test_routine_technical_work_does_not_require_personas(self):
        cases = {
            "FastAPI Pydantic endpoint": "fastapi-service",
            "AWS IAM STS trust policy permissions": "aws-iam-security",
            "Postgres database selection sqlite transactions": "database-selection",
            "shadcn UI components.json registry": "shadcn-ui",
            "fix SQLAlchemy session rollback persistence": "python-persistence",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                results = search(query, self.catalog, limit=3)
                self.assertTrue(results)
                self.assertEqual(results[0].skill.name, expected)

    def test_behavioral_evals_have_distinct_positive_negative_and_safety(self):
        self.assertEqual(self.examples["status"], "unexecuted")
        scenarios = self.examples["scenarios"]
        self.assertGreaterEqual(len(scenarios), len(PERSONAS) + 4)
        self.assertEqual(len({row["id"] for row in scenarios}), len(scenarios))
        positive = {row["expected"] for row in scenarios if "expected" in row}
        self.assertEqual(positive, set(PERSONAS))
        for row in scenarios:
            with self.subTest(case=row["id"]):
                self.assertTrue(row["must"])
                self.assertTrue(row["query"])
                if "expected_not" in row:
                    for name in row["expected_not"]:
                        self.assertIn(name, self.catalog)
                else:
                    self.assertIn(row["expected"], PERSONAS)
                    self.assertTrue(row.get("must_not") or len(row["must"]) >= 3)

    def test_technical_expertise_still_owns_implementation(self):
        doc = (ROOT / "docs" / "persona-protocols.md").read_text()
        for name in PERSONAS:
            self.assertIn(name, doc)
        for neighbor in ("requirements-discovery", "systematic-debugging",
                         "test-strategy", "secure-code-review",
                         "verification-before-done", "agent-orchestration"):
            self.assertIn(neighbor, doc)
        self.assertIn("Do not", self.catalog["grill-master"].description)
        self.assertIn("explicit", self.catalog["execution-orchestrator"].description.lower())
        self.assertEqual(search("/grill-me", self.catalog, limit=1)[0].skill.name,
                         "grill-master")

    def test_leadership_personas_have_independent_specialist_protocols(self):
        contracts = {
            "head-of-engineering": (
                "capacity", "ownership", "delivery", "developer", "quality",
                "30/60/90", "stop criteria", "execution-orchestrator",
            ),
            "privacy-compliance-lead": (
                "controller", "processor", "lawful basis", "DPIA",
                "retention", "rights", "legal", "stop criteria",
            ),
            "branding-lead": (
                "logo", "video", "storyboard", "asset ledger", "rights",
                "interaction-motion", "design-system", "stop conditions",
            ),
        }
        for name, concepts in contracts.items():
            with self.subTest(persona=name):
                body = (ROOT / self.catalog[name].path / "SKILL.md").read_text().lower()
                for term in concepts:
                    self.assertIn(term.lower(), body, (name, term))
                self.assertNotIn("http://", body)
                self.assertNotIn("https://", body)
                self.assertFalse((ROOT / self.catalog[name].path / "references").exists())

    def test_new_leaders_remain_opt_in_without_hijacking_technical_queries(self):
        for name in ("head-of-engineering", "privacy-compliance-lead", "branding-lead"):
            with self.subTest(persona=name):
                self.assertEqual(
                    search("use persona " + name.replace("-", " "), self.catalog, limit=1)[0].skill.name,
                    name,
                )
        existing = {
            "brand-identity-visualization logo concept board": "brand-identity-visualization",
            "interaction-motion CSS transition reduced motion": "interaction-motion",
            "FastAPI Pydantic endpoint": "fastapi-service",
            "AWS IAM STS trust policy permissions": "aws-iam-security",
        }
        for query, expected in existing.items():
            with self.subTest(query=query):
                self.assertEqual(search(query, self.catalog, limit=1)[0].skill.name, expected)

    def test_leadership_behavioral_scenarios_and_role_boundaries(self):
        rows = {case["id"]: case for case in self.examples["scenarios"]}
        for key, owner in (
            ("engineering-lead", "head-of-engineering"),
            ("privacy-governance", "privacy-compliance-lead"),
            ("brand-promo", "branding-lead"),
        ):
            self.assertEqual(rows[key]["expected"], owner)
            self.assertGreaterEqual(len(rows[key]["must"]), 3)
            self.assertTrue(rows[key]["must_not"])
        for key in ("negative-logo-only", "negative-ui-motion-only",
                    "negative-security-endpoint", "negative-task-execution"):
            self.assertIn("expected_not", rows[key])
            self.assertTrue(rows[key]["must"])

    def test_repository_validation(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
