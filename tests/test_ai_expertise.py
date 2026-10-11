"""AI category research: one standard, 26 refs, targeted routing and privacy."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"scripts"))
from toolkit.catalog import load_catalog,load_profile,search
from toolkit.knowledge import indexed_references,read_reference
from context_budget import estimate
from validate_skills import validate_repository

AI={
    "agent-tool-safety":3,
    "llm-evaluation":3,
    "llm-integration":4,
    "python-llm-gateways":4,
    "rag-evaluation":3,
    "agent-orchestration":3,
    "rag-engineering":3,
    "mcp-integration":3,
}


class AIExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=load_catalog(ROOT)
        cls.cases=yaml.safe_load((ROOT/"evals/ai-routing.yaml").read_text())

    def test_catalog_eight_independent_ai_skills(self):
        self.assertEqual(len(self.catalog),171)
        self.assertEqual(
            {x.name for x in self.catalog.values() if x.domain=="ai"},set(AI))

    def test_one_quality_contract_without_maturity(self):
        entries=yaml.safe_load((ROOT/"registry/skills.yaml").read_text())["skills"]
        self.assertFalse(any("maturity" in e for e in entries))

    def test_all_26_deep_source_annotated_selective_refs(self):
        n=0
        for name,total in AI.items():
            with self.subTest(name=name):
                s=self.catalog[name]
                self.assertIn("Use when",s.description)
                self.assertIn("Do not",s.description)
                refs=indexed_references(s,ROOT)
                self.assertEqual(len(refs),total)
                for path in refs:
                    data=read_reference(s,path,ROOT)
                    self.assertTrue(data.startswith("# "))
                    self.assertIn("Read when:",data[:600])
                    self.assertIn("## ",data)
                    self.assertIn("https://",data)
                    self.assertGreater(len(data),1400,(name,path))
                    n+=1
        self.assertEqual(n,26)

    def test_positive_routing(self):
        for case in self.cases["selection"]:
            with self.subTest(query=case["query"]):
                r=search(case["query"],self.catalog,limit=3)
                self.assertTrue(r)
                self.assertEqual(r[0].skill.name,case["expected"])

    def test_negative_neighbors(self):
        for case in self.cases["negative_neighbors"]:
            with self.subTest(query=case["query"]):
                r=search(case["query"],self.catalog,limit=3)
                self.assertTrue(r)
                self.assertEqual(r[0].skill.name,case["expected"])

    def test_no_match(self):
        for query in self.cases["no_match"]:
            self.assertEqual(search(query,self.catalog),[])

    def test_ref_access_safe_and_opt_in(self):
        skill=self.catalog["mcp-integration"]
        good="references/auth-and-tool-contracts.md"
        self.assertIn(good,indexed_references(skill,ROOT))
        for invalid in ("../SKILL.md","references/../../README.md",
                        "references/not-declared.md"):
            with self.subTest(path=invalid),self.assertRaises(ValueError):
                read_reference(skill,invalid,ROOT)
        b,_=estimate("ai-engineering",ROOT)
        a,_=estimate("ai-engineering",ROOT,("mcp-integration",))
        c,_=estimate("ai-engineering",ROOT,("mcp-integration",),
                     ("mcp-integration:references/auth-and-tool-contracts.md",))
        self.assertLess(b,a)
        self.assertLess(a,c)
        self.assertLessEqual(b,2500)

    def test_profile_bounds_and_no_autoload(self):
        ai=load_profile("ai-engineering",ROOT)
        self.assertEqual(len(ai),19)
        for x in AI: self.assertIn(x,ai)
        python=load_profile("python-llm-production",ROOT)
        self.assertEqual(len(python),20)
        self.assertIn("agent-orchestration",python)
        self.assertNotIn("mcp-integration",python)
        self.assertNotIn("mcp-integration",load_profile("minimal",ROOT))

    def test_primary_evidence_and_limits(self):
        doc=(ROOT/"docs/ai-refactor-audit.md").read_text()
        for word in ("OWASP","MCP","2026-07-28","LangGraph",
                     "LiteLLM","RAG","OpenAI","Azure","Vertex","Bedrock"):
            self.assertIn(word,doc)

    def test_repository_validator(self):
        self.assertEqual(validate_repository(ROOT),[])


if __name__=="__main__":
    unittest.main()
