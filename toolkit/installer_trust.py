"""Out-of-project trust anchor for managed installer ownership records.

A workspace can edit .aet/install*.json. An HMAC authenticated with a key held
outside that workspace prevents a forged ledger or recovery journal from
claiming arbitrary user files. This does not protect against an adversary with
access to the user's trust directory or account.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from pathlib import Path

class TrustError(ValueError):
    pass

def canonical(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

class Trust:
    def __init__(self, base: Path, scope: str, agent: str, trust_home: Path | None = None):
        default = Path(os.environ.get("AET_TRUST_HOME", "")) if os.environ.get("AET_TRUST_HOME") else (
            Path.home() / ".config" / "agent-engineering-toolkit" / "trust")
        self.home = (trust_home or default).expanduser()
        identifier = f"{base.resolve(strict=True)}\0{scope}\0{agent}".encode("utf-8")
        self.path = self.home / (hashlib.sha256(identifier).hexdigest() + ".key")

    def key(self, create: bool = False) -> bytes | None:
        if self.home.is_symlink() or self.path.is_symlink():
            raise TrustError("symlink in trusted key location")
        if not self.path.exists():
            if not create:
                return None
            self.home.mkdir(parents=True, exist_ok=True, mode=0o700)
            if os.name != "nt":
                self.home.chmod(0o700)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            try:
                fd = os.open(self.path, flags, 0o600)
            except FileExistsError:
                pass
            else:
                with os.fdopen(fd, "wb") as f:
                    f.write(os.urandom(32))
                    f.flush()
                    os.fsync(f.fileno())
        if not self.path.is_file() or self.path.is_symlink():
            raise TrustError("trusted key is not a regular file")
        if os.name != "nt" and self.path.stat().st_mode & 0o077:
            raise TrustError("trusted key has unsafe permissions")
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        with os.fdopen(os.open(self.path, flags), "rb") as f:
            value = f.read(33)
        if len(value) != 32:
            raise TrustError("invalid trusted key length")
        return value

    def sign(self, data: dict, create: bool = False) -> dict:
        key = self.key(create=create)
        if key is None:
            raise TrustError("no trust key; cannot claim ownership")
        unsigned = {k: v for k, v in data.items() if k != "signature"}
        signature = hmac.new(key, canonical(unsigned), hashlib.sha256).hexdigest()
        return {**unsigned, "signature": signature}

    def check(self, data: dict) -> None:
        key = self.key()
        if key is None:
            raise TrustError("missing trusted key; refuse installation ownership")
        sig = data.get("signature")
        if not isinstance(sig, str) or len(sig) != 64:
            raise TrustError("unsigned ownership record; use explicit seal procedure")
        expected = hmac.new(key, canonical({k:v for k,v in data.items() if k!="signature"}), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            raise TrustError("ownership record failed authentication")
