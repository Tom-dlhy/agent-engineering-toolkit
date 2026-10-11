"""Frontend category — routing, source references, guardrails and context budget.

This is catalog/contract evidence; it does not prove behavior of a real
Next/Nuxt/SvelteKit/Angular/Astro runtime or browser without separate tests.
"""
import re
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT / "scripts"))
from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference
from context_budget import estimate
from validate_skills import validate_repository

FRAMEWORKS = {
    "react-architecture", "nextjs-application", "tanstack-start",
    "vue-application", "sveltekit-application",
    "angular-application", "astro-application",
}
OFFICIAL = {
    "react-architecture": "react.dev",
    "nextjs-application": "nextjs.org",
    "tanstack-start": "tanstack.com",
    "vue-application": "vuejs.org",
    "sveltekit-application": "svelte.dev",
    "angular-application": "angular.dev",
    "astro-application": "astro.build",
}


class FrontendExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.routes = yaml.safe_load((ROOT / "evals/frontend-routing.yaml").read_text())

    def test_seven_independent_frontend_skills(self):
        self.assertEqual(len(self.catalog), 163)
        found = {s.name for s in self.catalog.values() if s.domain == "frontend"}
        self.assertEqual(found, FRAMEWORKS)
        self.assertNotIn("vue-svelte-patterns", self.catalog)

    def test_21_deep_references_and_official_sources(self):
        total = 0
        for name in sorted(FRAMEWORKS):
            with self.subTest(skill=name):
                skill = self.catalog[name]
                self.assertIn("Use when", skill.description)
                self.assertIn("Do not", skill.description)
                leaves = indexed_references(skill, ROOT)
                self.assertEqual(len(leaves), 3)
                content = (ROOT / skill.path / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("## Implementation procedure", content)
                self.assertIn("## Targeted expertise", content)
                for ref in leaves:
                    body = read_reference(skill, ref, ROOT)
                    self.assertTrue(body.startswith("# "))
                    self.assertIn("Read when:", body[:600])
                    self.assertGreater(len(body), 1400, (name, ref))
                    self.assertIn("## Official references", body)
                    # In multi-framework Nuxt skills, source may be Nuxt rather than Vue.
                    domain = OFFICIAL[name]
                    if name == "vue-application":
                        self.assertTrue("nuxt.com" in body or "vuejs.org" in body)
                    else:
                        self.assertIn(domain, body)
                    total += 1
        self.assertEqual(total, 21)

    def test_positive_routing(self):
        for row in self.routes["selection"]:
            with self.subTest(q=row["query"]):
                result = search(row["query"], self.catalog, limit=3)
                self.assertTrue(result)
                self.assertEqual(result[0].skill.name, row["expected"])

    def test_negative_neighbors(self):
        for row in self.routes["negative_neighbors"]:
            with self.subTest(q=row["query"]):
                result = search(row["query"], self.catalog, limit=3)
                self.assertTrue(result)
                self.assertEqual(result[0].skill.name, row["expected"])

    def test_unmatched_stays_unmatched(self):
        for query in self.routes["no_match"]:
            self.assertEqual(search(query, self.catalog), [])

    def test_opt_in_profile_and_reference_guards(self):
        entries = load_profile("frontend-platform", ROOT)
        self.assertEqual(len(entries), 18)
        self.assertTrue(FRAMEWORKS.issubset(set(entries)))
        self.assertNotIn("vue-svelte-patterns", entries)
        self.assertNotIn("astro-application", load_profile("minimal", ROOT))
        base, _ = estimate("frontend-platform", ROOT)
        active, _ = estimate("frontend-platform", ROOT, ("tanstack-start",))
        full, _ = estimate("frontend-platform", ROOT, ("tanstack-start",),
                           ("tanstack-start:references/start-server-functions-auth.md",))
        self.assertLess(base, active)
        self.assertLess(active, full)
        self.assertLessEqual(base, 2500)
        skill = self.catalog["tanstack-start"]
        for invalid in ("../SKILL.md","references/../../README.md","references/undefined.md"):
            with self.subTest(path=invalid), self.assertRaises(ValueError):
                read_reference(skill, invalid, ROOT)

    def test_security_claims_are_explicit_not_navigation_only(self):
        text = read_reference(
            self.catalog["tanstack-start"],
            "references/start-server-functions-auth.md", ROOT
        )
        self.assertIn("beforeLoad", text)
        self.assertIn("CSRF", text)
        next_text = read_reference(
            self.catalog["nextjs-application"],
            "references/next-actions-security-testing.md", ROOT
        )
        self.assertIn("authorize", next_text.lower())
        svelte = read_reference(
            self.catalog["sveltekit-application"],
            "references/sveltekit-load-actions-security.md", ROOT
        )
        self.assertIn("direct action calls", svelte)

    def test_source_audit_and_single_standard(self):
        audit = (ROOT / "docs/frontend-refactor-audit.md").read_text()
        for name in ("React","Next.js","TanStack","Vue","Nuxt","Svelte",
                     "Angular","Astro","SOTA"):
            self.assertIn(name, audit)
        reg = yaml.safe_load((ROOT / "registry/skills.yaml").read_text())["skills"]
        self.assertFalse(any("maturity" in item for item in reg))

    def test_validate_entire_repository(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
