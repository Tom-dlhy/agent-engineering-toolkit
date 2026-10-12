"""Opt-in native A/B/C benchmark runner. NOT a security sandbox.

Real CLIs may access the host's accounts, configuration, network or plugins.
Use only on a separate disposable trusted host with reviewed fixtures.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import time
import uuid

from .benchmark_model import BenchmarkError, Suite, Task, VARIANTS, inventory
from .catalog import load_catalog

FULL_METHODS = ("task-routing", "verification-before-done",
                "implementation-planning", "test-strategy")


def _run(argv: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess:
    """Never invoke a shell or interpolate untrusted commands."""
    return subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, errors="replace", timeout=timeout, check=False)


def _usage(host: str, output: str) -> int | None:
    """Only accept observed CLI JSON counters; never infer token cost."""
    if host == "claude":
        try:
            event = json.loads(output)
            usage = event.get("usage", {})
            a, b = usage.get("input_tokens"), usage.get("output_tokens")
            if type(a) is int and a >= 0 and type(b) is int and b >= 0:
                return a + b
        except (ValueError, AttributeError):
            pass
    if host == "codex":
        for line in reversed(output.splitlines()):
            try:
                event = json.loads(line)
                if event.get("type") != "turn.completed":
                    continue
                usage = event.get("usage", {})
                a, b = usage.get("input_tokens"), usage.get("output_tokens")
                if type(a) is int and a >= 0 and type(b) is int and b >= 0:
                    return a + b
            except (ValueError, AttributeError):
                continue
    return None


def _safe_copy(source: Path, dest: Path) -> None:
    if source.is_symlink() or not source.is_dir():
        raise BenchmarkError("invalid skill source")
    for path in source.rglob("*"):
        if path.is_symlink():
            raise BenchmarkError("linked skill source is forbidden")
        target = dest / path.relative_to(source)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        else:
            raise BenchmarkError("special skill files are forbidden")


def _stage(task: Task, workspace: Path, root: Path, host: str,
           variant: str, original_sha: str) -> list[str]:
    digest, files = inventory(task.fixture_dir)
    if digest != original_sha:
        raise BenchmarkError("source fixture changed during a trial")
    for rel, payload in files:
        path = workspace / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    if variant == "baseline":
        return []
    catalog = load_catalog(root)
    selected = list(task.technical_skills)
    if variant == "full":
        selected += [n for n in FULL_METHODS if n not in selected]
    for name in selected:
        if name not in catalog:
            raise BenchmarkError(f"unavailable skill: {name}")
    skills_dir = workspace / (".agents/skills" if host == "codex" else ".claude/skills")
    for name in selected:
        _safe_copy(root / catalog[name].path, skills_dir / name)
    if variant == "full":
        contract = (root / "AGENTS.md").read_text(encoding="utf-8")
        (workspace / ("AGENTS.md" if host == "codex" else "CLAUDE.md")).write_text(
            "# AET benchmark method\n\n" + contract, encoding="utf-8")
    return selected


def _artifacts(workspace: Path) -> tuple[str, list[str]]:
    h = hashlib.sha256()
    files = []
    for p in sorted(workspace.rglob("*")):
        if p.is_symlink():
            raise BenchmarkError("agent introduced linked file; cannot grade")
        if not p.is_file():
            continue
        rel = p.relative_to(workspace)
        if rel.parts[0] in (".agents", ".claude", ".git", ".aet"):
            continue
        if any(x.startswith(".env") for x in rel.parts):
            raise BenchmarkError("agent generated sensitive environment file")
        if p.stat().st_size > 2_000_000:
            raise BenchmarkError("large artifact needs manual inspection")
        blob = p.read_bytes()
        h.update(rel.as_posix().encode() + b"\0" + blob + b"\0")
        files.append(rel.as_posix())
    return h.hexdigest(), files


def _command(host: str, model: str, prompt: str) -> list[str]:
    binary = shutil.which(host)
    if binary is None:
        raise BenchmarkError("native CLI not available: " + host)
    if host == "codex":
        return [binary, "exec", "--skip-git-repo-check", "--sandbox",
                "workspace-write", "--json", "--model", model, prompt]
    if host == "claude":
        return [binary, "-p", prompt, "--output-format", "json",
                "--permission-mode", "dontAsk", "--allowedTools",
                "Read,Edit,Write,Glob,Grep", "--model", model, "--max-turns", "12"]
    raise BenchmarkError("unsupported agent host")


def plan(suite: Suite, root: Path, *, host: str, model: str,
         trials: int, seed: int = 42) -> dict:
    if host not in ("claude", "codex") or not isinstance(model, str) or not model.strip():
        raise BenchmarkError("choose codex/claude and explicit model")
    if type(trials) is not int or not 1 <= trials <= 10:
        raise BenchmarkError("trial count must be 1..10")
    catalog = load_catalog(root)
    fixtures = {}
    for task in suite.tasks:
        if any(name not in catalog for name in task.technical_skills):
            raise BenchmarkError(f"missing technical skill for {task.id}")
        fixtures[task.id] = inventory(task.fixture_dir)[0]
    order = [(t.id, n, v) for t in suite.tasks for n in range(trials) for v in VARIANTS]
    random.Random(seed).shuffle(order)
    return {"suite_sha256": suite.sha256, "model": model, "host": host,
            "tool_config": host + "-bounded-workspace-v1",
            "fixtures": fixtures, "trials": trials, "total_runs": len(order),
            "run_order": order, "unverified": True,
            "warning": "Host CLI can access host credentials, plugins and network; "
                       "a temporary folder is NOT an OS sandbox."}


def execute(suite: Suite, root: Path, *, host: str, model: str, trials: int,
            output: Path, allow_paid: bool, allow_tests: bool, trusted_host: bool,
            max_runs: int, timeout: int, max_total_seconds: int,
            seed: int = 42) -> dict:
    p = plan(suite, root, host=host, model=model, trials=trials, seed=seed)
    if not (allow_paid and allow_tests and trusted_host):
        raise BenchmarkError("paid runs require three explicit opt-ins")
    if (type(max_runs) is not int or not 1 <= max_runs <= 90
        or p["total_runs"] > max_runs or type(timeout) is not int
        or not 10 <= timeout <= 600 or type(max_total_seconds) is not int
        or not 30 <= max_total_seconds <= 7200):
        raise BenchmarkError("run/time limits exceeded")
    if any(t.fixture_sha256 is None for t in suite.tasks):
        raise BenchmarkError("paid runs need pinned fixture_sha256 per task")
    if output.exists() or output.is_symlink():
        raise BenchmarkError("refusing to overwrite an existing report")
    if shutil.which(host) is None:
        raise BenchmarkError("host executable not installed")
    output.mkdir(parents=True, mode=0o700)
    output.chmod(0o700)
    started = time.monotonic()
    records = []
    for task_id, trial, variant in p["run_order"]:
        remaining = max_total_seconds - int(time.monotonic() - started)
        if remaining <= 0:
            break
        task = next(t for t in suite.tasks if t.id == task_id)
        with tempfile.TemporaryDirectory(prefix="aet-benchmark-") as tmp:
            working = Path(tmp)
            selected = _stage(task, working, root, host, variant, p["fixtures"][task_id])
            before, _ = _artifacts(working)
            cmd = _command(host, model, task.prompt)
            begin = time.monotonic()
            timeout_hit = False
            try:
                answer = _run(cmd, working, min(timeout, remaining))
                status, text = answer.returncode, answer.stdout
            except subprocess.TimeoutExpired:
                status, text, timeout_hit = None, "", True
            duration = round(time.monotonic() - begin, 2)
            tokens = _usage(host, text) if status == 0 else None
            checked, check_code = "NOT_RUN", None
            if status == 0:
                remaining = max_total_seconds - int(time.monotonic() - started)
                if remaining > 0:
                    try:
                        test = _run(list(task.check_argv), working,
                                    max(1, min(timeout, remaining)))
                        check_code = test.returncode
                        checked = "PASS" if test.returncode == 0 else "FAIL"
                    except (subprocess.TimeoutExpired, OSError):
                        checked = "BLOCKED"
            try:
                after, artifact_paths = _artifacts(working)
            except BenchmarkError:
                after, artifact_paths, checked = None, [], "BLOCKED"
            row = {
                "task_id": task.id, "trial": trial, "variant": variant,
                "run_id": str(uuid.uuid4()), "suite_sha256": suite.sha256,
                "fixture_sha256": p["fixtures"][task_id],
                "host": host, "model": model, "tool_config": p["tool_config"],
                "mounted_skills": selected, "observed_skill_activation": None,
                "agent_status": "PASS" if status == 0 else "FAIL",
                "agent_exit": status, "timed_out": timeout_hit,
                "test_status": checked, "test_exit": check_code,
                "tokens": tokens, "duration_seconds": duration,
                "artifact_sha256": after, "initial_sha256": before,
                "artifact_paths": artifact_paths,
                "human_review": "NOT_REVIEWED", "critical_violation": None,
            }
            records.append(row)
            (output / "records.json").write_text(
                json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return {"report": str(output / "records.json"), "completed": len(records),
            "expected": p["total_runs"], "partial": len(records) < p["total_runs"],
            "warning": "Host not securely sandboxed; agent/check success is NOT human-reviewed quality."}
