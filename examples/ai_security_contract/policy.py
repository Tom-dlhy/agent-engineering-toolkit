"""Deterministic tool authorization/approval and ACL-filtered retrieval.

Illustrative only: no real auth service, durable DB, payment or LLM execution.
Do NOT deploy as production security middleware. It tests critical invariants.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable


class Denied(Exception):
    pass


@dataclass(frozen=True)
class Actor:
    tenant: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class Proposal:
    actor_tenant: str
    action: str
    args: dict[str, Any]
    digest: str


def _digest(action: str, args: dict[str, Any], tenant: str) -> str:
    canonical = json.dumps(
        {"action": action, "args": args, "tenant": tenant},
        sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def propose(actor: Actor, action: str, args: dict[str, Any]) -> Proposal:
    if action != "delete_report":
        raise Denied("unapproved tool name")
    if actor.tenant != args.get("tenant"):
        raise Denied("tenant mismatch")
    if "reports:delete" not in actor.scopes:
        raise Denied("missing scope")
    if set(args) != {"tenant", "report_id"}:
        raise Denied("unexpected arguments")
    if not isinstance(args["report_id"], str) or not args["report_id"]:
        raise Denied("invalid resource")
    return Proposal(actor.tenant, action, dict(args),
                    _digest(action, args, actor.tenant))


def execute_approved(
    actor: Actor,
    proposal: Proposal,
    approved_digest: str | None,
    executor: Callable[[dict[str, Any]], str],
) -> str:
    # Re-authorize at execution; approval is tied to precise arguments.
    fresh = propose(actor, proposal.action, proposal.args)
    if approved_digest is None or fresh.digest != approved_digest:
        raise Denied("missing, stale or modified approval")
    if proposal.digest != fresh.digest or proposal.actor_tenant != actor.tenant:
        raise Denied("proposal altered")
    return executor(fresh.args)


@dataclass(frozen=True)
class Chunk:
    id: str
    tenant: str
    text: str


def retrieve_authorized(chunks: list[Chunk], actor: Actor, query: str) -> list[Chunk]:
    if "documents:read" not in actor.scopes:
        raise Denied("missing read scope")
    if not query.strip():
        return []
    # IMPORTANT: tenant ACL before search/ranking; external chunk text is data.
    terms = query.lower().split()
    return [c for c in chunks
            if c.tenant == actor.tenant
            and all(term in c.text.lower() for term in terms)]
