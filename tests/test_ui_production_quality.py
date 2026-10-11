"""UI provider updates: 35 exact API specialists and brand-aware release gates.

Static evidence only. No claim of a visually reviewed website or of
runtime keyboard/accessibility conformance without browser/device testing.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"scripts"))
from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference
from context_budget import estimate
from validate_skills import validate_repository

SPECIAL={
    "shadcn-ui": ("components.json","https://ui.shadcn.com"),
    "base-ui": ("@base-ui/react","https://base-ui.com"),
    "chakra-ui": ("Chakra v3","https://chakra-ui.com"),
    "heroui": ("HeroUI v3","https://heroui.com"),
    "mui": ("MUI X","https://mui.com"),
    "primevue": ("PrimeVue v4","https://v4.primevue.org"),
    "skeleton": ("Skeleton v4","https://www.skeleton.dev"),
    "bits-ui": ("Bits UI v2","https://bits-ui.com"),
}


class UIProductionQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=load_catalog(ROOT)
        cls.providers=sorted(
            name for name,skill in cls.catalog.items()
            if skill.domain=="ui" and name!="ui-component-research"
        )

    def test_maintains_exact_catalog_no_fragmentation(self):
        self.assertEqual(len(self.catalog),148)
        self.assertEqual(len(self.providers),35)
        self.assertEqual(
            len([s for s in self.catalog.values() if s.domain=="ui"]),36)
        reg=yaml.safe_load((ROOT/"registry/skills.yaml").read_text())["skills"]
        self.assertFalse(any("maturity" in r for r in reg))

    def test_all_35_provider_skills_include_fit_and_version_contract(self):
        for name in self.providers:
            with self.subTest(provider=name):
                s=self.catalog[name]
                path=ROOT/s.path/"SKILL.md"
                body=path.read_text(encoding="utf-8")
                self.assertIn("## Current provider contract and visual identity",body)
                self.assertIn("frontend-design",body)
                self.assertIn("https://",body)
                self.assertIn("Use when",s.description)
                self.assertIn("Do not",s.description)

    def test_provider_references_remain_deep_local_and_selective(self):
        count=0
        for name in self.providers:
            with self.subTest(name=name):
                skill=self.catalog[name]
                refs=indexed_references(skill,ROOT)
                self.assertEqual(len(refs),2)
                for ref in refs:
                    data=read_reference(skill,ref,ROOT)
                    self.assertGreater(len(data),1700,(name,ref))
                    self.assertIn("Read when:",data[:500])
                    self.assertIn("https://",data)
                    count+=1
        self.assertEqual(count,70)

    def test_common_ui_specialist_owns_research_not_art_direction(self):
        skill=self.catalog["ui-component-research"]
        refs=indexed_references(skill,ROOT)
        self.assertEqual(len(refs),5)
        self.assertIn("references/provider-compatibility-and-release.md",refs)
        content=read_reference(
            skill,"references/provider-compatibility-and-release.md",ROOT)
        self.assertIn("## Exact API",content)
        self.assertIn("## Visual fidelity",content)
        self.assertIn("https://www.w3.org/WAI/ARIA",content)
        self.assertGreater(len(content),1700)

    def test_design_skill_extended_in_place_not_reduplicated(self):
        skill=self.catalog["frontend-design"]
        refs=indexed_references(skill,ROOT)
        self.assertEqual(len(refs),3)
        leaf=read_reference(skill,"references/brief-to-art-direction.md",ROOT)
        self.assertIn("counterfactual",leaf.lower())
        self.assertIn("https://github.com/anthropics/skills",leaf)
        self.assertNotIn("frontend-design-v2",self.catalog)

    def test_critical_version_and_license_corrections(self):
        for name,(term,link) in SPECIAL.items():
            with self.subTest(provider=name):
                skill=self.catalog[name]
                body=(ROOT/skill.path/"SKILL.md").read_text()
                self.assertIn(term,body)
                self.assertIn(link,body)
        base=(ROOT/self.catalog["base-ui"].path/"SKILL.md").read_text()
        self.assertNotIn("Read the installed @base-ui-components/react",base)
        self.assertIn("Read the installed @base-ui/react package",base)
        self.assertIn("asChild",base)

    def test_negative_framework_route_remains_accurate(self):
        for query,expected in {
            "shadcn ui components.json registry":"shadcn-ui",
            "base ui render headless":"base-ui",
            "radix primitives aschild":"radix-primitives",
            "MUI DataGrid material sx":"mui",
            "bits ui svelte select":"bits-ui",
            "flutter cupertino navigation":"flutter-cupertino",
            "FastAPI Pydantic endpoint":"fastapi-service",
            "/anti-ai-slop":"frontend-design",
        }.items():
            with self.subTest(query=query):
                hits=search(query,self.catalog,limit=3)
                self.assertTrue(hits)
                self.assertEqual(hits[0].skill.name,expected)

    def test_progressive_budget_remains_opt_in(self):
        self.assertIn("shadcn-ui",load_profile("ui-shadcn",ROOT))
        self.assertNotIn("mui",load_profile("web-app",ROOT))
        base,_=estimate("ui-shadcn",ROOT)
        activated,_=estimate("ui-shadcn",ROOT,("shadcn-ui",))
        self.assertLess(base,activated)
        self.assertLessEqual(base,2500)
        for ref in ("../SKILL.md","references/../../README.md",
                    "references/nonexistent.md"):
            with self.subTest(path=ref),self.assertRaises(ValueError):
                read_reference(self.catalog["ui-component-research"],ref,ROOT)

    def test_manual_briefs_vary_by_actual_work_and_do_not_invent_claims(self):
        src=yaml.safe_load((ROOT/"evals/ui-visual-briefs.yaml").read_text())
        cases=src["scenarios"]
        self.assertGreaterEqual(len(cases),3)
        self.assertEqual(len({x["id"] for x in cases}),len(cases))
        self.assertEqual(len({x["direction"] for x in cases}),len(cases))
        for x in cases:
            self.assertTrue(x["factual_inputs"])
            self.assertTrue(x["acceptance"])
            self.assertIn("invent",x["anti_template_failure"].lower(),
                          "Each challenge should block hallucinated business facts")

    def test_official_audit_and_honest_runtime_limitations(self):
        s=(ROOT/"docs/ui-refactor-audit.md").read_text()
        for word in ("Anthropic","Vercel","MUI","HeroUI","Chakra","WCAG",
                     "Skeleton","SOTA"):
            self.assertIn(word,s)
        guideline=(ROOT/"docs/ui-production-quality.md").read_text()
        self.assertIn("real",guideline)
        self.assertIn("24×24",guideline)
        self.assertIn("No automated",guideline)

    def test_entire_repository_integrity(self):
        self.assertEqual(validate_repository(ROOT),[])


if __name__=="__main__":
    unittest.main()
