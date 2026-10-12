"""Deterministic discovery properties, not native-agent activation evidence."""
import contextlib
import io
import json
import unittest
from pathlib import Path

import yaml

import toolkit.catalog as routing
from toolkit.cli import main

ROOT = Path(__file__).resolve().parents[1]


class RoutingRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = routing.load_catalog(ROOT)

    def names(self, query):
        return {m.skill.name for m in routing.search(query, self.catalog)}

    def test_database_choice_bilingual_without_base_ui(self):
        for query in ("choisir une base de données pour mon SaaS",
                      "choose a database for my SaaS",
                      "comparer les bases de données pour le stockage"):
            with self.subTest(query=query):
                self.assertIn("database-selection", self.names(query))
                self.assertNotIn("base-ui", self.names(query))

    def test_debugging_is_not_provider_selection(self):
        for query in ("debug duplicate payment after provider timeout",
                      "diagnostiquer un paiement dupliqué après un timeout fournisseur"):
            with self.subTest(query=query):
                self.assertIn("systematic-debugging", self.names(query))
                self.assertNotIn("cloud-provider-selection", self.names(query))

    def test_sensitive_documentation_typo_needs_no_skill(self):
        for query in ("Fix a typo in authentication documentation",
                      "corriger une faute dans la documentation d'authentification"):
            with self.subTest(query=query):
                self.assertEqual(routing.suggest_workflow(query)[0], "light")
                self.assertEqual(self.names(query), set())

    def test_exclusion_words_do_not_score(self):
        skill = routing.Skill("widget", "ui", "skills/ui/widget",
                              "Use for rendering widgets. Do not use for database selection.", ())
        self.assertEqual(routing.search("database selection", {skill.name: skill}), [])

    def test_exclusion_can_override_positive_keywords(self):
        skill = routing.Skill("widget", "ui", "skills/ui/widget",
                              "Use for widgets. Do not use for database selection.",
                              ("database", "selection"))
        self.assertEqual(routing.search("choose a database", {skill.name: skill}), [])

    def test_explicit_base_ui_survives(self):
        self.assertIn("base-ui", self.names("Implement a Base UI Dialog render"))

    def test_real_consequences_and_mentions(self):
        cases = {
            "restrict one tenant lookup": "deep",
            "remove the ownership filter from lookup": "deep",
            "modifier le prédicat d'autorisation entre tenants": "deep",
            "perform an irreversible data migration": "deep",
            "migration irréversible des données": "deep",
            "local reversible refactor of a helper": "light",
            "explain authentication in documentation": "light",
            "choose a database for my SaaS": "standard",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(routing.suggest_workflow(query)[0], expected)

    def test_public_explanation_is_available_and_advisory(self):
        discovery = routing.discover("Implement a date picker with an unknown UI provider", self.catalog)
        self.assertEqual(discovery.uncertainty, "ambiguous")
        self.assertTrue(discovery.required_checks)
        self.assertTrue(any(m.unfavorable for m in discovery.candidates))
        excluded = routing.discover("debug duplicate payment after provider timeout", self.catalog)
        self.assertIn("cloud-provider-selection", {x.skill.name for x in excluded.excluded})
        advice = routing.workflow_advice("restrict one tenant lookup")
        self.assertEqual(advice.risk, "potential")
        self.assertNotEqual(advice.source, "observed_change_signals")
        self.assertTrue(advice.required_checks)
        unknown = routing.workflow_advice("make it better")
        self.assertEqual(unknown.risk, "insufficient")

    def test_confirmed_risk_requires_observations(self):
        from toolkit.adaptive_policy import ChangeSignals
        advice = routing.workflow_advice("tiny correction", observed=ChangeSignals(authorization_or_secrets=True))
        self.assertEqual(advice.workflow, "deep")
        self.assertEqual(advice.risk, "confirmed")
        self.assertEqual(advice.source, "observed_change_signals")
        self.assertIn("independent R2 risk review unavailable", advice.required_checks)

    def test_no_match_and_profile_limits(self):
        for query in ("", "zzzxxyyqq"):
            self.assertEqual(self.names(query), set())
        allowed = routing.load_profile("minimal")
        self.assertTrue(all(m.skill.name in allowed for m in routing.search("choose database", self.catalog, allowed=allowed)))

    def test_routing_fixture_properties(self):
        fixture = yaml.safe_load((ROOT / "evals/routing-regressions.yaml").read_text())
        for case in fixture["selection"]:
            with self.subTest(query=case["query"]):
                actual = self.names(case["query"])
                self.assertTrue(set(case["include"]) <= actual)
                self.assertTrue(set(case["exclude"]).isdisjoint(actual))
        for case in fixture["workflows"]:
            with self.subTest(query=case["query"]):
                self.assertEqual(routing.suggest_workflow(case["query"])[0], case["expected"])
        for query in fixture["no_match"]:
            with self.subTest(query=query):
                self.assertEqual(self.names(query), set())

    def test_cli_legacy_search_json_shape(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main(["search", "FastAPI Pydantic endpoint", "--json"])
        self.assertIsInstance(json.loads(output.getvalue()), list)


class RoutingDiagnosticsTests(unittest.TestCase):
    def test_cli_explanation_has_separate_evidence_and_unknowns(self):
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                result = main(["recommend", "restrict one tenant lookup", "--json", "--explain"])
        except SystemExit as exc:
            self.fail(f"explanation interface not implemented: {exc}")
        report = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(report["workflow"]["risk"], "potential")
        self.assertEqual(report["workflow"]["source"], "request_heuristic")
        self.assertIn("excluded", report)
        self.assertIn("uncertainty", report)
        self.assertTrue(report["required_checks"])

    def test_negated_technology_is_not_positive_evidence(self):
        c = routing.load_catalog(ROOT)
        for query in ("Do not use FastAPI; review SQLAlchemy AsyncSession",
                      "without FastAPI, review SQLAlchemy AsyncSession",
                      "sans FastAPI; examiner SQLAlchemy AsyncSession"):
            with self.subTest(query=query):
                names = {m.skill.name for m in routing.search(query, c)}
                self.assertIn("python-persistence", names)
                self.assertNotIn("fastapi-service", names)

    def test_partial_exclusion_is_check_not_observed_fact(self):
        s = routing.Skill("widget", "ui", "skills/ui/widget",
                          "Use for widgets. Do not use for database schema migration.", ("database",))
        result = routing.discover("widget database schema", {s.name: s})
        self.assertTrue(result.candidates)
        self.assertTrue(result.candidates[0].unfavorable)
        self.assertEqual(result.excluded, ())

    def test_sensitive_fix_is_not_downgraded_by_documentation_mention(self):
        for query in ("fix authorization predicate", "refactor tenant ownership filter",
                      "fix a typo in documentation and remove tenant restriction"):
            with self.subTest(query=query):
                self.assertEqual(routing.suggest_workflow(query)[0], "deep")
        self.assertEqual(routing.suggest_workflow("update authentication documentation")[0], "light")

    def test_selection_intent_allows_both_languages(self):
        c = routing.load_catalog(ROOT)
        for query in ("choose a cloud provider compare AWS and GCP",
                      "comparer AWS et GCP pour choisir un fournisseur cloud"):
            self.assertIn("cloud-provider-selection", {m.skill.name for m in routing.search(query, c)})


class RoutingReviewRegressions(unittest.TestCase):
    def test_query_negation_survives_generic_keyword_overlap(self):
        c = routing.load_catalog(ROOT)
        names = {m.skill.name for m in routing.search("Do not use FastAPI; implement an HTTP endpoint", c)}
        self.assertNotIn("fastapi-service", names)

    def test_safety_warning_is_not_activation_exclusion(self):
        c = routing.load_catalog(ROOT)
        result = routing.discover("plan schema migration with external effects", c)
        self.assertNotIn("schema-migrations", {e.skill.name for e in result.excluded})
        self.assertIn("schema-migrations", {m.skill.name for m in result.candidates})

    def test_mixed_documentation_and_operational_changes(self):
        for query in ("Fix authentication and update docs",
                      "Fix a documentation typo and update authorization checks",
                      "Explain rollback then perform a data migration",
                      "delete all customer data"):
            with self.subTest(query=query):
                self.assertEqual(routing.suggest_workflow(query)[0], "deep")


if __name__ == "__main__":
    unittest.main()
