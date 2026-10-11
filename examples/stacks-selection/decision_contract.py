"""Illustrative, side-effect-free decision gate; NOT a real stack recommender.

Must-conditions trump preferences. No prices, security warranties or vendor data.
Only real user and environment evidence can populate these values.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping


@dataclass(frozen=True)
class Candidate:
    name: str
    hard_checks: Mapping[str, bool | None]
    # Caller-assessed qualitative fit: 0 = unsuitable, 5 = best, all rated.
    preferences: Mapping[str, float]


@dataclass(frozen=True)
class Evaluation:
    name: str
    eligible: bool
    vetoes: tuple[str, ...]
    unknown_hard_checks: tuple[str, ...]
    # None means option is disqualified or evidence is insufficient.
    score: float | None


def evaluate_candidates(
    candidates: list[Candidate],
    required: tuple[str, ...],
    weights: Mapping[str, float],
) -> list[Evaluation]:
    """Hard veto / unresolved MUST before a transparently weighted score.

    A missing hard check is unknown, never assumed PASS. Scores are useful
    only for remaining explicitly viable options and are *not* performance
    measurements, provider benchmarks, prices or legal/security certification.
    """
    if len(required) != len(set(required)):
        raise ValueError("required check names must be unique")
    if not required or not weights:
        raise ValueError("a decision needs hard checks and qualitative preferences")
    if any(not isfinite(w) or w < 0 for w in weights.values()):
        raise ValueError("weights must be nonnegative finite numbers")
    if sum(weights.values()) <= 0:
        raise ValueError("positive total weight required")
    names = [c.name for c in candidates]
    if not all(names) or len(names) != len(set(names)):
        raise ValueError("candidate names must be present and unique")

    result = []
    for c in candidates:
        vetoes = tuple(key for key in required if c.hard_checks.get(key) is False)
        unknown = tuple(key for key in required if c.hard_checks.get(key) is None)
        eligible = not vetoes and not unknown
        score = None
        if eligible:
            missing = set(weights) - set(c.preferences)
            if missing:
                raise ValueError(f"missing preference scores for {c.name}: {sorted(missing)}")
            for key in weights:
                value = c.preferences[key]
                if not isfinite(value) or not (0 <= value <= 5):
                    raise ValueError(f"invalid qualitative fit score: {c.name}/{key}")
            score = sum(weights[key] * c.preferences[key] for key in weights) / sum(weights.values())
        result.append(Evaluation(c.name, eligible, vetoes, unknown, score))
    return sorted(result, key=lambda row: (not row.eligible, -(row.score or 0), row.name))
