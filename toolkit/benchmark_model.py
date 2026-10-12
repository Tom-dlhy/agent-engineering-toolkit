"""Validated A/B/C task manifest for AET engineering evaluations.

AET does not infer behavior quality from prompts; tasks have explicit
observable acceptance checks. Manifests/fixtures are trusted executable inputs:
only run vetted local fixtures, never downloaded unreviewed repositories.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


class BenchmarkError(ValueError):
    """Unsafe, ambiguous or malformed benchmark definition."""


VARIANTS = ("baseline", "knowledge", "full")
_NAME = re.compile(r"^[a-z][a-z0-9-]{1,59}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN = {".git", ".agents", ".claude", ".aet", ".venv", "node_modules",
              "__pycache__", ".env", ".aws", ".ssh", ".config", ".mcp.json",
              "AGENTS.md", "CLAUDE.md", "settings.local.json"}


def _safe_path(name: str) -> Path:
    if not isinstance(name, str) or not name or "\\" in name:
        raise BenchmarkError("invalid fixture relative path")
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in ("", ".", "..") for x in name.split("/")):
        raise BenchmarkError("unsafe fixture relative path")
    if any(x in _FORBIDDEN or x.startswith(".env.") for x in p.parts):
        raise BenchmarkError(f"host settings or credentials forbidden: {name}")
    return Path(*p.parts)


def inventory(source: Path) -> tuple[str, tuple[tuple[Path, bytes], ...]]:
    """Stable sha256 over paths and bytes, rejecting links and special files."""
    if not source.is_dir() or source.is_symlink():
        raise BenchmarkError("fixture directory missing or linked")
    files: list[tuple[Path, bytes]] = []
    for p in source.rglob("*"):
        if p.is_symlink():
            raise BenchmarkError(f"symlink in benchmark fixture: {p}")
        rel = _safe_path(p.relative_to(source).as_posix())
        if p.is_dir():
            continue
        if not p.is_file():
            raise BenchmarkError(f"not a normal file: {p}")
        if p.stat().st_size > 2_000_000:
            raise BenchmarkError(f"fixture file too large: {rel}")
        files.append((rel, p.read_bytes()))
    if not files or len(files) > 300:
        raise BenchmarkError("fixture must contain 1..300 regular files")
    files.sort(key=lambda item: item[0].as_posix())
    h = hashlib.sha256()
    for rel, contents in files:
        h.update(rel.as_posix().encode("utf-8") + b"\0")
        h.update(contents + b"\0")
    return h.hexdigest(), tuple(files)


@dataclass(frozen=True)
class Task:
    id: str
    prompt: str
    fixture_dir: Path
    fixture_sha256: str | None
    technical_skills: tuple[str, ...]
    check_argv: tuple[str, ...]
    expected: str
    risk: str


@dataclass(frozen=True)
class Suite:
    path: Path
    tasks: tuple[Task, ...]
    sha256: str


def load_suite(path: Path, root: Path) -> Suite:
    """Manifest paths must reside under AET; no arbitrary file read on plan."""
    path = path.resolve(strict=True)
    root = root.resolve(strict=True)
    if not path.is_relative_to(root):
        raise BenchmarkError("manifest must live inside the local toolkit checkout")
    raw = path.read_bytes()
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise BenchmarkError(f"invalid manifest JSON: {exc}") from exc
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("tasks"), list):
        raise BenchmarkError("manifest requires version:1 and tasks array")
    if not 1 <= len(data["tasks"]) <= 30:
        raise BenchmarkError("a suite must have 1..30 tasks")
    tasks = []
    ids = set()
    for item in data["tasks"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not _NAME.fullmatch(item["id"]):
            raise BenchmarkError("task id must be lower-kebab-case")
        name = item["id"]
        if name in ids:
            raise BenchmarkError(f"duplicate task: {name}")
        ids.add(name)
        prompt = item.get("prompt")
        if not isinstance(prompt, str) or not 10 <= len(prompt) <= 4000:
            raise BenchmarkError(f"{name}: invalid prompt length")
        fixture = root / _safe_path(item.get("fixture_dir"))
        if not fixture.resolve(strict=True).is_relative_to(root):
            raise BenchmarkError("fixture path escapes repository")
        sha, _ = inventory(fixture)
        pinned = item.get("fixture_sha256")
        if pinned is not None and (not isinstance(pinned, str) or not _DIGEST.fullmatch(pinned)):
            raise BenchmarkError(f"{name}: invalid fixture SHA")
        if pinned is not None and pinned != sha:
            raise BenchmarkError(f"{name}: fixture changed; update versioned manifest deliberately")
        skills = item.get("technical_skills")
        if not isinstance(skills, list) or len(skills) > 5 or any(
            not isinstance(s, str) or not _NAME.fullmatch(s) for s in skills
        ) or len(set(skills)) != len(skills):
            raise BenchmarkError(f"{name}: invalid technical skills")
        check = item.get("check_argv")
        if not isinstance(check, list) or not 1 <= len(check) <= 16 or any(
            not isinstance(s, str) or not s or len(s) > 200 for s in check
        ):
            raise BenchmarkError(f"{name}: check_argv must be nonempty argv, no shell")
        if any(any(x in s for x in ("\n", "\r", "\0")) for s in check):
            raise BenchmarkError("control characters in check arguments")
        expected = item.get("expected")
        if not isinstance(expected, str) or len(expected) < 8:
            raise BenchmarkError(f"{name}: write an observable acceptance expectation")
        risk = item.get("risk", "standard")
        if risk not in ("light", "standard", "deep"):
            raise BenchmarkError(f"{name}: unsupported risk level")
        tasks.append(Task(name, prompt, fixture, pinned, tuple(skills),
                          tuple(check), expected, risk))
    return Suite(path, tuple(tasks), hashlib.sha256(raw).hexdigest())


def fixture_summary(suite: Suite) -> list[dict]:
    return [{"task_id": t.id, "fixture_sha256": inventory(t.fixture_dir)[0],
             "pinned": t.fixture_sha256 is not None, "risk": t.risk,
             "technical_skills": list(t.technical_skills),
             "check_argv": list(t.check_argv)} for t in suite.tasks]
