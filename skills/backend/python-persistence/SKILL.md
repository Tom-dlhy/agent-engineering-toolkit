---
name: python-persistence
domain: backend
version: "2.0.0"
description: >-
  Use when implementing Python SQLAlchemy 2.x repositories, async database sessions, transactions, migrations, unit of work, locking and concurrency. Do not use for NoSQL-only applications or raw Python packaging.
---

# Python persistence — transactions before abstractions

## Decision
1. Identify database, SQLAlchemy/driver versions, consistency invariants, expected writes, transaction boundaries, existing migration tool and connection pool.
2. Decide sync vs async from stack integration; async SQLAlchemy demands async driver and per-task AsyncSession. No session sharing between concurrent tasks.
3. Keep ORM persistence models distinct from transport Pydantic models and domain entities when different invariants exist; avoid generic repository CRUD abstraction without a domain need.
4. Delimit transaction per use case; avoid holding locks while awaiting LLM or external APIs. Use outbox/reconciliation for non-atomic external effects.
5. Plan schema evolution with reversible/expand-contract migrations, data backfills and verification; deploy migrations under controlled job.
6. Size DB pool vs workers and database max connections; instrument slow queries and concurrency before claiming scale.

## Targeted references
- [SQLAlchemy async sessions and mapping](references/sqlalchemy-sessions.md) — read when writing engines, sessionmakers, ORM queries and dependency injection.
- [Transactions, locking, outbox and idempotency](references/transactions-and-consistency.md) — read when enforcing consistency or coordinating DB with external API/LLM.
- [Migrations and performance](references/migrations-and-query-performance.md) — read when changing schema, diagnosing N+1/pool exhaustion or scaling data workloads.

## Related
database-design owns schema domain modeling; postgres-performance owns Postgres query internals; schema-migrations owns generic database evolution.

## Exit
Session ownership explicit; rollback tested; no transaction around long network call; migration forward/backward plan; race/duplicate integration tests; pool sizing and observability.
