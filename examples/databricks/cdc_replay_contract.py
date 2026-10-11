"""Pure Python oracle for a CDC business contract, NOT a Databricks AUTO CDC implementation.

No cloud calls, Spark imports, data mutations or credential access. Used to
validate expectations about ordering, duplicate events and tombstones before
authorizing a real Lakeflow integration test.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Change:
    key: str
    sequence: int
    value: int | None
    deleted: bool = False


@dataclass(frozen=True)
class HistoryRow:
    key: str
    valid_from: int
    valid_to: int | None
    value: int | None
    deleted: bool


def _versioned(changes: Iterable[Change]) -> dict[str, list[Change]]:
    state: dict[str, dict[int, Change]] = {}
    for event in changes:
        if not event.key or event.sequence < 0:
            raise ValueError("invalid CDC key or sequence")
        if event.deleted and event.value is not None:
            raise ValueError("deleted event must not carry value")
        versions = state.setdefault(event.key, {})
        old = versions.get(event.sequence)
        if old is not None and old != event:
            raise ValueError("conflicting CDC events at same source sequence")
        versions[event.sequence] = event
    return {
        key: [versions[v] for v in sorted(versions)]
        for key, versions in sorted(state.items())
    }


def scd1(changes: Iterable[Change]) -> dict[str, int]:
    """Latest source state, order-insensitive. Tombstone deletes entity."""
    ordered = _versioned(changes)
    current = {}
    for key, history in ordered.items():
        latest = history[-1]
        if not latest.deleted and latest.value is not None:
            current[key] = latest.value
    return current


def scd2(changes: Iterable[Change]) -> list[HistoryRow]:
    """Deterministic validity intervals by abstract source sequence.

    This is a TEST ORACLE only: production AUTO CDC uses supported Databricks
    sequence columns, SCD semantics and table schema, not this Python function.
    """
    output: list[HistoryRow] = []
    for key, versions in _versioned(changes).items():
        for idx, event in enumerate(versions):
            output.append(
                HistoryRow(
                    key=key,
                    valid_from=event.sequence,
                    valid_to=versions[idx + 1].sequence if idx + 1 < len(versions) else None,
                    value=event.value,
                    deleted=event.deleted,
                )
            )
    return output
