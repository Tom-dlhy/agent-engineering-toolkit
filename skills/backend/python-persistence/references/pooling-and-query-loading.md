# SQLAlchemy pool sizing, N+1 and async relationship loading

**Read when:** growing worker count, async lazy-load errors,
high p95 DB latency or unexplained pool exhaustion.

## Pool is not unlimited

Each application process may create an independent Engine/pool.
Total potential DB connections ≈ replicas × workers/process ×
configured pool capacity, plus admin/migration/other clients.
Size against actual DB max connections and burst demand.
A larger pool can worsen DB contention, not necessarily
reduce end-to-end latency. Observe pool checkout wait,
connection age, transaction duration and saturation.

## Async implicit I/O
With AsyncSession, attribute access that attempts lazy SQL
outside supported await context can fail. Prefer explicit
eager relationship loading (selectinload where appropriate)
or explicit awaited IO. Don't return ORM object with
unloaded relationships directly into a Pydantic response
and assume serialization can magically await queries.

### Example query-shape choice
- GET one order: explicit columns/relationships needed.
- List 100 orders with customer names: naive lazy access
  may create N+1 queries; test query count and eager selection.
- Analytical totals: SQL aggregation/read projection may
  be cheaper than loading every ORM row into Python.
- High-volume writes: batch/SQL bulk operations may reduce
  round trips but bypass some ORM identity/event behavior.

## Lifecycle
Create engine during app lifecycle (or controlled bootstrap),
close with await engine.dispose for async engines, open
sessions per request/job. A session per task does not mean
a new engine per request. Avoid storing raw DB credentials
in connection logs/exception traces.

## Testing
Count statements with integration fixture, profile EXPLAIN
for actual Postgres dialect, verify 100+ item list behavior,
model missing row, broken connection, pool timeout and
session cancellation. Mark simulated dialect-only checks
as limited rather than proven production isolation.

Sources: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html ,
https://docs.sqlalchemy.org/en/20/core/pooling.html and
https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html .
