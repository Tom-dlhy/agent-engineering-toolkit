---
name: python-persistence
domain: backend
version: "2.1.0"
description: >-
  Use when implementing Python SQLAlchemy repositories, AsyncSession lifecycle,
  migrations, transactions, constraints, concurrency and persistence performance.
  Do not use for NoSQL-only stores or abstract service design unrelated to SQL.
---

# Python persistence — DB invariants and transactions are first

## Method
1. Pin **SQLAlchemy 2.x or explicitly chosen 2.1**, driver/dialect and DB version; do not assume all async behaviors or migrations are portable across releases.
2. Choose sync/async from actual driver/API concurrency needs. Engine/pool is reusable; **one mutable Session per thread or AsyncSession per task**. Sharing session inside `asyncio.gather` is unsafe.
3. Assign use-case transaction owner, rollback on failure and ensure DB constraints for uniqueness, tenant isolation and business invariants. An ORM precheck doesn't prevent races.
4. Prevent lazy implicit I/O in async ORM; use explicit loading/selectinload or targeted query. Don't serialize arbitrary ORM relationships into HTTP.
5. Validate isolation, conflict handling, pool exhaustion and connection limits under true target DB; SQLite tests don't prove PostgreSQL locks/constraints.
6. Review Alembic autogeneration manually; plan expand/backfill/contract, safe DDL, rollback or forward repair. Avoid migrations per autoscaled worker and external calls inside open DB transaction.
7. If DB state triggers external event, keep transactional outbox intent local; publisher may duplicate, so consumer/idempotence is separate.

## References
- [SQLAlchemy sessions/async mapping](references/sqlalchemy-sessions.md) — read when wiring AsyncEngine/AsyncSession.
- [Transactions, locking and outbox](references/transactions-and-consistency.md) — read when guaranteeing DB invariants.
- [Migrations and SQL performance](references/migrations-and-query-performance.md) — read when deploying schema and profiling queries.
- [Concurrency/isolation failure matrix](references/concurrent-session-and-isolation.md) — read when testing stale writes, concurrent tasks or locks.
- [Pooling and query loading in production](references/pooling-and-query-loading.md) — read when dealing with N+1, pool exhaustion and async lazy loads.

## Boundaries
database-design models relational schema; postgres-performance owns
PostgreSQL planner internals; event-driven-design owns message replay.

## Exit
Real dialect/session ownership, transaction/rollback, race-negative tests,
safe migration plan, measured pool and no unbounded lock-held I/O.
