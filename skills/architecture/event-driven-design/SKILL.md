---
name: event-driven-design
domain: architecture
version: "0.1.0"
description: >-
  Use when designing event-driven systems, webhooks, message queues, outbox patterns, asynchronous boundaries or distributed workflows. Do not use if simple synchronous calls satisfy requirements.
---

# event-driven-design

## Model events
Name events in past tense as durable facts. Document producers, consumers, schema evolution, ordering guarantees, retention, delivery semantics, idempotency key and correlation ID.
## Reliability
Assume duplicates and eventual consistency unless guarantees explicitly say otherwise. Use transactional outbox for state change + publish, inbox/deduplication for consumers, retries with bounded backoff, dead-letter handling and replay strategy.
## Observability
Track event lag, retries, poison messages and trace correlation across services. Avoid leaking PII into broad event payloads.
## Tests
Contract tests on schemas, duplicate delivery, out-of-order events, retries, and failure between database commit and dispatch. Include a repair/reconciliation procedure.
