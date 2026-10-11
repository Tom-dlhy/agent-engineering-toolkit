"""Educational fixture for authorization/idempotency tests.

WARNING: In-memory state is not durable or process/concurrency safe.
Production side effects require transactional durable idempotency and auth.
"""
from dataclasses import dataclass


class AccessDenied(Exception):
    """Caller may not act on another tenant."""


class IdempotencyConflict(Exception):
    """Same request ID reused with a different operation."""


@dataclass(frozen=True)
class Receipt:
    tenant: str
    request_id: str
    amount: int


class ExampleLedger:
    def __init__(self) -> None:
        self._items: dict[tuple[str, str], Receipt] = {}
        self.effects = 0

    def apply(
        self, *,
        authenticated_tenant: str,
        target_tenant: str,
        request_id: str,
        amount: int,
    ) -> Receipt:
        if not authenticated_tenant or authenticated_tenant != target_tenant:
            raise AccessDenied("tenant ownership required")
        if not request_id or amount <= 0:
            raise ValueError("request_id and positive amount required")
        key = (target_tenant, request_id)
        prior = self._items.get(key)
        if prior is not None:
            if prior.amount != amount:
                raise IdempotencyConflict("same request ID has changed payload")
            return prior
        receipt = Receipt(target_tenant, request_id, amount)
        self._items[key] = receipt
        self.effects += 1
        return receipt
