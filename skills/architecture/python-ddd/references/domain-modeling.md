# Python DDD: contexts, aggregates and invariants

**Read when:** a Python domain has difficult consistency rules, varied vocabulary or lifecycle transitions.

## Domain language
Identify contexts, business events and contradictory meanings of shared nouns (e.g. Account in Billing vs Identity). Avoid one global "models" folder shared by unrelated contexts. Use aggregate boundaries around invariants that must be immediately consistent; do not make every table an aggregate.

~~~python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class OrderId:
    value: str

class Order:
    def __init__(self, order_id: OrderId) -> None:
        self.id = order_id
        self._confirmed = False
        self._lines: list[tuple[str, int]] = []

    def add_line(self, sku: str, quantity: int) -> None:
        if self._confirmed or quantity <= 0:
            raise ValueError("order already confirmed or quantity invalid")
        self._lines.append((sku, quantity))

    def confirm(self) -> None:
        if not self._lines:
            raise ValueError("cannot confirm empty order")
        self._confirmed = True
~~~

A real system persists state safely and uses a domain-specific exception; this is a concise example of invariant ownership. Domain model should not import Request, AsyncSession or boto3. Avoid setters that bypass aggregate methods.

## Deciding aggregate size
Smaller aggregates reduce lock contention and permit independent changes; too small risks violated cross-entity invariants. Strong consistency across multiple modules or services requires explicit transaction and saga design; DDD labels do not make distributed writes atomic.

## Test design
State-transition tests, invalid quantity/empty order, retry duplicate confirmation and persistence concurrency. Keep events descriptive past tense and idempotent consumers.

Background: https://martinfowler.com/bliki/DDD_Aggregate.html and https://www.cosmicpython.com/ .
