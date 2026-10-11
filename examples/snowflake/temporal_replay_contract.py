"""Offline Snowflake-adjacent contract for temporal features and source dedupe.

This is PURE PYTHON to illustrate invariants, not an implementation of
Snowflake Streams, Dynamic Tables, MERGE or Feature Store. No credentials,
network requests, destructive SQL or claim of execution on Snowflake.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True)
class FeatureVersion:
    entity: str
    event_time: datetime
    available_at: datetime
    source_version: int
    value: float


def asof_feature(
    entity: str,
    observed_at: datetime,
    history: Iterable[FeatureVersion],
) -> FeatureVersion | None:
    """Choose last source version observable at the prediction time.

    Event time alone is NOT sufficient; an old event may arrive after
    observation. Ties are broken deterministically by a stable version.
    """
    obs = _utc(observed_at)
    candidates = [
        row
        for row in history
        if row.entity == entity
        and _utc(row.event_time) <= obs
        and _utc(row.available_at) <= obs
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda r: (_utc(r.available_at), r.source_version))


@dataclass(frozen=True)
class SourceChange:
    business_key: str
    source_version: int
    value: float | None
    is_deleted: bool = False


def replay_changes(events: Iterable[SourceChange]) -> dict[str, SourceChange]:
    """Rebuild a canonical state independent of arrival/file ordering.

    Exact same version duplicates are accepted only when their contents
    agree. A conflicting duplicate version is an explicit data-quality
    error, not an arbitrary last-write-wins decision.
    """
    winners: dict[str, SourceChange] = {}
    for row in events:
        if not row.business_key or row.source_version < 0:
            raise ValueError("invalid source identity/version")
        if row.is_deleted and row.value is not None:
            raise ValueError("deleted state cannot also contain value")
        old = winners.get(row.business_key)
        if old is None or row.source_version > old.source_version:
            winners[row.business_key] = row
        elif row.source_version == old.source_version and row != old:
            raise ValueError("conflicting same-version source changes")
    return winners


def published_values(events: Iterable[SourceChange]) -> dict[str, float]:
    """Materialize non-deleted canonical records after replay."""
    state = replay_changes(events)
    return {
        key: change.value
        for key, change in state.items()
        if not change.is_deleted and change.value is not None
    }
