"""Deterministic advisory policy for proportional engineering effort.

This operates on *observed*, structured facts; it never authorizes a tool
call, performs a review, dispatches an agent or infers safety from keywords.
Actual host-agent behavior requires held-out external evaluations.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChangeSignals:
    """Human/agent supplied observations, not a replacement for code inspection."""

    local_reversible: bool = False
    multi_component: bool = False
    shared_contract: bool = False
    acceptance_uncertain: bool = False
    authorization_or_secrets: bool = False
    sensitive_or_production_data: bool = False
    migration_with_rollback_risk: bool = False
    destructive_or_irreversible: bool = False
    destructive_authorized: bool = False
    external_privileged_effect: bool = False
    external_action_authorized: bool = False
    independent_tasks: bool = False
    independent_write_paths: bool = False
    isolated_workspaces: bool = False
    subagents_available: bool = False
    reviewer_available: bool = False
    prefer_subagents: bool = False
    long_running: bool = False
    explicit_independent_review: bool = False


@dataclass(frozen=True)
class Decision:
    workflow: str
    review: str
    execution: str
    rationale: tuple[str, ...]
    unmet_gates: tuple[str, ...]

    @property
    def ready_for_integration(self) -> bool:
        """No *known* policy blocker; NOT authorization to merge/deploy."""
        return not self.unmet_gates


def assess(change: ChangeSignals) -> Decision:
    """Choose the smallest default consistent with observed impact.

    A tiny authorization fix is DEEP/R2; a large mechanical change is
    not automatically deep. A missing reviewer is exposed as an unmet
    gate, never described as having performed an independent review.
    """
    if not isinstance(change, ChangeSignals):
        raise TypeError("assess requires ChangeSignals, not raw text or keywords")
    hard_risk = any((
        change.authorization_or_secrets,
        change.sensitive_or_production_data,
        change.migration_with_rollback_risk,
        change.destructive_or_irreversible,
        change.external_privileged_effect,
    ))
    regular_complexity = any((
        change.multi_component, change.shared_contract,
        change.acceptance_uncertain, change.long_running,
        change.independent_tasks,
    ))

    reasons: list[str] = []
    unmet: list[str] = []

    if hard_risk:
        workflow, review = "deep", "R2"
        reasons.append("high-impact trust, persistence or irreversible boundary")
    elif regular_complexity:
        workflow = "standard"
        review = ("R1" if change.explicit_independent_review or
                  (change.acceptance_uncertain and
                   (change.multi_component or change.shared_contract)) else "R0")
        reasons.append("nontrivial but recoverable integration or uncertainty")
    else:
        workflow = "light"
        review = "R1" if change.explicit_independent_review else "R0"
        reasons.append("localized/reversible change; no demonstrated higher-impact boundary")

    if review == "R2" and not change.reviewer_available:
        unmet.append("independent R2 risk review unavailable")
    elif review == "R1" and not change.reviewer_available:
        unmet.append("requested/indicated independent R1 review unavailable")

    if change.destructive_or_irreversible and not change.destructive_authorized:
        unmet.append("destructive or irreversible action not authorized")
    if change.external_privileged_effect and not change.external_action_authorized:
        unmet.append("external privileged action not authorized")

    can_parallelize = (
        change.independent_tasks and change.independent_write_paths
        and change.isolated_workspaces and change.subagents_available
        and not change.shared_contract
        and not change.destructive_or_irreversible
        and not change.external_privileged_effect
    )
    if can_parallelize:
        execution = "parallel"
        reasons.append("independent tasks with isolated writes and available agents")
    elif change.prefer_subagents and change.subagents_available and workflow != "light":
        execution = "subagent-driven"
        reasons.append("delegation requested, available and task warrants context cost")
    else:
        execution = "inline"
        reasons.append("inline avoids unjustified agent startup or unsafe shared writes")
    return Decision(workflow, review, execution, tuple(reasons), tuple(unmet))
