"""Offline candidate diagnostics and agent-decision handoff, not model-behavior proof."""
from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path

import yaml

import toolkit.catalog as routing
from toolkit.adaptive_policy import ChangeSignals
from toolkit.cli import main

ROOT = Path(__file__).resolve().parents[1]


class RoutingRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = routing.load_catalog(ROOT)

    def names(self, query: str) -> set[str]:
        return {m.skill.name for m in routing.search(query, self.catalog)}

    def test_selection_and_no_match_cases(self):
        fixture = yaml.safe_load((ROOT / "evals/routing-regressions.yaml").read_text())
        for case in fixture["selection"]:
            with self.subTest(query=case["query"]):
                found = self.names(case["query"])
                self.assertTrue(set(case["include"]) <= found)
                self.assertTrue(set(case["exclude"]).isdisjoint(found))
        for query in fixture["no_match"]:
            with self.subTest(query=query):
                self.assertFalse(self.names(query))

    def test_free_text_never_claims_to_decide_workflow(self):
        fixture = yaml.safe_load((ROOT / "evals/routing-regressions.yaml").read_text())
        for query in fixture["unclassified"]:
            with self.subTest(query=query):
                advice = routing.workflow_advice(query)
                self.assertEqual((advice.workflow, advice.risk, advice.source),
                                 ("unclassified", "unknown", "agent_decision_required"))
                self.assertTrue(advice.required_checks)
                self.assertEqual(routing.suggest_workflow(query)[0], "unclassified")

    def test_structured_observations_remain_separate(self):
        cases = (
            (ChangeSignals(authorization_or_secrets=True), "deep"),
            (ChangeSignals(local_reversible=True), "light"),
            (ChangeSignals(multi_component=True), "standard"),
        )
        for observations, expected in cases:
            with self.subTest(workflow=expected):
                advice = routing.workflow_advice("arbitrary words", observed=observations)
                self.assertEqual(advice.workflow, expected)
                self.assertEqual(advice.source, "caller_supplied_change_signals")

    def test_exclusion_is_not_positive_evidence(self):
        skill = routing.Skill("widget", "ui", "skills/ui/widget",
                              "Use for widgets. Do not use for database selection.", ())
        self.assertEqual(routing.search("database selection", {skill.name: skill}), [])

    def test_exclusions_and_safety_warnings(self):
        denied = routing.Skill("widget", "ui", "skills/ui/widget",
                               "Use for widgets. Do not use for database selection.",
                               ("database", "selection"))
        self.assertFalse(routing.search("choose a database", {denied.name: denied}))
        allowed = routing.Skill("widget", "ui", "skills/ui/widget",
                                "Use for widgets. Do not assume user credentials are safe.",
                                ("widget",))
        self.assertTrue(routing.search("widget", {allowed.name: allowed}))

    def test_negative_and_ambiguous_discovery(self):
        names = self.names("Do not use FastAPI; review SQLAlchemy AsyncSession")
        self.assertIn("python-persistence", names)
        self.assertNotIn("fastapi-service", names)
        self.assertNotIn("fastapi-service", self.names("without FastAPI, review SQLAlchemy"))
        self.assertIn("base-ui", self.names("Implement a Base UI Dialog render"))
        result = routing.discover("Implement a date picker with an unknown UI provider", self.catalog)
        self.assertEqual(result.uncertainty, "ambiguous")

    def test_legacy_search_json_shape(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(main(["search", "FastAPI Pydantic endpoint", "--json"]), 0)
        self.assertIsInstance(json.loads(stream.getvalue()), list)

    def test_recommend_explicitly_abstains(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(main(["recommend", "modify billing logic", "--json", "--explain"]), 0)
        report = json.loads(stream.getvalue())
        self.assertEqual(report["workflow"]["workflow"], "unclassified")
        self.assertEqual(report["workflow"]["source"], "agent_decision_required")
        self.assertIn("candidates", report)


class RoutingContextTests(unittest.TestCase):
    def _run(self, *arguments: str) -> object:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(main(["routing-context", *arguments]), 0)
        return yaml.safe_load(stream.getvalue())

    def test_scoped_profile_yaml_architecture_and_metadata(self):
        result = self._run("--profile", "minimal")
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["scope"]["skill_count"], 5)
        self.assertTrue(result["scope"]["cataloged_not_proven_installed"])
        self.assertEqual(result["architecture"]["decision_owner"],
                         "skills/core/task-routing/SKILL.md")
        self.assertEqual({entry["name"] for entry in result["skills"]},
                         set(routing.load_profile("minimal")))
        self.assertTrue(all(entry["path"].endswith("/SKILL.md") for entry in result["skills"]))
        self.assertTrue(all(entry["use_when"] for entry in result["skills"]))
        self.assertNotIn("references/", str(result["skills"]))

    def test_explicit_skills_no_duplication_and_json(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(main(["routing-context", "--skill", "task-routing",
                                   "--skill", "task-routing", "--skill", "database-selection",
                                   "--json"]), 0)
        output = json.loads(stream.getvalue())
        self.assertEqual([x["name"] for x in output["skills"]],
                         ["task-routing", "database-selection"])

    def test_profile_does_not_claim_host_activation(self):
        report = self._run("--profile", "minimal")
        self.assertNotIn("activated", report["scope"])
        self.assertNotIn("installed", report["scope"])
        self.assertIn("permissions", report["architecture"])

    def test_metadata_separates_scope_exclusions_from_cautions(self):
        skill = routing.Skill("sample", "core", "skills/core/sample",
                              "Use when checking widgets. Do not use for databases. "
                              "Do not assume credentials are safe.", ("widgets",))
        meta = routing.routing_metadata(skill)
        self.assertIn("Do not use for databases", meta["avoid_when"][0])
        self.assertIn("Do not assume credentials", meta["cautions"][0])

    def test_explicit_scope_required_and_bounded(self):
        for args in ((), ("--skill", "unknown-skill"),
                     ("--profile", "nonexistent"),
                     tuple(sum((["--skill", s] for s in list(routing.load_catalog())[:21]), []))):
            with self.subTest(args=args):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    main(["routing-context", *args])


if __name__ == "__main__":
    unittest.main()
