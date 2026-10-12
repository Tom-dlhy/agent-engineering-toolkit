"""Evidence snapshot, integrity and simulated A/B/C execution (no model calls)."""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toolkit.benchmark_model import BenchmarkError, inventory, load_suite
from toolkit.benchmark_evidence import (
    MAX_FILE_BYTES, snapshot, store, verify, verify_records)
from toolkit.benchmark_runner import execute
from toolkit.benchmark_analysis import analyze


class EvidenceTests(unittest.TestCase):
    def test_changed_added_deleted_and_binary_are_reviewable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            work = root / "work"
            work.mkdir()
            (work / "kept.py").write_text("OLD\n")
            (work / "removed.txt").write_text("gone\n")
            (work / "binary.bin").write_bytes(b"\x00\xff")
            before = snapshot(work)
            (work / "kept.py").write_text("NEW\n")
            (work / "removed.txt").unlink()
            (work / "new.txt").write_text("hello\n")
            (work / "binary.bin").write_bytes(b"\x00\xfe")
            after = snapshot(work)
            run_id = str(uuid.uuid4())
            output = root / "report"
            output.mkdir(mode=0o700)
            evidence = store(output, run_id, before, after)
            row = {"run_id": run_id, "artifact_evidence": evidence}
            self.assertEqual(evidence["status"], "CAPTURED")
            self.assertEqual(evidence["changed_paths"],
                             ["binary.bin", "kept.py", "new.txt", "removed.txt"])
            self.assertTrue(verify(output, row))
            folder = output / "artifacts" / run_id
            self.assertEqual((folder / "before/kept.py").read_bytes(), b"OLD\n")
            self.assertEqual((folder / "after/kept.py").read_bytes(), b"NEW\n")
            self.assertFalse((folder / "after/removed.txt").exists())
            self.assertIn("--- a/kept.py", (folder / "changes.patch").read_text())
            self.assertIn("Binary change", (folder / "changes.patch").read_text())
            (folder / "after/kept.py").write_text("TAMPER")
            self.assertFalse(verify(output, row))

    def test_detects_manifest_tampering_and_extra_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / "out"
            output.mkdir()
            run_id = str(uuid.uuid4())
            evidence = store(output, run_id, {"a.txt": b"old"}, {"a.txt": b"new"})
            record = {"run_id": run_id, "artifact_evidence": evidence}
            folder = output / "artifacts" / run_id
            (folder / "intruder").write_text("surprise")
            self.assertFalse(verify(output, record))
            (folder / "intruder").unlink()
            self.assertTrue(verify(output, record))
            (folder / "manifest.json").write_text("{}")
            self.assertFalse(verify(output, record))

    def test_does_not_archive_secrets_links_or_special_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".env.production").write_text("PASSWORD=secret")
            with self.assertRaises(BenchmarkError):
                snapshot(root)
            (root / ".env.production").unlink()
            (root / "key.txt").write_text("-----BEGIN RSA PRIVATE KEY-----\nSECRET")
            with self.assertRaises(BenchmarkError):
                snapshot(root)
            (root / "key.txt").unlink()
            (root / "big.dat").write_bytes(b"A" * (MAX_FILE_BYTES + 1))
            with self.assertRaises(BenchmarkError):
                snapshot(root)
            (root / "big.dat").unlink()
            (root / "safe.py").write_text("print('safe')")
            (root / "link").symlink_to(root / "safe.py")
            with self.assertRaises(BenchmarkError):
                snapshot(root)
            (root / "link").unlink()
            os.link(root / "safe.py", root / "hardlink.py")
            with self.assertRaises(BenchmarkError):
                snapshot(root)

    def test_excludes_installed_agent_scaffolding_and_test_caches(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "src").mkdir()
            (root / "src/app.py").write_text("ok")
            (root / ".agents/skills/testing").mkdir(parents=True)
            (root / ".agents/skills/testing/SKILL.md").write_text("method")
            (root / "__pycache__").mkdir()
            (root / "__pycache__/app.pyc").write_bytes(b"cache")
            self.assertEqual(sorted(snapshot(root)), ["src/app.py"])

    def test_verified_report_copy_no_overwrite_or_fake_review(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td)
            run_id = str(uuid.uuid4())
            evidence = store(output, run_id, {"file": b"old"}, {"file": b"new"})
            data = [{"run_id": run_id, "artifact_evidence": evidence,
                     "human_review": "NOT_REVIEWED", "critical_violation": None}]
            raw = output / "records.json"
            raw.write_text(json.dumps(data))
            dest = output / "verified-records.json"
            result = verify_records(raw, dest)
            self.assertEqual(result["verified"], 1)
            self.assertFalse(json.loads(raw.read_text())[0].get("artifact_evidence_verified", False))
            reviewed = json.loads(dest.read_text())
            self.assertTrue(reviewed[0]["artifact_evidence_verified"])
            self.assertEqual(reviewed[0]["human_review"], "NOT_REVIEWED")
            with self.assertRaises(BenchmarkError):
                verify_records(raw, dest)

    def test_symlinked_evidence_directory_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "artifacts").mkdir()
            run_id = str(uuid.uuid4())
            (root / "artifacts" / run_id).symlink_to(root)
            row = {"run_id": run_id, "artifact_evidence": {
                "status": "CAPTURED", "manifest_sha256": "a" * 64,
                "directory": f"artifacts/{run_id}"}}
            self.assertFalse(verify(root, row))


class SimulatedNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        suite = load_suite(ROOT / "evals/benchmark/example.json", ROOT)
        task = suite.tasks[0]
        digest, _ = inventory(task.fixture_dir)
        cls.suite = replace(suite, tasks=(replace(task, fixture_sha256=digest),))

    def _simulate(self, output: Path, *, test_modifies_source: bool = True,
                  fail_agent: bool = False):
        called = []
        def fake_subprocess(argv, cwd, timeout):
            path = Path(cwd) / "string_ops.py"
            if "exec" in argv:
                called.append("agent")
                if fail_agent:
                    return subprocess.CompletedProcess(argv, 1, '{"type":"turn.failed"}', "")
                path.write_text('def normalize_email(raw: str) -> str:\n'
                                '    return raw.strip().lower()\n')
                return subprocess.CompletedProcess(
                    argv, 0, '{"type":"turn.completed","usage":'
                             '{"input_tokens":8,"output_tokens":4}}', "")
            called.append("acceptance")
            if test_modifies_source:
                path.write_text("TEST MODIFIED THIS FILE")
            return subprocess.CompletedProcess(argv, 0, "tests pass", "")
        with mock.patch("toolkit.benchmark_runner.shutil.which", return_value="/usr/bin/codex"), \
             mock.patch("toolkit.benchmark_runner._run", side_effect=fake_subprocess):
            result = execute(
                self.suite, ROOT, host="codex", model="pinned-model",
                trials=1, output=output, allow_paid=True, allow_tests=True,
                trusted_host=True, max_runs=3, timeout=20, max_total_seconds=120)
        return result, called

    def test_all_arms_preserve_model_patch_before_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "benchmark"
            result, calls = self._simulate(root)
            self.assertEqual(result["completed"], 3)
            self.assertEqual(calls.count("agent"), 3)
            self.assertEqual(calls.count("acceptance"), 3)
            records = json.loads((root / "records.json").read_text())
            self.assertEqual(len(records), 3)
            self.assertEqual({r["variant"] for r in records},
                             {"baseline", "knowledge", "full"})
            for r in records:
                self.assertFalse(r["artifact_evidence_verified"])
                self.assertTrue(verify(root, r))
                self.assertEqual(r["artifact_evidence"]["status"], "CAPTURED")
                self.assertEqual(r["test_status"], "PASS")
                self.assertEqual(r["tokens"], 12)
                stored = (root / "artifacts" / r["run_id"] /
                          "after/string_ops.py").read_text()
                self.assertIn("raw.strip().lower()", stored)
                self.assertNotIn("TEST MODIFIED", stored)
            verified = root / "verified.json"
            summary = verify_records(root / "records.json", verified)
            self.assertEqual(summary["verified"], 3)
            rows = json.loads(verified.read_text())
            self.assertEqual(analyze(rows, min_trials=1)["promotion"],
                             "INSUFFICIENT_EVIDENCE")
            # Integrity verification is not human review. Only independent
            # reviewers can classify results and critical vulnerabilities.
            for row in rows:
                row["human_review"] = "PASS"
                row["critical_violation"] = False
            self.assertEqual(analyze(rows, min_trials=1)["promotion"],
                             "CANDIDATE_FOR_HUMAN_APPROVAL")

    def test_agent_failure_still_retains_artifacts_and_no_test(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "benchmark"
            result, calls = self._simulate(root, fail_agent=True)
            self.assertEqual(result["completed"], 3)
            self.assertNotIn("acceptance", calls)
            rows = json.loads((root / "records.json").read_text())
            for row in rows:
                self.assertEqual(row["test_status"], "NOT_RUN")
                self.assertEqual(row["agent_status"], "FAIL")
                self.assertTrue(verify(root, row))

    def test_generated_secret_blocks_evidence_and_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "bench"
            def malicious(argv, cwd, timeout):
                self.assertIn("exec", argv)
                (Path(cwd) / ".env.production").write_text("TOKEN=secret")
                return subprocess.CompletedProcess(argv, 0, "{}", "")
            with mock.patch("toolkit.benchmark_runner.shutil.which", return_value="/usr/bin/codex"), \
                 mock.patch("toolkit.benchmark_runner._run", side_effect=malicious) as run:
                result = execute(self.suite, ROOT, host="codex", model="m",
                    trials=1, output=out, allow_paid=True, allow_tests=True,
                    trusted_host=True, max_runs=3, timeout=20, max_total_seconds=120)
            self.assertEqual(run.call_count, 3)  # no acceptance commands
            self.assertEqual(result["completed"], 3)
            for row in json.loads((out / "records.json").read_text()):
                self.assertEqual(row["artifact_evidence"]["status"], "BLOCKED")
                self.assertEqual(row["test_status"], "BLOCKED")
                self.assertFalse(verify(out, row))


if __name__ == "__main__":
    unittest.main()
