"""Managed, opt-in, file-owned skill installation for Codex and Claude Code.

The repository is the source of truth. Installed copies are never trusted as
source material. No hooks, skill scripts, network access or prompts are executed.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid

import yaml

from toolkit.installer_trust import Trust, TrustError, canonical

ROOT = Path(__file__).resolve().parents[1]
AGENTS = {"codex": ".agents/skills", "claude": ".claude/skills"}
SCHEMA = "aet.install.v2"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class InstallError(ValueError):
    """Unsafe or unsupported operation; never proceed after this exception."""


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_name(name: str) -> str:
    if not isinstance(name, str) or not SLUG.fullmatch(name):
        raise InstallError(f"invalid skill/profile identifier: {name!r}")
    return name


def _safe_relative(path: str) -> str:
    if not isinstance(path, str) or not path or "\\" in path:
        raise InstallError(f"unsafe relative path: {path!r}")
    p = Path(path)
    if p.is_absolute() or any(s in ("", ".", "..") for s in path.split("/")):
        raise InstallError(f"unsafe relative path: {path!r}")
    return path


def _no_link(path: Path) -> None:
    if path.is_symlink():
        raise InstallError(f"refusing symlink: {path}")


def _parents_safe(root: Path, leaf: Path) -> None:
    root = root.resolve(strict=True)
    if not leaf.is_relative_to(root):
        raise InstallError(f"destination outside trusted root: {leaf}")
    candidate = root
    for part in leaf.relative_to(root).parts:
        candidate = candidate / part
        _no_link(candidate)


def _files(folder: Path) -> dict[str, str]:
    if not folder.is_dir() or folder.is_symlink():
        raise InstallError(f"invalid skill directory: {folder}")
    found: dict[str, str] = {}
    for item in sorted(folder.rglob("*")):
        _no_link(item)
        if item.is_file():
            if not item.stat().st_mode & 0o400:
                raise InstallError(f"unreadable source: {item}")
            key = item.relative_to(folder).as_posix()
            found[_safe_relative(key)] = _digest(item.read_bytes())
        elif not item.is_dir():
            raise InstallError(f"non-regular skill entry: {item}")
    if "SKILL.md" not in found:
        raise InstallError(f"missing SKILL.md: {folder}")
    return found


def _existing(folder: Path) -> dict[str, str] | None:
    if not folder.exists() and not folder.is_symlink():
        return None
    if folder.is_symlink() or not folder.is_dir():
        raise InstallError(f"unsafe or non-directory destination: {folder}")
    found: dict[str, str] = {}
    for item in sorted(folder.rglob("*")):
        _no_link(item)
        if item.is_file():
            found[_safe_relative(item.relative_to(folder).as_posix())] = _digest(item.read_bytes())
        elif not item.is_dir():
            raise InstallError(f"non-regular destination entry: {item}")
    return found


def _source(root: Path) -> tuple[dict[str, Path], str]:
    registry = yaml.safe_load((root / "registry/skills.yaml").read_text(encoding="utf-8"))
    allowed = (root / "skills").resolve(strict=True)
    entries: dict[str, Path] = {}
    for entry in registry["skills"]:
        name = _safe_name(entry["name"])
        rel = _safe_relative(entry["path"])
        folder = root / rel
        # Do not resolve every registry entry: a stale unrelated skill must
        # never prevent uninstall or inspection of an installed one.
        parts = Path(rel).parts
        if len(parts) < 3 or parts[0] != "skills" or folder.name != name:
            raise InstallError(f"invalid registry source: {rel}")
        if folder.exists():
            if not folder.resolve(strict=True).is_relative_to(allowed):
                raise InstallError(f"invalid registry source: {rel}")
            cursor = root
            for part in parts:
                cursor = cursor / part
                _no_link(cursor)
        if name in entries:
            raise InstallError(f"duplicate skill: {name}")
        entries[name] = folder
    try:
        revision = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
            check=True, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        if dirty:
            revision = "dirty-" + revision[:12]
    except (OSError, subprocess.SubprocessError):
        revision = ""
    if not re.fullmatch(r"[0-9a-f]{40}|dirty-[0-9a-f]{12}", revision):
        revision = "snapshot"
    return entries, revision


def _requested(root: Path, profile: str | None, skills: tuple[str, ...]) -> list[str]:
    selected: list[str] = []
    if profile:
        name = _safe_name(profile)
        profile_file = root / "profiles" / (name + ".yaml")
        if not profile_file.is_file():
            raise InstallError(f"unknown profile: {name}")
        selected.extend(yaml.safe_load(profile_file.read_text(encoding="utf-8"))["skills"])
    selected.extend(skills)
    return list(dict.fromkeys(_safe_name(n) for n in selected))



LOCK_SCHEMA = "aet.lock.v1"


def generate_lock(root: Path, agent: str, profile: str | None = None,
                  skills: tuple[str, ...] = ()) -> dict:
    """Reproducible, target-independent inventory of exact source skill bytes."""
    if agent not in AGENTS:
        raise InstallError(f"unknown agent: {agent}")
    available, revision = _source(root.resolve(strict=True))
    selected = _requested(root, profile, skills)
    if not selected:
        raise InstallError("lockfile requires a profile or explicit skills")
    if any(name not in available for name in selected):
        raise InstallError("unknown skill in lockfile selection")
    return {"schema": LOCK_SCHEMA, "agent": agent, "revision": revision,
            "selected": selected, "files": {name: _files(available[name]) for name in selected}}


def read_lock(path: Path, agent: str) -> dict:
    """Validate untrusted lockfile; never trust paths or ownership from it."""
    _no_link(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["schema"] != LOCK_SCHEMA or data["agent"] != agent:
            raise InstallError("lockfile schema or agent mismatch")
        selected = [_safe_name(n) for n in data["selected"]]
        if not selected or len(set(selected)) != len(selected) or set(data["files"]) != set(selected):
            raise InstallError("invalid lockfile selection")
        for name, hashes in data["files"].items():
            _safe_name(name)
            if not isinstance(hashes, dict) or "SKILL.md" not in hashes:
                raise InstallError("invalid lockfile inventory")
            for rel, digest in hashes.items():
                _safe_relative(rel)
                if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                    raise InstallError("invalid lockfile SHA")
        if not isinstance(data["revision"], str):
            raise InstallError("invalid lockfile revision")
        return data
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise InstallError(f"invalid lockfile: {exc}") from exc


def _assert_locked(plan: dict, lock: dict) -> None:
    if (plan["selected"] != lock["selected"] or plan["desired"] != lock["files"]
            or plan["revision"] != lock["revision"]):
        raise InstallError("source differs from pinned lockfile; checkout its exact revision")


class ManagedInstaller:
    def __init__(self, root: Path, agent: str, scope: str, project: Path | None = None,
                 home: Path | None = None, trust_home: Path | None = None):
        if agent not in AGENTS or scope not in ("project", "user"):
            raise InstallError("agent must be codex/claude; scope must be project/user")
        self.root = root.resolve(strict=True)
        self.agent, self.scope = agent, scope
        base = (project or Path.cwd()) if scope == "project" else (home or Path.home())
        if not base.is_dir():
            raise InstallError(f"target root must exist: {base}")
        self.base = base.resolve(strict=True)
        self.target = self.base / AGENTS[agent]
        self.meta = self.base / ".aet"
        self.state_path = self.meta / f"install-{scope}-{agent}.json"
        self.journal = self.meta / f"pending-{scope}-{agent}.json"
        self.lock_path = self.meta / f"lock-{scope}-{agent}"
        self.trust = Trust(self.base, scope, agent, trust_home=trust_home)
        _parents_safe(self.base, self.target)
        _parents_safe(self.base, self.meta)

    def _state(self) -> dict:
        if not self.state_path.exists():
            return {"schema": SCHEMA, "agent": self.agent, "scope": self.scope,
                    "selected": [], "files": {}, "sources": {}, "revision": None}
        _no_link(self.state_path)
        try:
            record = json.loads(self.state_path.read_text(encoding="utf-8"))
            self.trust.check(record)
            if (record["schema"] != SCHEMA or record["agent"] != self.agent
                    or record["scope"] != self.scope or not isinstance(record["selected"], list)
                    or not isinstance(record["files"], dict)):
                raise InstallError("installation state does not match current target")
            selected = [_safe_name(n) for n in record["selected"]]
            if len(selected) != len(set(selected)) or set(record["files"]) != set(selected):
                raise InstallError("installation state has inconsistent selection")
            if not (record.get("revision") is None or isinstance(record.get("revision"), str)):
                raise InstallError("invalid source revision")
            sources = record.get("sources", {})
            if not isinstance(sources, dict) or any(n not in record["files"] for n in sources):
                raise InstallError("invalid per-skill source revisions")
            for n, revision in sources.items():
                if not isinstance(revision, (str, type(None))):
                    raise InstallError("invalid per-skill revision")
            for n, hashes in record["files"].items():
                _safe_name(n)
                if not isinstance(hashes, dict) or "SKILL.md" not in hashes:
                    raise InstallError("invalid stored file inventory")
                for rel, sha in hashes.items():
                    _safe_relative(rel)
                    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
                        raise InstallError("invalid stored digest")
            return record
        except (OSError, ValueError, KeyError, TypeError, TrustError) as exc:
            raise InstallError(f"invalid state; refusing to claim ownership: {exc}") from exc

    def _status(self, name: str, expected: dict[str, str]) -> tuple[str, dict[str, str] | None]:
        path = self.target / name
        _parents_safe(self.base, path)
        present = _existing(path)
        if present is None:
            return "missing", None
        if present == expected:
            return "clean", present
        if set(present) - set(expected):
            return "extra", present
        if any(present[k] != expected[k] for k in present if k in expected):
            return "modified", present
        return "missing-files", present

    def inspect(self) -> dict:
        state = self._state()
        statuses = {}
        for name, hashes in state["files"].items():
            try:
                statuses[name] = self._status(name, hashes)[0]
            except (OSError, InstallError):
                statuses[name] = "unsafe"
        return {"agent": self.agent, "scope": self.scope, "revision": state["revision"],
                "installed": statuses, "pending_recovery": self.journal.exists()}

    def plan(self, command: str, profile: str | None = None,
             skills: tuple[str, ...] = ()) -> dict:
        if command not in ("install", "update", "repair", "uninstall"):
            raise InstallError(f"unknown operation: {command}")
        state = self._state()
        previous = state["files"]
        if command == "uninstall":
            available, revision = {}, state["revision"]
            requested = [_safe_name(s) for s in skills]
        else:
            available, revision = _source(self.root)
            requested = _requested(self.root, profile, skills)
        if command == "repair":
            selected = list(previous)
        elif command == "uninstall":
            if profile:
                raise InstallError("uninstall does not accept --profile; select --skill")
            selected = [n for n in previous if n not in requested] if requested else []
        else:
            selected = list(dict.fromkeys([*previous, *requested]))
            if not selected:
                raise InstallError("specify --profile or --skill for initial installation")
        missing_sources = set(selected) - set(available) if command != "uninstall" else set()
        if missing_sources:
            raise InstallError("selected skills missing from source: " + ", ".join(sorted(missing_sources)))
        desired: dict[str, dict[str, str]] = {}
        for name in selected:
            desired[name] = previous[name] if command == "repair" else _files(available[name])
            if command == "repair" and _files(available[name]) != previous[name]:
                raise InstallError(f"repair requires original source revision for {name}; use update")
        operations = []
        for name in dict.fromkeys([*previous, *selected]):
            prev = previous.get(name)
            status, present = self._status(name, prev or {}) if prev is not None else (
                ("unmanaged", _existing(self.target / name)) if (self.target / name).exists() or
                (self.target / name).is_symlink() else ("missing", None)
            )
            want = desired.get(name)
            if prev is None and present is not None:
                action = "conflict-unmanaged"
            elif status in ("modified", "extra", "unsafe"):
                action = "conflict-" + status
            elif prev is not None and status == "missing-files" and present is not None and want is None:
                action = "conflict-missing-files"
            elif want is None:
                action = "remove" if present is not None else "forget"
            elif prev is None:
                action = "add"
            elif command == "repair" and status == "clean":
                action = "unchanged"
            elif status != "clean" or prev != want:
                action = "replace" if present is not None else "restore"
            else:
                action = "unchanged"
            baseline, candidate = prev or {}, want or {}
            present_files = present or {}
            diff = {
                "upstream_added": sorted(set(candidate) - set(baseline)),
                "upstream_removed": sorted(set(baseline) - set(candidate)),
                "upstream_changed": sorted(k for k in set(candidate) & set(baseline)
                                           if candidate[k] != baseline[k]),
                "local_added": sorted(set(present_files) - set(baseline)),
                "local_missing": sorted(set(baseline) - set(present_files)),
                "local_modified": sorted(k for k in set(present_files) & set(baseline)
                                         if present_files[k] != baseline[k]),
            }
            operations.append({"skill": name, "action": action, "status": status,
                               "observed": present,
                               "file_diff": {k: v for k, v in diff.items() if v}})
        return {"command": command, "selected": selected, "desired": desired,
                "operations": operations, "revision": revision if command not in ("repair", "uninstall") else state["revision"]}

    @contextmanager
    def _locked(self):
        self.meta.mkdir(parents=True, exist_ok=True)
        _parents_safe(self.base, self.meta)
        _no_link(self.lock_path)
        with os.fdopen(os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600), "r+b") as lock:
            try:
                if os.name == "nt":
                    import msvcrt
                    lock.seek(0)
                    lock.write(b"0")
                    lock.flush()
                    lock.seek(0)
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise InstallError("another installer owns this target") from exc
            try:
                yield
            finally:
                if os.name == "nt":
                    lock.seek(0)
                    msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _write_json(path: Path, data: dict) -> None:
        fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".aet-tmp-")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def _recover(self) -> bool:
        """Restore an interrupted transaction only after authenticating every byte.

        Never trust filesystem paths or delete a destination just because a
        journal says it did not previously exist. Missing/inconsistent evidence
        causes a safe halt for manual inspection, not speculative cleanup.
        """
        if not self.journal.exists() and not self.journal.is_symlink():
            return False
        _no_link(self.journal)
        record = json.loads(self.journal.read_text(encoding="utf-8"))
        self.trust.check(record)
        tx_name = record.get("transaction")
        if (record.get("schema") != "aet.transaction.v2"
                or record.get("agent") != self.agent
                or record.get("scope") != self.scope
                or record.get("target") != str(self.base)
                or not isinstance(tx_name, str)
                or not re.fullmatch(r"tx-[a-f0-9]{32}", tx_name)
                or not isinstance(record.get("operations"), list)
                or not isinstance(record.get("had_state"), bool)):
            raise InstallError("invalid recovery journal identity; manual inspection required")
        tx = self.meta / tx_name
        _parents_safe(self.base, tx)
        if not tx.is_dir():
            raise InstallError("recovery transaction directory is missing")
        seen = set()
        verified = []
        for op in record["operations"]:
            name = _safe_name(op["skill"])
            if name in seen:
                raise InstallError("duplicate recovery operation")
            seen.add(name)
            before, after = op.get("before"), op.get("after")
            if not isinstance(op.get("had_original"), bool) or (before is None) != (not op["had_original"]):
                raise InstallError("invalid previous ownership declaration")
            for hashes in (before, after):
                if hashes is not None:
                    if not isinstance(hashes, dict) or "SKILL.md" not in hashes:
                        raise InstallError("invalid transaction inventory")
                    for rel, sha in hashes.items():
                        _safe_relative(rel)
                        if not isinstance(sha, str) or not re.fullmatch(r"[a-f0-9]{64}", sha):
                            raise InstallError("invalid transaction hash")
            dest, backup = self.target / name, tx / "backups" / name
            _parents_safe(self.base, dest)
            _parents_safe(self.base, backup)
            present, saved = _existing(dest), _existing(backup)
            # Backup is never valid unless it exactly matches signed pre-state.
            if saved is not None:
                if not op["had_original"] or saved != before:
                    raise InstallError(f"untrusted backup for {name}; manual recovery required")
                if present is not None and present != after:
                    raise InstallError(f"destination modified during interruption: {name}")
            elif op["had_original"]:
                if present != before:
                    raise InstallError(f"missing original backup or concurrent edit: {name}")
            elif present is not None and present != after:
                raise InstallError(f"unowned/modified destination during recovery: {name}")
            verified.append((dest, backup, present, saved, before, after))
        old_state = record.get("before_state_sha")
        new_state = record.get("after_state_sha")
        def valid_sha(value):
            return value is None or (isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value))
        if not valid_sha(old_state) or not valid_sha(new_state) or (old_state is None) != (not record["had_state"]):
            raise InstallError("invalid recovery state hash")
        previous = tx / "previous-state.json"
        _parents_safe(self.base, previous)
        if previous.is_symlink() or self.state_path.is_symlink():
            raise InstallError("symlinked transaction state")
        backup_bytes = previous.read_bytes() if previous.is_file() else None
        live_bytes = self.state_path.read_bytes() if self.state_path.is_file() else None
        if backup_bytes is not None and _digest(backup_bytes) != old_state:
            raise InstallError("previous state backup does not match transaction")
        if live_bytes is not None:
            if _digest(live_bytes) not in {old_state, new_state}:
                raise InstallError("state changed during interruption; cannot recover safely")
        if record["had_state"] and backup_bytes is None and (live_bytes is None or _digest(live_bytes) != old_state):
            raise InstallError("original state missing; manual recovery required")
        # Only after all paths, directories and ledger states are verified may
        # the transaction perform its rollback. Repeatable if interrupted.
        for dest, backup, present, saved, before, after in reversed(verified):
            if saved is not None:
                if present is not None:
                    shutil.rmtree(dest)
                backup.rename(dest)
            elif before is None and present is not None:
                shutil.rmtree(dest)
        if backup_bytes is not None:
            os.replace(previous, self.state_path)
        elif not record["had_state"] and self.state_path.exists():
            self.state_path.unlink()
        self.journal.unlink()
        if tx.exists():
            shutil.rmtree(tx)
        return True

    @staticmethod
    def _json_bytes(data: dict) -> bytes:
        return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")

    def seal_legacy(self, confirmation: str) -> dict:
        """Explicit opt-in transition; never silently adopt pre-v2 ownership."""
        with self._locked():
            if self.journal.exists():
                raise InstallError("pending transaction: recovery must be resolved first")
            if not self.state_path.is_file():
                raise InstallError("no legacy installation to seal")
            _no_link(self.state_path)
            raw = json.loads(self.state_path.read_text(encoding="utf-8"))
            if "signature" in raw:
                self._state()
                return {"sealed": True, "already_sealed": True}
            if confirmation != "I-VERIFIED-OWNERSHIP":
                raise InstallError("sealing requires --confirm-adoption I-VERIFIED-OWNERSHIP")
            if raw.get("schema") != SCHEMA or raw.get("agent") != self.agent or raw.get("scope") != self.scope:
                raise InstallError("invalid legacy installation state")
            files = raw.get("files")
            if not isinstance(files, dict) or set(files) != set(raw.get("selected", [])):
                raise InstallError("legacy ledger does not match selection")
            # A forged legacy ledger can have matching SHA values; this explicit
            # administrative action asserts that each file is indeed managed.
            for name, hashes in files.items():
                _safe_name(name)
                if not isinstance(hashes, dict) or "SKILL.md" not in hashes:
                    raise InstallError("invalid legacy inventory")
                for rel, digest in hashes.items():
                    _safe_relative(rel)
                    if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                        raise InstallError("invalid legacy checksum")
                if _existing(self.target / name) != hashes:
                    raise InstallError(f"legacy folder changed: {name}")
            raw["sources"] = {name: raw.get("revision") for name in files}
            signed = self.trust.sign(raw, create=True)
            self._write_json(self.state_path, signed)
            return {"sealed": True, "skills": sorted(files)}


    def apply(self, command: str, profile: str | None = None,
              skills: tuple[str, ...] = (), lock: dict | None = None) -> dict:
        with self._locked():
            self._recover()
            plan = self.plan(command, profile, skills)
            if lock is not None:
                _assert_locked(plan, lock)
            conflicts = [o for o in plan["operations"] if o["action"].startswith("conflict")]
            if conflicts:
                raise InstallError("conflicts; no changes made: " + json.dumps(conflicts))
            changes = [o for o in plan["operations"] if o["action"] not in ("unchanged", "forget")]
            if not changes and plan["selected"] == self._state()["selected"]:
                return plan
            available, _ = _source(self.root) if command != "uninstall" else ({}, None)
            previous_state = self._state()
            # Every existing destination (including unchanged skills) is checked
            # before creating any transaction record. Do not trust stale plans.
            def assert_unchanged(op):
                dest = self.target / op["skill"]
                _parents_safe(self.base, dest)
                actual = _existing(dest)
                if actual != op["observed"]:
                    raise InstallError(f"concurrent user modification: {op['skill']}")
            for op in plan["operations"]:
                assert_unchanged(op)
            tx_name = "tx-" + uuid.uuid4().hex
            tx = self.meta / tx_name
            stage, backups = tx / "stage", tx / "backups"
            stage.mkdir(parents=True)
            backups.mkdir()
            try:
                for op in changes:
                    if op["action"] not in ("add", "replace", "restore"):
                        continue
                    name = op["skill"]
                    staged = stage / name
                    staged.mkdir()
                    for rel, sha in plan["desired"][name].items():
                        data = (available[name] / rel).read_bytes()
                        if _digest(data) != sha:
                            raise InstallError(f"source changed during staging: {name}/{rel}")
                        output = staged / rel
                        output.parent.mkdir(parents=True, exist_ok=True)
                        output.write_bytes(data)
                        if os.name != "nt":
                            mode = (available[name] / rel).stat().st_mode
                            output.chmod(0o755 if mode & 0o111 else 0o644)
                    if _existing(staged) != plan["desired"][name]:
                        raise InstallError(f"staged copy verification failed: {name}")
                prior_sources = previous_state.get("sources", {})
                sources = {}
                for name in plan["selected"]:
                    if name in previous_state["files"] and previous_state["files"][name] == plan["desired"][name]:
                        sources[name] = prior_sources.get(name, previous_state["revision"])
                    else:
                        sources[name] = plan["revision"]
                updated = self.trust.sign({
                    "schema": SCHEMA, "agent": self.agent, "scope": self.scope,
                    "revision": plan["revision"], "selected": plan["selected"],
                    "files": plan["desired"], "sources": sources,
                    "installed_at": datetime.now(timezone.utc).isoformat(),
                }, create=True)
                # Revalidate even after potentially lengthy staging. Ensure an
                # editor did not modify a skill while we were copying it.
                for op in plan["operations"]:
                    assert_unchanged(op)
                had_state = self.state_path.exists()
                if had_state:
                    _no_link(self.state_path)
                journal = self.trust.sign({
                    "schema": "aet.transaction.v2",
                    "transaction": tx_name, "target": str(self.base),
                    "agent": self.agent, "scope": self.scope,
                    "had_state": had_state,
                    "before_state_sha": _digest(self.state_path.read_bytes()) if had_state else None,
                    "after_state_sha": _digest(self._json_bytes(updated)),
                    "operations": [{
                        "skill": op["skill"],
                        "had_original": op["observed"] is not None,
                        "before": previous_state["files"].get(op["skill"]),
                        "after": plan["desired"].get(op["skill"]),
                    } for op in changes]
                })
                self._write_json(self.journal, journal)
                try:
                    self.target.mkdir(parents=True, exist_ok=True)
                    _parents_safe(self.base, self.target)
                    if had_state:
                        self.state_path.rename(tx / "previous-state.json")
                    for op in changes:
                        # Last-second optimistic concurrency check: if an agent
                        # edits this folder after planning, don't overwrite it.
                        assert_unchanged(op)
                        name = op["skill"]
                        dest = self.target / name
                        _parents_safe(self.base, dest)
                        if dest.exists():
                            dest.rename(backups / name)
                        if op["action"] in ("add", "replace", "restore"):
                            (stage / name).rename(dest)
                    self._write_json(self.state_path, updated)
                    self.journal.unlink()
                except BaseException:
                    self._recover()
                    raise
            finally:
                if tx.exists() and not self.journal.exists():
                    shutil.rmtree(tx)
            return plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "install", "update", "doctor", "list",
                                            "repair", "uninstall", "lock", "seal"))
    parser.add_argument("--agent", choices=tuple(AGENTS), required=True)
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--profile")
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument("--apply", action="store_true", help="Explicitly allow filesystem mutation")
    parser.add_argument("--confirm-adoption", help="Explicitly authorize signing old ownership ledger")
    parser.add_argument("--locked", action="store_true", help="Install exactly from a pinned lockfile")
    parser.add_argument("--lockfile", type=Path, help="Optional lockfile path; default .aet/skills-lock-<agent>.json")
    args = parser.parse_args(argv)
    try:
        mgr = ManagedInstaller(args.source, args.agent, args.scope, args.project)
        if args.scope == "user" and args.project is not None:
            raise InstallError("do not specify --project with --scope user")
        lock_path = args.lockfile or (mgr.meta / f"skills-lock-{args.agent}.json")
        if args.command == "seal":
            if not args.apply:
                raise InstallError("seal requires --apply and explicit ownership verification")
            print(json.dumps(mgr.seal_legacy(args.confirm_adoption or ""), indent=2))
            return 0
        if args.command == "lock":
            selected = tuple(args.skill) if args.profile or args.skill else tuple(mgr._state()["selected"])
            lock_data = generate_lock(args.source, args.agent, args.profile, selected)
            if args.apply:
                with mgr._locked():
                    if mgr.journal.exists():
                        raise InstallError("pending transaction; recover before writing a lock")
                    if lock_path.exists() or lock_path.is_symlink():
                        current = read_lock(lock_path, args.agent)
                        if current != lock_data:
                            raise InstallError("lockfile already exists and differs; remove/review it explicitly")
                    else:
                        mgr._write_json(lock_path, lock_data)
            print(json.dumps({"path": str(lock_path), "applied": args.apply,
                              "selected": lock_data["selected"],
                              "revision": lock_data["revision"]}, indent=2))
            return 0
        lock_data = None
        selected_skills = tuple(args.skill)
        selected_profile = args.profile
        if args.locked:
            if args.command not in ("plan", "install", "update"):
                raise InstallError("--locked is only valid for plan/install/update")
            if args.profile or args.skill:
                raise InstallError("--locked determines selections; omit --profile/--skill")
            lock_data = read_lock(lock_path, args.agent)
            selected_skills = tuple(lock_data["selected"])
        if args.command in ("doctor", "list"):
            result = mgr.inspect()
            print(json.dumps(result, indent=2))
            if args.command == "doctor" and (result["pending_recovery"] or any(
                    s != "clean" for s in result["installed"].values())):
                return 2
            return 0
        command = "install" if args.command == "plan" else args.command
        result = (mgr.apply(command, selected_profile, selected_skills, lock=lock_data)
                  if args.apply and args.command != "plan"
                  else mgr.plan(command, selected_profile, selected_skills))
        if lock_data is not None:
            _assert_locked(result, lock_data)
        # The desired manifest is internal to the planner, never clutter CLI output.
        result.pop("desired")
        result["applied"] = bool(args.apply and args.command != "plan")
        print(json.dumps(result, indent=2))
        return 0 if not any(o["action"].startswith("conflict") for o in result["operations"]) else 2
    except (OSError, InstallError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
