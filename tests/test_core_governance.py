"""Core expertise, removal of maturity tiers, and universal reference safety.

Tests verify a deterministic lexical baseline and static rules, NOT live model
behavior, repository-wide technical expertise, or deployment permission.
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

from toolkit.catalog import load_catalog, load_profile, search, suggest_workflow
from toolkit.knowledge import indexed_references, read_reference
from context_budget import estimate
from validate_skills import validate_repository

CORE = (
    "task-routing",
    "skill-authoring",
    "systematic-debugging",
    "verification-before-done",
    "requirements-discovery",
)


def _fixture(root: Path, *, legacy_maturity: bool = False, missing_leaf: bool = True) -> None:
    """Create an isolated small repository; no external network or executables."""
    folder = root / "skills" / "core" / "example-core"
    (folder / "references").mkdir(parents=True)
    (root / "registry").mkdir(parents=True)
    (root / "profiles").mkdir(parents=True)
    source = (
        "---\nname: example-core\ndomain: core\n"
        "description: >-\n  Use when testing a fake skill's references. "
        "Do not use for a real user task.\n---\n"
        "# Example core\n\n## Procedure\n"
        "Read the declared leaf when testing the sample file; "
        "otherwise preserve the implementation constraints.\n"
        "[Leaf](references/checks.md) — read when testing integrity.\n"
    )
    (folder / "SKILL.md").write_text(source, encoding="utf-8")
    if not missing_leaf:
        (folder / "references" / "checks.md").write_text(
            "# Checks\n\n**Read when:** testing.\n\n## Example\n"
            "Check behavior and failure cases.\n", encoding="utf-8"
        )
    entry = {
        "name": "example-core", "domain": "core",
        "path": "skills/core/example-core", "keywords": ["example"],
    }
    if legacy_maturity:
        entry["maturity"] = "expert-v2"
    (root / "registry" / "skills.yaml").write_text(
        yaml.safe_dump({"version": 1, "skills": [entry]}, sort_keys=False),
        encoding="utf-8",
    )
    (root / "profiles" / "minimal.yaml").write_text(
        "name: minimal\ndescription: Test\nskills: [example-core]\n", encoding="utf-8"
    )


class CoreGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skills = load_catalog(ROOT)
        cls.fixtures = yaml.safe_load(
            (ROOT / "evals" / "core-routing.yaml").read_text(encoding="utf-8")
        )

    def test_five_existing_core_skills_without_duplication(self) -> None:
        found = {x.name for x in self.skills.values() if x.domain == "core"}
        self.assertEqual(found, set(CORE))
        self.assertEqual(len(self.skills), 163)

    def test_all_core_skills_have_targeted_substantial_local_references(self) -> None:
        for name in CORE:
            with self.subTest(name=name):
                skill = self.skills[name]
                body = (ROOT / skill.path / "SKILL.md").read_text()
                self.assertIn("## ", body)
                self.assertIn("Do not", skill.description)
                refs = indexed_references(skill, ROOT)
                self.assertGreaterEqual(len(refs), 2)
                for leaf in refs:
                    contents = read_reference(skill, leaf, ROOT)
                    self.assertGreater(len(contents), 1500)
                    self.assertIn("Read when:", contents[:500])
                    self.assertIn("## ", contents)

    def test_registry_has_no_maturity_tiers_and_no_tier_routing(self) -> None:
        registry = yaml.safe_load(
            (ROOT / "registry" / "skills.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(len(registry["skills"]), 163)
        self.assertFalse(any("maturity" in row for row in registry["skills"]))
        self.assertNotIn("maturity", (ROOT / "toolkit" / "catalog.py").read_text())

    def test_deterministic_positive_and_neighbor_routing(self) -> None:
        for case in self.fixtures["selection"]:
            with self.subTest(query=case["query"]):
                results = search(case["query"], self.skills, limit=3)
                self.assertTrue(results)
                self.assertEqual(results[0].skill.name, case["expected"])

    def test_unknown_queries_do_not_force_activation(self) -> None:
        for query in self.fixtures["no_match"]:
            with self.subTest(query=query):
                self.assertEqual(search(query, self.skills), [])

    def test_light_standard_deep_are_workflow_not_trust(self) -> None:
        for case in self.fixtures["workflows"]:
            with self.subTest(query=case["query"]):
                self.assertEqual(suggest_workflow(case["query"])[0], case["expected"])

    def test_reference_read_is_opt_in_and_context_incremental(self) -> None:
        base, count = estimate("minimal", ROOT)
        active, other = estimate("minimal", ROOT, ("systematic-debugging",))
        specific, _ = estimate(
            "minimal", ROOT, ("systematic-debugging",),
            ("systematic-debugging:references/reproduction-and-isolation.md",),
        )
        self.assertEqual(count, other)
        self.assertLess(base, active)
        self.assertLess(active, specific)
        self.assertLessEqual(base, 2500)
        with self.assertRaises(ValueError):
            estimate(
                "minimal", ROOT, (),
                ("systematic-debugging:references/reproduction-and-isolation.md",),
            )
        with self.assertRaises(ValueError):
            read_reference(
                self.skills["systematic-debugging"], "../AGENTS.md", ROOT
            )

    def test_universal_validation_detects_undeclared_missing_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _fixture(root, missing_leaf=True)
            problems = validate_repository(root)
            self.assertTrue(any("invalid leaf" in p for p in problems), problems)

    def test_universal_validation_rejects_reintroduced_maturity(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _fixture(root, legacy_maturity=True, missing_leaf=False)
            problems = validate_repository(root)
            self.assertTrue(any("maturity tiers are not allowed" in p for p in problems), problems)

    def test_universally_checked_leaf_is_valid_without_old_tier(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _fixture(root, missing_leaf=False)
            self.assertEqual(validate_repository(root), [])

    def test_repo_and_profile_validation(self) -> None:
        self.assertEqual(validate_repository(ROOT), [])
        self.assertIn("task-routing", load_profile("minimal", ROOT))


if __name__ == "__main__":
    unittest.main()
