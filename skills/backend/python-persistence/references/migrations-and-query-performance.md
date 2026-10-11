# SQLAlchemy/Alembic schema evolution and performance

**Read when:** writing migrations, changing public tables or diagnosing slow/blocked DB operations.

## Expand-contract sequence
1. Add nullable/backward-compatible column/table/index.
2. Deploy application capable of old and new versions.
3. Backfill in controlled batches with progress and resumability.
4. Add constraints or nonnullable only after verified data and compatibility.
5. Retire old code/column in later release; record rollback and data recovery steps.

Never run destructive schema migration as a side effect of every API replica startup. Alembic autogenerate produces **candidates**, not reviewed operationally safe migration scripts; check locks, full-table rewrites, data backfills, index creation and DB-specific DDL semantics.

## Query performance
Use EXPLAIN (ANALYZE when safe), actual query counts, row estimates and locks. Fix N+1 via loader strategy where appropriate. Bounded pagination and explicit sort ordering avoid unbounded loads; offset pagination degrades at deep offsets while cursor pagination requires stable keys and semantics.

## Connection management
Probe pool wait, connection lifetime, transaction duration, DB CPU/IO and max connections. App worker count times engine pool ceiling defines potential worst-case connections; adjust to budget and consider pooler. Pool expansion without query fixes can increase overload.

## Verification
Apply migrations against snapshot/staging DB with realistic volume; test old app ↔ new schema compatibility, rollback or roll-forward on failure, concurrent reads during backfill and correct business results.

Official: https://alembic.sqlalchemy.org/en/latest/ and https://docs.sqlalchemy.org/en/20/core/pooling.html .
