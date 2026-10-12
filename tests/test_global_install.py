"""Global single-gateway installation: inventory, safety and lifecycle."""
from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from toolkit.global_install import build_source, run
from toolkit.managed_installer import InstallError, ManagedInstaller, _files

ROOT = Path(__file__).resolve().parents[1]


class GlobalGatewayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        env = patch.dict(os.environ, {"AET_TRUST_HOME": str(self.base / "trust")})
        env.start()
        self.addCleanup(env.stop)
        self.home = self.base / "user"
        self.home.mkdir()
        self.source = self.base / "source"
        (self.source / "registry").mkdir(parents=True)
        for domain, name, description in (
            ("core", "task-routing", "Use when routing uncertain work. Do not use for a typo."),
            ("backend", "fastapi-service", "Use when implementing a FastAPI endpoint."),
        ):
            base = self.source / "skills" / domain / name
            (base / "references").mkdir(parents=True)
            (base / "SKILL.md").write_text(
                f"---\nname: {name}\ndomain: {domain}\n"
                f"description: {description}\n---\n\n# {name}\n",
                encoding="utf-8",
            )
            (base / "references/topic.md").write_text(
                f"# {name} reference\n", encoding="utf-8"
            )
        (self.source / "registry/skills.yaml").write_text(yaml.safe_dump({
            "version": 1, "skills": [
                {"name": "task-routing", "domain": "core",
                 "path": "skills/core/task-routing", "keywords": []},
                {"name": "fastapi-service", "domain": "backend",
                 "path": "skills/backend/fastapi-service", "keywords": []},
            ],
        }), encoding="utf-8")
        template = self.source / "templates/aet-global/SKILL.md"
        template.parent.mkdir(parents=True)
        template.write_text((ROOT / "templates/aet-global/SKILL.md").read_text(),
                            encoding="utf-8")

    def test_bundle_exposes_exactly_one_native_skill(self):
        bundle = self.base / "bundle"
        result = build_source(self.source, bundle)
        self.assertEqual(result["specialists"], 2)
        skill = bundle / "skills/core/aet"
        self.assertEqual([p.relative_to(skill).as_posix()
                          for p in skill.rglob("SKILL.md")], ["SKILL.md"])
        self.assertTrue((skill / "library/core/task-routing/GUIDE.md").is_file())
        self.assertTrue((skill / "library/backend/fastapi-service/GUIDE.md").is_file())
        self.assertTrue((skill / "library/backend/fastapi-service/references/topic.md").is_file())
        self.assertEqual(
            (skill / "library/backend/fastapi-service/GUIDE.md").read_bytes(),
            (self.source / "skills/backend/fastapi-service/SKILL.md").read_bytes(),
        )
        self.assertIn("fastapi-service", (skill / "index/backend.md").read_text())
        self.assertIn("Do not use for a typo",
                      (skill / "index/core.md").read_text())
        self.assertEqual(len(_files(skill)), 8)
        self.assertFalse((bundle / "skills/backend/fastapi-service").exists())

    def test_preview_is_read_only_and_install_is_global_both_hosts(self):
        preview, code = run("plan", ("codex", "claude"),
                            source=self.source, home=self.home)
        self.assertEqual(code, 0)
        self.assertFalse(preview["applied"])
        self.assertFalse((self.home / ".aet").exists())
        self.assertFalse((self.home / ".agents").exists())
        result, code = run("install", ("codex", "claude"),
                           source=self.source, home=self.home, apply=True)
        self.assertEqual(code, 0)
        self.assertTrue(result["applied"])
        for path in (".agents/skills/aet", ".claude/skills/aet"):
            self.assertTrue((self.home / path / "SKILL.md").is_file())
            self.assertTrue((self.home / path / "index/INDEX.md").is_file())
        self.assertFalse((self.home / ".agents/skills/fastapi-service").exists())
        report, code = run("doctor", ("codex", "claude"),
                           source=self.source, home=self.home)
        self.assertEqual(code, 0)
        self.assertTrue(all(x["gateway_installed"]
                            for x in report["agents"].values()))

    def test_update_and_uninstall_manage_only_owned_files(self):
        run("install", ("codex",), source=self.source, home=self.home, apply=True)
        guide = self.home / ".agents/skills/aet/library/backend/fastapi-service/GUIDE.md"
        src = self.source / "skills/backend/fastapi-service/SKILL.md"
        src.write_text(src.read_text() + "\nImproved feature guidance.\n")
        result, code = run("update", ("codex",), source=self.source,
                           home=self.home, apply=True)
        self.assertEqual(code, 0)
        self.assertTrue(result["applied"])
        self.assertIn("Improved feature guidance", guide.read_text())
        run("uninstall", ("codex",), source=self.source,
            home=self.home, apply=True)
        self.assertFalse((self.home / ".agents/skills/aet").exists())

    def test_modified_gateway_blocks_update_or_removal(self):
        run("install", ("codex",), source=self.source, home=self.home, apply=True)
        guide = self.home / ".agents/skills/aet/index/backend.md"
        guide.write_text("user local edit", encoding="utf-8")
        for operation in ("update", "uninstall"):
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(InstallError, "conflicts"):
                    run(operation, ("codex",), source=self.source,
                        home=self.home, apply=True)
        self.assertEqual(guide.read_text(), "user local edit")
        report, code = run("doctor", ("codex",),
                           source=self.source, home=self.home)
        self.assertEqual(code, 2)
        self.assertEqual(report["agents"]["codex"]["installed"]["aet"], "modified")

    def test_unmanaged_gateway_conflict_preflights_both_hosts(self):
        foreign = self.home / ".agents/skills/aet"
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text("user owned")
        with self.assertRaisesRegex(InstallError, "conflicts"):
            run("install", ("claude", "codex"), source=self.source,
                home=self.home, apply=True)
        self.assertEqual((foreign / "SKILL.md").read_text(), "user owned")
        self.assertFalse((self.home / ".claude").exists())

    def test_existing_user_profile_must_be_migrated_explicitly(self):
        old = ManagedInstaller(self.source, "codex", "user", home=self.home)
        old.apply("install", skills=("fastapi-service",))
        with self.assertRaisesRegex(InstallError, "migrate explicitly"):
            run("install", ("codex",), source=self.source,
                home=self.home, apply=True)
        self.assertTrue((self.home / ".agents/skills/fastapi-service/SKILL.md").exists())
        self.assertFalse((self.home / ".agents/skills/aet").exists())

    def test_missing_gateway_is_not_reported_as_healthy(self):
        result, code = run("doctor", ("codex",), source=self.source, home=self.home)
        self.assertEqual(code, 2)
        self.assertFalse(result["agents"]["codex"]["gateway_installed"])

    def test_real_repository_catalog_is_bundled_without_native_expansion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata = build_source(ROOT, root)
            self.assertEqual(metadata["specialists"], 178)
            gateway = root / "skills/core/aet"
            self.assertEqual(len(list(gateway.rglob("SKILL.md"))), 1)
            self.assertEqual(len(list(gateway.rglob("GUIDE.md"))), 178)
            self.assertTrue((gateway / "index/INDEX.md").is_file())
            self.assertTrue((gateway / "library/core/task-routing/GUIDE.md").is_file())


if __name__ == "__main__":
    unittest.main()
