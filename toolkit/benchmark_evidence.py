"""Bounded, auditable AET benchmark artifacts.

Store reviewable before/after source and textual diffs *before* executing
acceptance checks. Reports are local-only and untrusted until independently
verified. This is NOT a confidentiality sandbox or DLP guarantee.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import uuid

from .benchmark_model import BenchmarkError

MAX_FILES = 300
MAX_FILE_BYTES = 2_000_000
MAX_TOTAL_BYTES = 12_000_000
MAX_PATCH_BYTES = 2_000_000
_SKIP_ROOT = frozenset({".agents", ".claude", ".git", ".aet", ".venv",
                       "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache"})
_SKIP_PARTS = frozenset({"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"})
_SENSITIVE_NAMES = re.compile(
    r"(^\.env(?:\.|$)|^\.npmrc$|^\.netrc$|^id_(?:rsa|ed25519|ecdsa)"
    r"|\.pem$|\.p12$|\.pfx$|\.key$|^credentials(?:\.|$))", re.I)
_SENSITIVE_CONTENT = re.compile(
    rb"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"
    rb"|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"
    rb"|\bgh[pousr]_[A-Za-z0-9_]{24,}\b"
    rb"|\bsk-[A-Za-z0-9_-]{25,}\b"
)


def canonical_bytes(obj: object) -> bytes:
    return (json.dumps(obj, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot(workspace: Path) -> dict[str, bytes]:
    """Read a strictly bounded set of regular task files.

    Never follow symlinks (even in excluded directories). Refuse suspicious
    filenames and recognizable secrets rather than archiving their contents.
    """
    if workspace.is_symlink() or not workspace.is_dir():
        raise BenchmarkError("invalid benchmark workspace")
    contents: dict[str, bytes] = {}
    total = 0
    for path in sorted(workspace.rglob("*")):
        if path.is_symlink():
            raise BenchmarkError("unsafe symlink in agent workspace")
        relative = path.relative_to(workspace)
        if any(_SENSITIVE_NAMES.search(part) for part in relative.parts):
            raise BenchmarkError("sensitive-looking path in workspace; preserve manually")
        if any(part in _SKIP_ROOT for part in relative.parts[:1]) or any(
            part in _SKIP_PARTS for part in relative.parts
        ):
            continue
        metadata = path.lstat()
        if stat.S_ISDIR(metadata.st_mode):
            continue
        if not stat.S_ISREG(metadata.st_mode):
            raise BenchmarkError("special workspace file, cannot archive")
        if metadata.st_nlink != 1:
            raise BenchmarkError("hard-linked workspace file, cannot archive")
        if metadata.st_size > MAX_FILE_BYTES:
            raise BenchmarkError("oversized file; manual review required")
        if len(contents) >= MAX_FILES:
            raise BenchmarkError("too many workspace files")
        total += metadata.st_size
        if total > MAX_TOTAL_BYTES:
            raise BenchmarkError("workspace exceeded artifact byte budget")
        raw = path.read_bytes()
        if len(raw) > MAX_FILE_BYTES or len(raw) != metadata.st_size:
            raise BenchmarkError("workspace file changed during snapshot")
        if _SENSITIVE_CONTENT.search(raw):
            raise BenchmarkError("possible credential in generated artifact")
        contents[relative.as_posix()] = raw
    return contents


def _put(root: Path, name: str, data: bytes) -> None:
    path = root / name
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as file:
        file.write(data)


def _patch(before: dict[str, bytes], after: dict[str, bytes]) -> bytes:
    chunks: list[str] = []
    for name in sorted(set(before) | set(after)):
        left = before.get(name)
        right = after.get(name)
        if left == right:
            continue
        try:
            a = (left or b"").decode("utf-8").splitlines(keepends=True)
            b = (right or b"").decode("utf-8").splitlines(keepends=True)
        except UnicodeDecodeError:
            chunks.append(f"Binary change (see snapshots): {name}\n")
            continue
        lines = difflib.unified_diff(a, b, fromfile=f"a/{name}",
                                     tofile=f"b/{name}", lineterm="\n")
        chunks.extend(lines)
        if sum(len(x.encode("utf-8")) for x in chunks) > MAX_PATCH_BYTES:
            raise BenchmarkError("diff too large; manual review required")
    data = "".join(chunks).encode("utf-8")
    if len(data) > MAX_PATCH_BYTES:
        raise BenchmarkError("diff exceeds size limit")
    return data


def store(output: Path, run_id: str, before: dict[str, bytes],
          after: dict[str, bytes]) -> dict:
    """Write an evidence bundle once; never modify another run's files."""
    if str(uuid.UUID(run_id)) != run_id:
        raise BenchmarkError("invalid run ID for artifact storage")
    root = output / "artifacts" / run_id
    if root.exists() or root.is_symlink():
        raise BenchmarkError("artifact bundle already exists")
    root.mkdir(mode=0o700, parents=True)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    names: dict[str, str] = {}
    try:
        for side, files in (("before", before), ("after", after)):
            for name, data in sorted(files.items()):
                _put(root, f"{side}/{name}", data)
                names[f"{side}/{name}"] = digest(data)
        patch = _patch(before, after)
        _put(root, "changes.patch", patch)
        names["changes.patch"] = digest(patch)
        manifest = {
            "schema": 1, "run_id": run_id, "files": names,
            "changed_paths": changed, "before_count": len(before),
            "after_count": len(after),
        }
        manifest_raw = canonical_bytes(manifest)
        _put(root, "manifest.json", manifest_raw)
        return {"status": "CAPTURED", "manifest_sha256": digest(manifest_raw),
                "changed_paths": changed, "directory": f"artifacts/{run_id}"}
    except BaseException:
        # Evidence may be incomplete; caller must report it as BLOCKED,
        # never silently treat a half-written bundle as verified.
        raise


