"""Installer v2 safety, lifecycle and native-distribution integration contracts."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toolkit.managed_installer import ManagedInstaller, InstallError, generate_lock, read_lock, _assert_locked
from toolkit.plugin_packager import archive, build, verify


class InstallerV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / "source"
        self.project = self.base / "project"
        self.project.mkdir()
        (self.source / "skills" / "test" / "alpha").mkdir(parents=True)
        (self.source / "skills" / "test" / "beta").mkdir(parents=True)
        (self.source / "profiles").mkdir()
        (self.source / "registry").mkdir()
        self.alpha = self.source / "skills" / "test" / "alpha"
        self.beta = self.source / "skills" / "test" / "beta"
        (self.alpha / "SKILL.md").write_text("---\nname: alpha\n---\nAlpha", encoding="utf-8")
        (self.alpha / "references").mkdir()
        (self.alpha / "references" / "topic.md").write_text("reference", encoding="utf-8")
        (self.beta / "SKILL.md").write_text("---\nname: beta\n---\nBeta", encoding="utf-8")
        (self.source / "registry" / "skills.yaml").write_text(yaml.safe_dump({
            "skills": [
                {"name": "alpha", "path": "skills/test/alpha"},
                {"name": "beta", "path": "skills/test/beta"},
            ]
        }), encoding="utf-8")
        (self.source / "profiles" / "small.yaml").write_text(
            yaml.safe_dump({"skills": ["alpha"]}), encoding="utf-8")
        self.manager = ManagedInstaller(self.source, "codex", "project", self.project)

    def test_preview_is_read_only(self):
        plan = self.manager.plan("install", "small")
        self.assertEqual(plan["operations"][0]["action"], "add")
        self.assertFalse((self.project / ".aet").exists())
        self.assertFalse((self.project / ".agents").exists())

    def test_idempotent_incremental_and_cumulative_inventory(self):
        self.manager.apply("install", "small")
        target = self.project / ".agents/skills"
        self.assertTrue((target / "alpha/references/topic.md").is_file())
        self.assertEqual(self.manager.plan("install", "small")["operations"][0]["action"],
                         "unchanged")
        self.manager.apply("install", skills=("beta",))
        state = self.manager._state()
        self.assertEqual(state["selected"], ["alpha", "beta"])
        self.assertEqual(set(state["files"]), {"alpha", "beta"})
        self.manager.apply("install", skills=("beta",))
        self.assertEqual(len(self.manager.inspect()["installed"]), 2)

    def test_unmanaged_destination_is_never_claimed(self):
        target = self.project / ".agents/skills/alpha"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("user-owned", encoding="utf-8")
        plan = self.manager.plan("install", "small")
        self.assertEqual(plan["operations"][0]["action"], "conflict-unmanaged")
        with self.assertRaises(InstallError):
            self.manager.apply("install", "small")
        self.assertEqual((target / "SKILL.md").read_text(), "user-owned")

    def test_upgrade_and_preserve_edited_file(self):
        self.manager.apply("install", "small")
        dest = self.project / ".agents/skills/alpha/SKILL.md"
        (self.alpha / "SKILL.md").write_text("upstream new", encoding="utf-8")
        self.assertEqual(self.manager.plan("update")["operations"][0]["action"], "replace")
        dest.write_text("my customization", encoding="utf-8")
        self.assertEqual(self.manager.plan("update")["operations"][0]["action"],
                         "conflict-modified")
        with self.assertRaises(InstallError):
            self.manager.apply("update")
        self.assertEqual(dest.read_text(), "my customization")

    def test_changed_source_requires_update_not_repair(self):
        self.manager.apply("install", "small")
        (self.project / ".agents/skills/alpha").rename(self.project / "stash")
        (self.alpha / "SKILL.md").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(InstallError, "original source revision"):
            self.manager.apply("repair")

    def test_doctor_missing_and_repair(self):
        self.manager.apply("install", "small")
        dest = self.project / ".agents/skills/alpha"
        (dest / "references/topic.md").unlink()
        self.assertEqual(self.manager.inspect()["installed"]["alpha"], "missing-files")
        self.manager.apply("repair")
        self.assertEqual(self.manager.inspect()["installed"]["alpha"], "clean")

    def test_extra_file_blocks_update_and_uninstall(self):
        self.manager.apply("install", "small")
        extra = self.project / ".agents/skills/alpha/user.txt"
        extra.write_text("user", encoding="utf-8")
        for op in ("update", "uninstall", "repair"):
            with self.subTest(op=op):
                with self.assertRaises(InstallError):
                    self.manager.apply(op)
        self.assertEqual(extra.read_text(), "user")

    def test_selective_uninstall_and_safe_full_uninstall(self):
        self.manager.apply("install", skills=("alpha", "beta"))
        self.manager.apply("uninstall", skills=("alpha",))
        self.assertEqual(self.manager._state()["selected"], ["beta"])
        self.assertFalse((self.project / ".agents/skills/alpha").exists())
        self.assertTrue((self.project / ".agents/skills/beta").exists())
        self.manager.apply("uninstall")
        self.assertEqual(self.manager.inspect()["installed"], {})

    def test_deleted_skill_can_be_uninstalled_without_source(self):
        self.manager.apply("install", "small")
        (self.alpha / "SKILL.md").unlink()
        # The source is no longer in a usable form, but ownership still matters.
        self.manager.apply("uninstall")
        self.assertFalse((self.project / ".agents/skills/alpha").exists())

    def test_atomic_recovery_if_state_commit_fails(self):
        self.manager.apply("install", "small")
        dest = self.project / ".agents/skills/alpha/SKILL.md"
        original = dest.read_bytes()
        (self.alpha / "SKILL.md").write_text("new upstream", encoding="utf-8")
        writer = self.manager._write_json
        def fail_state(path, data):
            if path == self.manager.state_path:
                raise OSError("simulated disk failure")
            return writer(path, data)
        with patch.object(self.manager, "_write_json", side_effect=fail_state):
            with self.assertRaises(OSError):
                self.manager.apply("update")
        self.assertEqual(dest.read_bytes(), original)
        self.assertFalse(self.manager.journal.exists())
        self.assertEqual(self.manager.inspect()["installed"]["alpha"], "clean")

    def test_recover_interrupted_transaction_from_journal(self):
        self.manager.apply("install", "small")
        target = self.project / ".agents/skills/alpha"
        tx = self.manager.meta / ("tx-" + "a" * 32)
        (tx / "backups").mkdir(parents=True)
        target.rename(tx / "backups/alpha")
        target.mkdir()
        (target / "SKILL.md").write_text("partial", encoding="utf-8")
        state_backup = tx / "previous-state.json"
        self.manager.state_path.rename(state_backup)
        self.manager._write_json(self.manager.journal, {
            "transaction": tx.name, "had_state": True,
            "operations": [{"skill": "alpha", "had_original": True}],
        })
        self.manager.apply("install", "small")
        self.assertEqual(self.manager.inspect()["installed"]["alpha"], "clean")
        self.assertFalse(self.manager.journal.exists())

    def test_refuse_symlink_source_and_target(self):
        source_link = self.alpha / "leak"
        try:
            source_link.symlink_to(self.project, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with self.assertRaises(InstallError):
            self.manager.plan("install", "small")
        source_link.unlink()
        dest = self.project / ".agents"
        dest.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(InstallError):
            ManagedInstaller(self.source, "codex", "project", self.project)

    def test_reject_state_path_traversal(self):
        self.manager.meta.mkdir()
        self.manager._write_json(self.manager.state_path, {
            "schema": "aet.install.v2", "agent": "codex", "scope": "project",
            "selected": ["alpha"], "revision": "bogus",
            "files": {"alpha": {"../outside": "a" * 64, "SKILL.md": "b" * 64}},
        })
        with self.assertRaises(InstallError):
            self.manager.plan("uninstall")

    def test_user_scope_is_isolated(self):
        global_mgr = ManagedInstaller(self.source, "claude", "user", home=self.base)
        global_mgr.apply("install", skills=("beta",))
        self.assertTrue((self.base / ".claude/skills/beta/SKILL.md").is_file())
        self.assertFalse((self.project / ".claude").exists())

    def test_package_is_selective_verified_and_non_overwriting(self):
        target = self.base / "dist"
        record = build(self.source, target, "small", version="1.2.3")
        self.assertEqual(record["skills"], ["alpha"])
        self.assertEqual(verify(target)["version"], "1.2.3")
        pkg = target / "plugins/agent-engineering-toolkit"
        self.assertTrue((pkg / "plugin.json").is_file())
        self.assertTrue((pkg / ".codex-plugin/plugin.json").is_file())
        self.assertTrue((pkg / ".claude-plugin/plugin.json").is_file())
        self.assertFalse((pkg / "skills/beta").exists())
        self.assertIn("plugins", json.loads(
            (target / ".agents/plugins/marketplace.json").read_text()))
        with self.assertRaises(InstallError):
            build(self.source, target, "small")
        z = self.base / "package.zip"
        archive(target, z)
        self.assertTrue(z.is_file())

    def test_package_detects_drift_and_invalid_version(self):
        with self.assertRaises(InstallError):
            build(self.source, self.base / "invalid", "small", version="../../evil")
        package = self.base / "release"
        build(self.source, package, skills=("beta",), version="2.0.0")
        skill = package / "plugins/agent-engineering-toolkit/skills/beta/SKILL.md"
        skill.write_text("tampered", encoding="utf-8")
        with self.assertRaises(InstallError):
            verify(package)

    def test_package_reproducible_contents(self):
        first = self.base / "a"
        second = self.base / "b"
        build(self.source, first, "small", version="1.0.0")
        build(self.source, second, "small", version="1.0.0")
        self.assertEqual((first / "aet-distribution.json").read_bytes(),
                         (second / "aet-distribution.json").read_bytes())
        first_zip, second_zip = self.base / "one.zip", self.base / "two.zip"
        self.assertEqual(archive(first, first_zip), archive(second, second_zip))
        self.assertEqual(first_zip.read_bytes(), second_zip.read_bytes())


    def test_lockfile_pins_exact_bytes_and_selection(self):
        lock = generate_lock(self.source, "codex", "small")
        self.assertEqual(lock["selected"], ["alpha"])
        self.manager.meta.mkdir(parents=True, exist_ok=True)
        path = self.manager.meta / "skills-lock-codex.json"
        self.manager._write_json(path, lock)
        loaded = read_lock(path, "codex")
        _assert_locked(self.manager.plan("install", skills=("alpha",)), loaded)
        self.manager.apply("install", skills=("alpha",), lock=loaded)
        (self.alpha / "SKILL.md").write_text("upstream changed", encoding="utf-8")
        with self.assertRaisesRegex(InstallError, "source differs"):
            self.manager.apply("update", skills=("alpha",), lock=loaded)
        self.assertEqual(self.manager.inspect()["installed"]["alpha"], "clean")

    def test_lockfile_rejects_wrong_agent_and_traversal(self):
        lock = generate_lock(self.source, "codex", skills=("beta",))
        self.manager.meta.mkdir(parents=True, exist_ok=True)
        path = self.manager.meta / "skills-lock-codex.json"
        self.manager._write_json(path, lock)
        with self.assertRaises(InstallError):
            read_lock(path, "claude")
        lock["files"]["beta"]["../outside"] = "f" * 64
        self.manager._write_json(path, lock)
        with self.assertRaises(InstallError):
            read_lock(path, "codex")


    def test_named_plugin_variants_are_independent(self):
        out1, out2 = self.base / "variant-a", self.base / "variant-b"
        build(self.source, out1, "small", version="1.0.0", name="aet-alpha")
        build(self.source, out2, skills=("beta",), version="1.0.0", name="aet-beta")
        self.assertTrue(verify(out1)["valid"])
        self.assertTrue(verify(out2)["valid"])
        meta1 = json.loads((out1 / ".agents/plugins/marketplace.json").read_text())
        meta2 = json.loads((out2 / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(meta1["plugins"][0]["name"], "aet-alpha")
        self.assertEqual(meta2["plugins"][0]["name"], "aet-beta")

    def test_real_repo_minimal_profile_packaged(self):
        output = self.base / "real-dist"
        build(ROOT, output, "minimal", version="0.1.0", name="aet-smoke")
        self.assertTrue(verify(output)["valid"])


    def test_live_probe_package_and_no_prompt_token_leak(self):
        from scripts.native_agent_smoke import prepare, PROMPT, TOKEN
        self.assertNotIn(TOKEN, PROMPT)
        output = self.base / "native-probe"
        prepared = prepare(output)
        self.assertEqual(prepared["skills"], ["aet-activation-probe"])
        self.assertTrue(verify(output)["valid"])
        probe = output / "plugins/agent-engineering-toolkit/skills/aet-activation-probe/SKILL.md"
        self.assertIn(TOKEN, probe.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
