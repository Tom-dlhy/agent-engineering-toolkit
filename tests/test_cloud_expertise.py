"""Cloud refactor: service taxonomy, progressive references and provider profiles.

Mock/static/lexical checks only; no live provider identity proof or cloud mutation.
"""
from __future__ import annotations
import ast
import re
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

AWS = ("aws-rds-postgres","aws-dynamodb","aws-eventbridge",
       "aws-secrets-manager","aws-vpc-networking","aws-api-gateway")
GCP = ("gcp-iam-identity","gcp-cloud-run","gcp-cloud-storage",
       "gcp-pubsub","gcp-secret-manager","gcp-cloud-sql")
AZURE = ("azure-identity-security","azure-container-apps","azure-blob-storage",
         "azure-service-bus","azure-key-vault","azure-functions-runtime")
CF = ("cloudflare-workers-runtime","cloudflare-r2-storage",
      "cloudflare-d1-database","cloudflare-access-security")
NEW = AWS + GCP + AZURE + CF
ALL_CLOUD = (
    "aws-bedrock","aws-ecs-deployment","aws-iam-security",
    "aws-integration","aws-lambda-runtime","aws-s3-storage",
    "aws-sqs-messaging","azure-ai-foundry","azure-integration",
    "ci-cd-engineering","cloud-provider-selection","cloudflare-platform",
    "container-hardening","finops-engineering","gcp-integration",
    "gcp-vertex-ai","kubernetes-deployment","observability-sre",
    "terraform-iac",
) + NEW
OFFICIAL = {"aws":("docs.aws.amazon.com",),
            "gcp":("docs.cloud.google.com",),
            "azure":("learn.microsoft.com",),
            "cloudflare":("developers.cloudflare.com",)}


class CloudExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=load_catalog(ROOT)
        cls.cases=yaml.safe_load((ROOT/"evals/cloud-routing.yaml").read_text())

    def test_41_independent_cloud_skills_141_catalog(self):
        self.assertEqual(len(self.catalog),166)
        self.assertEqual({s.name for s in self.catalog.values()
                          if s.domain=="cloud"},set(ALL_CLOUD))
        self.assertEqual(len(NEW),22)

    def test_single_standard_without_tier(self):
        entries=yaml.safe_load((ROOT/"registry/skills.yaml").read_text())["skills"]
        self.assertFalse(any("maturity" in e for e in entries))
        self.assertEqual(len(entries),166)

    def test_82_declared_selective_cloud_references(self):
        total=0
        for name in ALL_CLOUD:
            with self.subTest(name=name):
                skill=self.catalog[name]
                self.assertIn("Use when",skill.description)
                self.assertIn("Do not",skill.description)
                refs=indexed_references(skill,ROOT)
                self.assertEqual(len(refs),2)
                for ref in refs:
                    text=read_reference(skill,ref,ROOT)
                    self.assertGreater(len(text),1300,(name,ref))
                    self.assertTrue("Read when:" in text[:650] or "Open when:" in text[:650])
                    self.assertTrue(text.startswith("# "))
                    self.assertIn("https://",text)
                    total+=1
        self.assertEqual(total,82)

    def test_new_service_specific_sources_and_connectivity(self):
        for name in NEW:
            with self.subTest(name=name):
                skill=self.catalog[name]
                leaves=" ".join(read_reference(skill,ref,ROOT)
                                for ref in indexed_references(skill,ROOT))
                provider=("aws" if name.startswith("aws-") else "gcp"
                          if name.startswith("gcp-") else "azure"
                          if name.startswith("azure-") else "cloudflare")
                self.assertTrue(any(domain in leaves for domain in OFFICIAL[provider]))
                self.assertTrue(any(word in leaves.lower()
                                    for word in ("identity","credentials","iam","rbac","binding")))
                self.assertTrue(any(word in leaves.lower()
                                    for word in ("permission","role","scope","authorization")))
                self.assertTrue(any(word in leaves.lower()
                                    for word in ("retry","timeout","recovery","fault")))

    def test_positive_routing_service_names(self):
        for row in self.cases["selection"]:
            with self.subTest(query=row["query"]):
                found=search(row["query"],self.catalog,limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name,row["expected"])

    def test_negative_interdomain_routing(self):
        for row in self.cases["negative_neighbors"]:
            with self.subTest(query=row["query"]):
                found=search(row["query"],self.catalog,limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name,row["expected"])

    def test_unknown_does_not_activate(self):
        for query in self.cases["no_match"]:
            self.assertEqual(search(query,self.catalog),[])

    def test_provider_profiles_and_token_budgets(self):
        profiles={"aws-platform":20,"gcp-platform":15,"azure-platform":15,
                  "cloudflare-edge":12}
        for name,expected in profiles.items():
            with self.subTest(profile=name):
                entries=load_profile(name,ROOT)
                self.assertEqual(len(entries),expected)
                self.assertEqual(len(set(entries)),len(entries))
                budget,_=estimate(name,ROOT)
                self.assertLessEqual(budget,2500)
        for name,prof in (("aws-rds-postgres","aws-platform"),
                          ("gcp-cloud-run","gcp-platform"),
                          ("azure-blob-storage","azure-platform"),
                          ("cloudflare-d1-database","cloudflare-edge")):
            self.assertIn(name,load_profile(prof,ROOT))
            self.assertNotIn(name,load_profile("minimal",ROOT))

    def test_opt_in_reference_loading_and_traversal_rejected(self):
        skill=self.catalog["gcp-cloud-run"]
        path="references/connection-and-permissions.md"
        self.assertIn(path,indexed_references(skill,ROOT))
        for invalid in ("../SKILL.md","references/../../README.md","references/unknown.md"):
            with self.subTest(path=invalid),self.assertRaises(ValueError):
                read_reference(skill,invalid,ROOT)
        base,_=estimate("gcp-platform",ROOT)
        active,_=estimate("gcp-platform",ROOT,("gcp-cloud-run",))
        leaf,_=estimate("gcp-platform",ROOT,("gcp-cloud-run",),
                       ("gcp-cloud-run:"+path,))
        self.assertLess(base,active)
        self.assertLess(active,leaf)

    def test_python_connection_code_fences_parse_as_python(self):
        # AST catches broken snippets without importing cloud SDKs or making requests.
        for name in NEW:
            for ref in indexed_references(self.catalog[name],ROOT):
                content=read_reference(self.catalog[name],ref,ROOT)
                for snippet in re.findall(r"~~~python\n(.*?)\n~~~",content,re.S):
                    with self.subTest(name=name,ref=ref):
                        ast.parse(snippet)

    def test_security_guardrails_and_source_audit(self):
        doc=(ROOT/"docs/cloud-refactor-audit.md").read_text()
        for word in ("AWS","GCP","Azure","Cloudflare","Boto3",
                     "ADC","DefaultAzureCredential","R2","D1","SOTA"):
            self.assertIn(word,doc)
        self.assertNotIn("AKIA1234567890123456",doc)

    def test_repo_validation(self):
        self.assertEqual(validate_repository(ROOT),[])


if __name__=="__main__":
    unittest.main()
