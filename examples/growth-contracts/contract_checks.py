"""Offline Growth contract examples: no SDK, network, sending or legal authorization.

Run with Python 3.12+. These checks catch some assignment/suppression defects;
they do NOT certify A/B statistical inference or lawful marketing consent.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import erfc, sqrt
from typing import Iterable


@dataclass(frozen=True)
class AllocationReport:
    unique_units: int
    duplicate_logs: int
    control: int
    treatment: int
    srm_pvalue: float | None
    srm_flagged: bool | None


def check_two_arm_allocation(
    assignments: Iterable[tuple[str, str]],
    *,
    expected_control_share: float = 0.5,
    srm_threshold: float = 0.001,
) -> AllocationReport:
    """Check assignment consistency, then 2-arm Pearson chi-square SRM if large enough.

    Only supports independent assignment-unit counts to two named variants,
    with planned known allocation. Duplicated identical logs are deduplicated;
    conflicting assignments are rejected. A nonflagged SRM does not prove
    randomization was correct, and an SRM flag calls for investigation.
    """
    if not (0 < expected_control_share < 1):
        raise ValueError("expected_control_share must be between 0 and 1")
    if not (0 < srm_threshold < 1):
        raise ValueError("srm_threshold must be between 0 and 1")

    unique: dict[str, str] = {}
    duplicates = 0
    for unit, variant in assignments:
        if not unit or variant not in {"control", "treatment"}:
            raise ValueError("every row needs a unit and control/treatment variant")
        if unit in unique:
            if unique[unit] != variant:
                raise ValueError(f"assignment changed variants for unit {unit!r}")
            duplicates += 1
        else:
            unique[unit] = variant

    n = len(unique)
    control = sum(v == "control" for v in unique.values())
    treatment = n - control
    expected_control = n * expected_control_share
    expected_treatment = n * (1 - expected_control_share)
    if expected_control < 5 or expected_treatment < 5:
        return AllocationReport(n, duplicates, control, treatment, None, None)

    chi2 = ((control - expected_control) ** 2 / expected_control
            + (treatment - expected_treatment) ** 2 / expected_treatment)
    # Chi-square survival for df=1. Not a generic multi-arm experiment test.
    pvalue = erfc(sqrt(chi2 / 2))
    return AllocationReport(n, duplicates, control, treatment,
                            pvalue, pvalue < srm_threshold)


@dataclass(frozen=True)
class MarketingEligibility:
    permission_current: bool
    recipient_suppressed: bool
    account_active: bool
    journey_complete: bool
    frequency_cap_reached: bool
    trigger_expired: bool


def evaluate_marketing_send(state: MarketingEligibility) -> tuple[bool, str]:
    """Pure policy illustration to be checked at send time, not just scheduling.

    Caller is responsible for real regional legal eligibility, atomic
    idempotency/suppression storage, and provider-specific delivery behavior.
    """
    if state.recipient_suppressed:
        return False, "suppressed"
    if not state.permission_current:
        return False, "permission_missing"
    if not state.account_active:
        return False, "account_inactive"
    if state.journey_complete:
        return False, "journey_completed"
    if state.frequency_cap_reached:
        return False, "frequency_cap"
    if state.trigger_expired:
        return False, "trigger_expired"
    return True, "eligible"
