---
name: event-driven-design
domain: architecture
version: "0.2.0"
description: >-
  Use when designing business events, asynchronous messaging, webhooks,
  distributed consistency, transactional outbox, idempotent consumers,
  saga orchestration or replay. Do not replace sufficient synchronous
  calls or local transactions with an event bus by default.
---

# Event-driven architecture — failure semantics before broker names

## Procedure
1. Decide **why async**: durable long jobs, decoupled independently owned
   consumers, spikes or data propagation. A queue is not inherently safer
   than a local function for short strongly consistent work.
2. Distinguish event (past business fact) from command (desired action)
   and notification (a change of interest). Define producer ownership,
   schema/version, correlation and per-aggregate ordering needs.
3. Specify delivery and **failure contract**: most practical broker
   integrations require at-least-once processing with possible duplicates,
   out-of-order messages, delays and poison events. Do not claim
   exactly-once **end-to-end side effects** without evidence.
4. If a DB change must publish an event, use **transactional outbox** in
   the same DB transaction; publisher can resend, so consumer idempotency
   and inbox/dedupe remain necessary.
5. For multi-service business transactions, select a saga only with
   explicit local transaction, timeout, compensation and reconciliation
   design. Choreography vs orchestration is a complexity trade-off.
6. Design bounded retries/backoff/DLQ, retention and replay,
   schema compatibility, tenant and PII controls, per-key order and
   tracing/lag metrics.
7. Run fault-injection tests at *crash windows*: before commit, after
   commit before publish, after publish before ACK, duplicated event
   and out-of-order delivery.

## Targeted references
- [Event contracts, ordering, AsyncAPI and compatibility](references/event-contracts-and-semantics.md)
  — **read when** designing event schemas, ordering, partition keys,
  consumer boundaries or delivery guarantees.
- [Transactional outbox and idempotent consumer](references/outbox-inbox-and-idempotency.md)
  — **read when** integrating state mutation with publish,
  replay and deduplication.
- [Saga, compensation and recovery](references/saga-and-reconciliation.md)
  — **read when** coordinating multiple services/DBs,
  partial commits, compensating actions or long workflows.

## Boundaries
background-jobs handles Python queue worker selection/runtime;
python-persistence handles SQL session/UoW/locking; modular-monolith
handles module ownership; api-contract-design handles public
webhook/API contract compatibility.

## Done
Event identity, independent consumers, failure matrix, consistency
expectation, security, recoverability, observability and executed
integration/simulation tests documented.
