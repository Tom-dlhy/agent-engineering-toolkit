# SQLAlchemy 2.x sync/async mapping and session scope

**Read when:** implementing SQLAlchemy persistence, unit-of-work boundaries or request-scoped DB sessions.

~~~python
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)

engine = create_async_engine(
    "postgresql+asyncpg://app:REDACTED@db.example/app",
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True,
)
SessionFactory = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)

async def get_resource(session_factory=SessionFactory):
    async with session_factory() as session:
        resource = await session.get(ResourceRow, 1)
        return resource
~~~

Never hardcode a production connection URL/password; inject from settings/secret manager. This example refers to an application-defined mapped ResourceRow. Dispose engine on app shutdown. SQLAlchemy warns: **do not share one AsyncSession across concurrent asyncio tasks**. Each transaction/task owns session; session is a mutable transaction context, not a thread-safe cache.

## ORM query patterns

Use SQLAlchemy 2-style select() and result handling, selectinload/joinedload deliberately; avoid implicit async lazy loading after session close. Convert ORM models into safe DTOs while session is open; never return persistence row objects directly as public API responses if they expose secrets/relationships.

## Transaction lifecycle

Keep commits in one clear unit-of-work/application boundary. Don't silently commit in every repository.save() then discover two writes cannot be rolled back together. Use session.begin() when atomic set of writes required; on exception transaction rolls back.

~~~python
async with SessionFactory.begin() as session:
    session.add(ResourceRow(name="demo"))
    # more related DB writes in same transaction
# commit on clean exit, rollback on error
~~~

## Pool strategy and scaling

One worker with pool_size=5/max_overflow=5 may open up to 10 connections; with 8 workers this could yield 80 before other services. Evaluate DB maximum, proxies/poolers and long queries. Async will not fix missing indexes, N+1 or held locks.

## Integration tests

Use a disposable real database with migrations, unique constraints and concurrent updates for critical workflows; SQLite in-memory tests are not equivalent to Postgres isolation or JSON/DDL behavior.

Official: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html and https://docs.sqlalchemy.org/en/20/orm/session_transaction.html .
