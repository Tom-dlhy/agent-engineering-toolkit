"""Pure standard-library CDC replay example (not production storage)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Change:
    tenant: str
    key: str
    revision: int
    operation: str
    amount_minor: int | None


def reduce_changes(changes: Iterable[Change]) -> dict[tuple[str, str], Change]:
    """Apply trusted source order, preserve delete tombstones, reject conflicts."""
    latest: dict[tuple[str, str], Change] = {}
    for change in changes:
        if not change.tenant or not change.key or change.revision < 0:
            raise ValueError("invalid identity/revision")
        if change.operation == "upsert":
            if change.amount_minor is None or change.amount_minor < 0:
                raise ValueError("invalid amount")
        elif change.operation == "delete":
            if change.amount_minor is not None:
                raise ValueError("delete cannot carry amount")
        else:
            raise ValueError("unknown operation")
        key = (change.tenant, change.key)
        previous = latest.get(key)
        if previous is None or change.revision > previous.revision:
            latest[key] = change
        elif change.revision == previous.revision and change != previous:
            raise ValueError("source revision reused with different payload")
    return latest


def live_values(changes: Iterable[Change]) -> dict[tuple[str, str], int]:
    return {
        key: item.amount_minor
        for key, item in reduce_changes(changes).items()
        if item.operation == "upsert" and item.amount_minor is not None
    }
