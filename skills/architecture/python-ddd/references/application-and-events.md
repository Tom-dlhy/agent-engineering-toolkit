# Python DDD application layer, ports and event boundaries

**Read when:** writing use cases around domain aggregates and coordinating repositories, transactions and domain events.

## Depend on behavior, not infrastructure

~~~python
from typing import Protocol

class OrderRepository(Protocol):
    async def get(self, order_id: str) -> "Order | None": ...
    async def save(self, order: "Order") -> None: ...

class ConfirmOrder:
    def __init__(self, orders: OrderRepository) -> None:
        self.orders = orders

    async def execute(self, order_id: str) -> None:
        order = await self.orders.get(order_id)
        if order is None:
            raise OrderNotFound(order_id)
        order.confirm()
        await self.orders.save(order)
~~~

Illustrative types Order and OrderNotFound are defined in the domain. In real production, a unit of work owns commit/rollback around required changes; do not commit inside each repository and accidentally break atomic operations.

## Cross-system communication
Write domain event/outbox in same transaction as aggregate persistence. Publish outside transaction and deduplicate on consumption; never claim exactly-once external message/email/payment. An application service can coordinate cloud or LLM adapters via ports, but should not hold DB row locks during an outbound long-running model request.

## Decision gate
If your service has one resource with CRUD plus three adapters, a simple service and concrete classes may be clearer than a DDD layer. When multiple business invariants/states require explicit model language, tests and strict module boundaries pay off.

## Verification
Fake repository tests for use-case behavior, real database tests for unique constraints/concurrency, replay tests for emitted events and typed error mapping at transport edge.

Background: https://www.cosmicpython.com/ and https://martinfowler.com/eaaCatalog/unitOfWork.html .
