# SQLAlchemy concurrency, transaction isolation and lost updates

**Read when:** concurrent requests/jobs share database resources,
a session crosses tasks or uniqueness/lock semantics are critical.

## Sessions are units of mutable state

SQLAlchemy 2.0 and 2.1 docs explicitly prohibit sharing one
AsyncSession across independently running asyncio tasks.
A session holds identity map and transaction state, not a
general concurrency-safe connection pool. Share AsyncEngine/
async_sessionmaker, construct **one AsyncSession per task**.

~~~python
from sqlalchemy.ext.asyncio import async_sessionmaker

async def load_one(factory: async_sessionmaker, resource_id: int):
    async with factory() as session:
        return await session.get(Resource, resource_id)
~~~

Resource is a **project-specific SQLAlchemy mapped class**, omitted
from this design excerpt. Awaited loading and session ownership
must fit the project repository interface.

## Lost-update example
Two writers both read balance/version=7, compute new values and
commit. A service-level if-check cannot prevent one overwriting
the other under common default isolation. Options:
- Optimistic version in UPDATE WHERE version=7; require exactly
  one affected row, otherwise return conflict and optionally retry
  bounded operation.
- SELECT FOR UPDATE for short transactional invariant, only
  where supported by actual dialect.
- Unique/FK/check constraints for invariants enforceable in DB.
- SERIALIZABLE transactions with documented serialization
  retries only when necessary and supported.

Isolation level terminology differs by database. SQLite
in-memory tests cannot prove PostgreSQL row locks, isolation
or pool wait; run disposable real DB tests for high-risk cases.

## Fault matrix
Concurrent create of same unique name, stale PATCH update,
deadlock with bounded retry, DB disconnect mid-commit
(unknown outcome), duplicate queue consume, transaction
commit failure and cancellation. Never hold a transaction
across outbound LLM/model calls or slow HTTP provider.

Sources: https://docs.sqlalchemy.org/en/20/orm/session_basics.html ,
https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html and
https://www.postgresql.org/docs/current/transaction-iso.html .
