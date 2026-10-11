"""Executable positive and negative tests for simple module import boundaries."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_architecture_boundaries import Rule, load_rules, scan

EXAMPLE = ROOT / "examples" / "architecture_boundaries"


class ImportBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(EXAMPLE / "boundaries.json")

    def test_example_allowed_public_contract(self):
        self.assertEqual(scan(EXAMPLE, self.rules), [])

    def test_absolute_private_import_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "example"
            shutil.copytree(EXAMPLE, directory)
            file = directory / "app/modules/orders/service.py"
            file.write_text(
                "from app.modules.billing import persistence\n", encoding="utf-8"
            )
            findings = scan(directory, self.rules)
            self.assertEqual(len(findings), 1)
            self.assertIn("app.modules.billing.persistence", findings[0])

    def test_relative_private_import_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "example"
            shutil.copytree(EXAMPLE, directory)
            file = directory / "app/modules/orders/service.py"
            file.write_text(
                "from ..billing.persistence import secret\n", encoding="utf-8"
            )
            findings = scan(directory, self.rules)
            self.assertEqual(len(findings), 1)
            self.assertIn("app.modules.billing.persistence", findings[0])

    def test_domain_vendor_import_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "example"
            shutil.copytree(EXAMPLE, directory)
            file = directory / "app/modules/billing/domain.py"
            file.write_text("import sqlalchemy.orm\n", encoding="utf-8")
            findings = scan(directory, self.rules)
            self.assertEqual(len(findings), 1)
            self.assertIn("sqlalchemy.orm", findings[0])

    def test_unrelated_module_has_no_rule(self):
        self.assertEqual(
            scan(EXAMPLE, (Rule("app.modules.unknown", ("fastapi",)),)), []
        )

    def test_invalid_rule_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"rules":[{"source":"app","forbidden":[]}]}')
            with self.assertRaises(ValueError):
                load_rules(path)

    def test_syntax_error_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "example"
            shutil.copytree(EXAMPLE, directory)
            file = directory / "app/modules/orders/service.py"
            file.write_text("def not_valid(:\n", encoding="utf-8")
            findings = scan(directory, self.rules)
            self.assertEqual(len(findings), 1)
            self.assertIn("invalid Python", findings[0])


if __name__ == "__main__":
    unittest.main()
