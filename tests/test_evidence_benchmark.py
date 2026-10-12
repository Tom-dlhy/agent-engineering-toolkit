"""Contract, negative, budget and simulated runner tests. No paid calls."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from toolkit.benchmark_model import BenchmarkError, inventory, load_suite
from toolkit.benchmark_runner import _usage, _stage, _artifacts, execute, plan
from toolkit.benchmark_analysis import analyze


def case(variant: str, trial: int = 0, **override):
    r = dict(task_id="task-one", trial=trial, variant=variant,
             suite_sha256="suite-a", fixture_sha256="fixture-a",
             host="codex", model="pinned-model", tool_config="bounded",
             run_id=f"{variant}-{trial}", agent_status="PASS",
             test_status="PASS", tokens=100, human_review="PASS",
             critical_violation=False)
    return {**r, **override}


def trio(trial=0, **by_variant):
    return [case(v, trial, **by_variant.get(v, {})) for v in
            ("baseline", "knowledge", "full")]


class AnalysisTests(unittest.TestCase):
    def test_passed_two_trials_still_require_owner_promotion(self):
        result = analyze(trio(0) + trio(1))
        self.assertEqual(result["promotion"], "CANDIDATE_FOR_HUMAN_APPROVAL")
        self.assertTrue(result["never_auto_promote"])
        self.assertEqual(result["n_trials"], 2)

    def test_critical_risk_beats_token_savings(self):
        result = analyze(trio(0, full={"critical_violation": True, "tokens": 12}) +
                         trio(1))
        self.assertEqual(result["promotion"], "NO_GO_CRITICAL_FINDING")
        self.assertEqual(result["new_critical_regressions_full_vs_baseline"], 1)

    def test_human_review_and_unrun_tests_block(self):
        records = trio(0) + trio(1)
        records[0]["human_review"] = "NOT_REVIEWED"
        self.assertEqual(analyze(records)["promotion"], "INSUFFICIENT_EVIDENCE")
        records[0]["human_review"] = "PASS"
        records[1]["critical_violation"] = None
        self.assertEqual(analyze(records)["promotion"], "INSUFFICIENT_EVIDENCE")
        records[1]["critical_violation"] = False
        records[1]["test_status"] = "NOT_RUN"
        self.assertEqual(analyze(records)["promotion"], "INSUFFICIENT_EVIDENCE")

    def test_no_fabricated_token_improvement(self):
        records = trio(0) + trio(1)
        records[0]["tokens"] = None
        result = analyze(records, max_token_increase_pct=20)
        self.assertIsNone(result["token_change_pct_full_vs_baseline"])
        self.assertEqual(result["promotion"], "NO_GO_COST_THRESHOLD_OR_UNMEASURED")

    def test_cost_and_quality_gates(self):
        records = trio(0) + trio(1)
        for r in records:
            if r["variant"] == "full":
                r["tokens"] = 125
        self.assertEqual(analyze(records, max_token_increase_pct=20)["promotion"],
                         "NO_GO_COST_THRESHOLD_OR_UNMEASURED")
        self.assertEqual(analyze(records, min_success_delta=.1)["promotion"],
                         "NO_GO_QUALITY_THRESHOLD")

    def test_reject_missing_mismatched_and_duplicate_arms(self):
        for records in (
            trio(0)[:2], trio(0) + trio(0),
            trio(0, knowledge={"fixture_sha256": "different"}),
            trio(0, knowledge={"model": "other"}),
            trio(0, knowledge={"run_id": "baseline-0"}),
            trio(0, full={"tokens": -1}),
            trio(0, full={"critical_violation": "false"}),
            trio(0, full={"trial": True}),
        ):
            with self.subTest(records=repr(records)[:120]):
                with self.assertRaises(BenchmarkError):
                    analyze(records)

    def test_all_variants_and_minimum_repeatability(self):
        result = analyze(trio(0))
        self.assertEqual(result["promotion"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(set(result["arms"]), {"baseline", "knowledge", "full"})


class ManifestTests(unittest.TestCase):
    def test_example_suite_offline_and_model_is_explicit(self):
        suite = load_suite(ROOT / "evals/benchmark/example.json", ROOT)
        self.assertEqual(len(suite.tasks), 1)
        self.assertIsNone(suite.tasks[0].fixture_sha256)
        info = plan(suite, ROOT, host="codex", model="pinned-model", trials=2)
        self.assertEqual(info["total_runs"], 6)
        self.assertEqual(len(info["run_order"]), 6)
        self.assertEqual(len({tuple(x) for x in info["run_order"]}), 6)

    def test_fixture_tampering_and_symlinks_rejected(self):
        suite = load_suite(ROOT / "evals/benchmark/example.json", ROOT)
        sha, _ = inventory(suite.tasks[0].fixture_dir)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "fixture").mkdir()
            (root / "fixture" / "a.py").write_text("print('ok')")
            stable, _ = inventory(root / "fixture")
            (root / "fixture" / "a.py").write_text("print('changed')")
            changed, _ = inventory(root / "fixture")
            self.assertNotEqual(stable, changed)
            (root / "fixture" / "linked").symlink_to(root / "fixture" / "a.py")
            with self.assertRaises(BenchmarkError):
                inventory(root / "fixture")
        self.assertEqual(len(sha), 64)

    def test_invalid_manifest_and_hidden_credential_path(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "evals") as temp:
            path = Path(temp) / "bad.json"
            path.write_text(json.dumps({"version": 1, "tasks": [
                {"id": "bad", "prompt": "Some long enough prompt",
                 "fixture_dir": "evals/../.env", "technical_skills": [],
                 "check_argv": ["python"], "expected": "Should pass or fail"}]}))
            with self.assertRaises(BenchmarkError):
                load_suite(path, ROOT)

    def test_staging_does_not_mutate_fixture_and_arms_differ(self):
        suite = load_suite(ROOT / "evals/benchmark/example.json", ROOT)
        task = suite.tasks[0]
        digest, _ = inventory(task.fixture_dir)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mounted = _stage(task, root, ROOT, "codex", "baseline", digest)
            self.assertEqual(mounted, [])
            self.assertFalse((root / ".agents").exists())
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            selected = _stage(task, root, ROOT, "codex", "knowledge", digest)
            self.assertEqual(selected, list(task.technical_skills))
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertTrue((root / ".agents/skills/systematic-debugging/SKILL.md").is_file())
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            selected = _stage(task, root, ROOT, "claude", "full", digest)
            self.assertIn("task-routing", selected)
            self.assertTrue((root / "CLAUDE.md").is_file())
            self.assertTrue((root / ".claude/skills/test-strategy/SKILL.md").is_file())

    def test_artifact_guard_refuses_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "safe.py").write_text("ok")
            a, names = _artifacts(d)
            self.assertEqual(names, ["safe.py"])
            (d / "link").symlink_to(d / "safe.py")
            with self.assertRaises(BenchmarkError):
                _artifacts(d)


class NativeSafetyTests(unittest.TestCase):
    def test_unknown_usage_is_never_guessed(self):
        self.assertIsNone(_usage("codex", '{"type":"turn.completed"}'))
        self.assertIsNone(_usage("claude", '{"message":"finished"}'))
        self.assertEqual(_usage("codex",
            '{"type":"turn.completed","usage":{"input_tokens":8,"output_tokens":4}}'), 12)
        self.assertEqual(_usage("claude",
            '{"usage":{"input_tokens":6,"output_tokens":3}}'), 9)

    def test_no_native_run_without_three_opt_ins_and_pinned_digest(self):
        suite = load_suite(ROOT / "evals/benchmark/example.json", ROOT)
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "report"
            with mock.patch("toolkit.benchmark_runner._run") as sub:
                with self.assertRaises(BenchmarkError):
                    execute(suite, ROOT, host="codex", model="m", trials=1,
                            output=report, allow_paid=True, allow_tests=False,
                            trusted_host=True, max_runs=3, timeout=90,
                            max_total_seconds=180)
                with self.assertRaises(BenchmarkError):
                    execute(suite, ROOT, host="codex", model="m", trials=1,
                            output=report, allow_paid=True, allow_tests=True,
                            trusted_host=True, max_runs=2, timeout=90,
                            max_total_seconds=180)
                # Absent fixture digest is a blocker even if every approval flag is set.
                with self.assertRaises(BenchmarkError):
                    execute(suite, ROOT, host="codex", model="m", trials=1,
                            output=report, allow_paid=True, allow_tests=True,
                            trusted_host=True, max_runs=3, timeout=90,
                            max_total_seconds=180)
                sub.assert_not_called()
                self.assertFalse(report.exists())


if __name__ == "__main__":
    unittest.main()