def verify(output: Path, record: dict) -> bool:
    """Verify bundle digest and bytes, not authenticity or human judgment."""
    evidence = record.get("artifact_evidence")
    if not isinstance(evidence, dict) or evidence.get("status") != "CAPTURED":
        return False
    run_id = record.get("run_id")
    try:
        if not isinstance(run_id, str) or str(uuid.UUID(run_id)) != run_id:
            return False
    except (ValueError, AttributeError):
        return False
    root = output / "artifacts" / run_id
    if root.is_symlink() or not root.is_dir():
        return False
    if evidence.get("directory") != f"artifacts/{run_id}":
        return False
    try:
        raw = (root / "manifest.json").read_bytes()
        if digest(raw) != evidence.get("manifest_sha256"):
            return False
        manifest = json.loads(raw)
        if canonical_bytes(manifest) != raw or manifest.get("run_id") != run_id:
            return False
        files = manifest.get("files")
        if not isinstance(files, dict) or "changes.patch" not in files:
            return False
        expected_paths = set(files) | {"manifest.json"}
        actual_paths = set()
        for path in root.rglob("*"):
            if path.is_symlink():
                return False
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                actual_paths.add(relative)
        if actual_paths != expected_paths:
            return False
        for name, expected in files.items():
            from .benchmark_model import _safe_path
            rel = _safe_path(name)
            target = root / rel
            if not target.is_file() or target.is_symlink():
                return False
            if digest(target.read_bytes()) != expected:
                return False
        if evidence.get("changed_paths") != manifest.get("changed_paths"):
            return False
        return True
    except (OSError, ValueError, TypeError, BenchmarkError, UnicodeError):
        return False


def verify_records(records_path: Path, destination: Path) -> dict:
    """Create a *separate* verified copy, never mutate runner's raw records."""
    if destination.exists() or destination.is_symlink():
        raise BenchmarkError("verified report exists; refusing overwrite")
    try:
        raw = json.loads(records_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise BenchmarkError("cannot read benchmark results") from exc
    if not isinstance(raw, list):
        raise BenchmarkError("records.json must contain a list")
    checked = []
    for row in raw:
        if not isinstance(row, dict):
            raise BenchmarkError("invalid record")
        proof = verify(records_path.parent, row)
        checked.append({**row, "artifact_evidence_verified": proof})
    if destination.parent.resolve() != records_path.parent.resolve():
        raise BenchmarkError("verified copy must stay in same private output directory")
    _put(destination.parent, destination.name, canonical_bytes(checked))
    return {"total": len(checked), "verified": sum(x["artifact_evidence_verified"] for x in checked),
            "reviewed_copy": str(destination),
            "note": "Integrity only; independent human review is still required."}
