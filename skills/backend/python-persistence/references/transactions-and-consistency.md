# Transactions, concurrency, idempotency and outbox

**Read when:** preventing lost updates, duplicate jobs, inconsistent writes or side effects across SQL and external systems.

## Enforce invariants at correct boundary

- DB unique/foreign/check constraints protect concurrent requests regardless of app code.
- Application checks provide understandable errors but can race before commit; catch unique-constraint violations.
- Optimistic version column/ETag detects stale update; row locks can serialize short critical sections.
- Choose isolation and lock behavior based on actual DB, not assumptions.

## Never hold DB transaction during slow LLM request

Bad: begin transaction → SELECT FOR UPDATE → call Bedrock/Vertex for 60s → UPDATE → commit. This exhausts locks/pool. Better: record job/intention atomically, commit, call external service, then finalize with conditional state/version and idempotency. If consistency cannot be atomic across DB and external provider, define compensations or reconciliation.

## Transactional outbox

~~~text
[DB transaction]
  update business row
  insert outbox event(event_id, type, version, payload)
[commit]
  ↓
publisher polls outbox → sends message
  ↓
consumer deduplicates event_id → applies side effect
~~~

Publisher can crash after send before marking delivered, so duplicates are normal. Event ID and durable idempotency are required. Outbox doesn't give exactly-once effects for an arbitrary external payment/LLM/email.

## Race-test scenarios
Two concurrent PATCH writes; unique name creation; invoice with timeout after remote commit; consumer crash after DB transaction before ack; outbox publisher restart; backfill while old/new app versions coexist.

## Anti-patterns
"check then insert" as sole uniqueness guarantee, automatic retry on failed payment, global DB session, parallel tasks sharing AsyncSession, indefinite lock under API call, fake exactly-once without durable proof.

Official: https://docs.sqlalchemy.org/en/20/orm/session_transaction.html and https://microservices.io/patterns/data/transactional-outbox.html .
