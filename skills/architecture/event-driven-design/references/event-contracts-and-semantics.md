# Event contracts, ordering and AsyncAPI

**Read when:** designing event meaning, queue topic, partition strategy, version
compatibility or consumer delivery guarantees.

## Events are facts, commands are requests

OrderConfirmed is a business fact; ConfirmOrder is a requested operation
that may be rejected. Domain events should not serialize an ORM row or
personal data that arbitrary subscribers are not entitled to consume.

~~~json
{
  "event_id": "4a5766b2-8e33-42d5-a45f-cb2d9a49fadb",
  "event_type": "order.confirmed",
  "schema_version": 1,
  "aggregate_id": "order-42",
  "aggregate_version": 7,
  "occurred_at": "2026-10-11T10:00:00Z",
  "correlation_id": "req-123",
  "payload": {"order_id": "order-42"}
}
~~~

This is an illustrative envelope, not a provider-specific
protocol. Specify producer owner, consumer expectation, size,
PII policy, allowed versions, optional/null fields and retention.

## Delivery semantics are scoped

At-least-once delivery implies consumers may see duplicates.
Ordering may only apply **per partition/key or FIFO group** and can
be affected by retries/retention. Even a broker providing a form
of exactly-once processing does not guarantee that an unrelated
HTTP payment API receives one effect. Decide application-level
idempotency and version handling.

## AsyncAPI 3.0

AsyncAPI 3.0.0 distinguishes channels, messages, send/receive
operations and protocol bindings. The schema is a **contract**
not a guarantee about broker delivery, DB atomicity or runtime
tenant authorization.

## Failure and compatibility tests

Old consumer receives added field/enum; new consumer receives
old event; duplicate event_id; version 8 arrives before 7;
missing event; poison payload; replay after storage retention.
Define reconciliation if strict ordering matters.

Sources: https://www.asyncapi.com/docs/reference/specification/v3.0.0 and
https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices .
