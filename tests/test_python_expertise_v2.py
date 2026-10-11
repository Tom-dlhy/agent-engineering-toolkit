"""Regression contract for progressively loaded Python and LLM expertise."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from toolkit.catalog import load_catalog, load_profile, search
from toolkit.knowledge import indexed_references, read_reference
from context_budget import estimate
from install_profile import install
from validate_skills import validate_repository


class PythonExpertiseV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.new = (
            "python-project-architecture",
            "python-http-clients",
            "python-persistence",
            "python-observability",
            "python-llm-gateways",
            "gcp-vertex-ai",
            "azure-ai-foundry",
        )
        cls.extended = (
            "modern-python",
            "fastapi-service",
            "llm-integration",
            "python-ddd",
            "hexagonal-architecture",
            "background-jobs",
        )

    def test_skills_and_count(self):
        self.assertEqual(len(self.catalog), 141)
        self.assertIn("aws-bedrock", self.catalog)
        for name in self.new + self.extended:
            self.assertIn(name, self.catalog)

    def test_all_python_references_are_real_and_indexed(self):
        total = 0
        for name in self.new + self.extended:
            with self.subTest(name=name):
                paths = indexed_references(self.catalog[name], ROOT)
                self.assertGreaterEqual(len(paths), 2)
                for path in paths:
                    body = read_reference(self.catalog[name], path, ROOT)
                    self.assertGreater(len(body), 1200)
                    self.assertIn("Read when:", body[:500])
                    self.assertIn("## ", body)
                    self.assertIn("https://", body)
                    total += 1
        self.assertEqual(total, 50)  # +2 AI provider/gateway reference leaves

    def test_provider_native_vs_gateway_routing(self):
        cases = {
            "Google Vertex AI Gemini google genai SDK": "gcp-vertex-ai",
            "Azure Foundry Entra Responses deployment": "azure-ai-foundry",
            "AWS Bedrock Converse model inference": "aws-bedrock",
            "LiteLLM Router multi provider gateway": "python-llm-gateways",
            "SQLAlchemy AsyncSession Alembic transaction": "python-persistence",
            "httpx AsyncClient outbound timeout": "python-http-clients",
            "Python opentelemetry correlation logging": "python-observability",
            "FastAPI lifespan dependency endpoint": "fastapi-service",
            "uv pyproject Python packaging": "modern-python",
            "DDD bounded aggregate Python": "python-ddd",
            "Python project architecture layout feature monolith": "python-project-architecture",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = search(query, self.catalog, limit=3)
                self.assertTrue(result)
                self.assertEqual(result[0].skill.name, expected)

    def test_negative_routes(self):
        cases = {
            "FastAPI Pydantic endpoint test": "fastapi-service",
            "Flutter Cupertino widget": "flutter-cupertino",
            "s3 bucket presigned upload": "aws-s3-storage",
        }
        for query, name in cases.items():
            with self.subTest(query=query):
                self.assertEqual(search(query, self.catalog, limit=1)[0].skill.name, name)

    def test_profiles_are_explicit_and_bounded(self):
        names = load_profile("python-llm-production", ROOT)
        self.assertLessEqual(len(names), 20)
        self.assertEqual(len(names), len(set(names)))
        for name in ("python-http-clients", "gcp-vertex-ai", "azure-ai-foundry", "python-llm-gateways"):
            self.assertIn(name, names)
        self.assertIn("python-persistence", load_profile("python-backend", ROOT))
        self.assertNotIn("python-llm-gateways", load_profile("minimal", ROOT))

    def test_context_leaves_only_explicit(self):
        base, _ = estimate("python-llm-production", ROOT)
        active, _ = estimate("python-llm-production", ROOT, ("python-llm-gateways",))
        selected, _ = estimate(
            "python-llm-production", ROOT, ("python-llm-gateways",),
            ("python-llm-gateways:references/litellm-routing.md",)
        )
        self.assertLess(base, active)
        self.assertLess(active, selected)
        with self.assertRaises(ValueError):
            estimate("python-llm-production", ROOT, (), ("python-llm-gateways:references/litellm-routing.md",))

    def test_allowlisted_reference_rejects_traversal(self):
        skill = self.catalog["gcp-vertex-ai"]
        for path in ("../SKILL.md", "references/../../README.md", "references/unknown.md"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                read_reference(skill, path, ROOT)

    def test_opt_in_installs_one_provider_with_leaves(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = install(None, "codex", Path(temp), apply=True, skills=("gcp-vertex-ai",))
            self.assertEqual(len(paths), 1)
            self.assertTrue((paths[0] / "references" / "google-genai-sdk.md").is_file())

    def test_readme_evidence(self):
        doc = (ROOT / "docs" / "python-engineering-v2.md").read_text(encoding="utf-8")
        for expected in ("LangChain", "LiteLLM", "Vertex", "Azure", "Bedrock", "PoC"):
            self.assertIn(expected, doc)

    def test_repository_structure(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
