"""Progressive expertise requires local, explicitly selected leaf references."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from toolkit.catalog import load_catalog, search
from toolkit.knowledge import indexed_references, read_reference, resolve_reference
from context_budget import estimate
from validate_skills import validate_repository


class ProgressiveExpertiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)

    def test_expert_splits_expose_two_distinct_references(self):
        names = ("aws-integration", "aws-iam-security", "aws-s3-storage",
                 "aws-sqs-messaging", "aws-lambda-runtime", "aws-ecs-deployment",
                 "aws-bedrock")
        for name in names:
            with self.subTest(skill=name):
                refs = indexed_references(self.catalog[name], ROOT)
                self.assertGreaterEqual(len(refs), 2)
                for path in refs:
                    text = read_reference(self.catalog[name], path, ROOT)
                    self.assertIn("## ", text)
                    self.assertIn("Official", text)

    def test_traversal_and_unlisted_files_rejected(self):
        s3 = self.catalog["aws-s3-storage"]
        for ref in ("../SKILL.md", "references/../../SKILL.md",
                    "references/secret.md", "SKILL.md"):
            with self.subTest(ref=ref):
                with self.assertRaises(ValueError):
                    read_reference(s3, ref, ROOT)

    def test_symlinked_reference_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "skills" / "cloud" / "aws-s3-storage"
            (folder / "references").mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                "# Skill\n[leaf](references/leaf.md)\n", encoding="utf-8"
            )
            outside = root / "outside.md"
            outside.write_text("private", encoding="utf-8")
            (folder / "references" / "leaf.md").symlink_to(outside)
            with self.assertRaises(ValueError):
                resolve_reference(self.catalog["aws-s3-storage"], "references/leaf.md", root)

    def test_reference_budget_is_strictly_incremental(self):
        profile = "aws-platform"
        baseline, n = estimate(profile, ROOT)
        activated, _ = estimate(profile, ROOT, ("aws-s3-storage",))
        one_leaf, _ = estimate(profile, ROOT, ("aws-s3-storage",),
            ("aws-s3-storage:references/object-api-and-uploads.md",))
        self.assertEqual(n, 20)
        self.assertLess(baseline, activated)
        self.assertLess(activated, one_leaf)
        with self.assertRaises(ValueError):
            estimate(profile, ROOT, (), ("aws-s3-storage:references/object-api-and-uploads.md",))

    def test_routing_service_specialists(self):
        cases = {
            "AWS S3 presigned upload object": "aws-s3-storage",
            "AWS SQS FIFO DLQ queue": "aws-sqs-messaging",
            "AWS Lambda serverless handler concurrency": "aws-lambda-runtime",
            "AWS ECS Fargate task deployment": "aws-ecs-deployment",
            "AWS Bedrock Converse guardrails": "aws-bedrock",
            "AWS IAM OIDC trust policy": "aws-iam-security",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                found = search(query, self.catalog, limit=3)
                self.assertTrue(found)
                self.assertEqual(found[0].skill.name, expected)

    def test_negative_routing_fastapi_does_not_select_aws(self):
        found = search("FastAPI Pydantic endpoint test", self.catalog, limit=1)
        self.assertEqual(found[0].skill.name, "fastapi-service")

    def test_structural_validation(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
