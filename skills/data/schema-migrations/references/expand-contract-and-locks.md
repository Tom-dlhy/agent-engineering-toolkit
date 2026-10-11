# Expand–migrate–contract with deployed application compatibility

**Read when:** changing DDL on valuable tables while several
application versions, workers or consumers remain active.

## Release stages
1. Expand with additive columns/tables compatible with old code.
2. Deploy code that tolerates old/new schema, optionally dual-read/write
   with version and reconciliation protections.
3. Backfill in bounded atomic batches, proving no newer writes overwritten.
4. Switch readers and enforce constraints only after validation.
5. Contract/remove columns after old code, replay jobs and integrations
   are retired and destructive operation approved.

A live RENAME COLUMN can break old running binaries: use an
add-copy-switch-remove sequence if zero-downtime compatibility
is required. An application feature flag can't resurrect data
that a DROP permanently erased.

## PostgreSQL lock considerations
DDL lock modes and table rewrites depend on major version,
column type, constraint operations and metadata. CREATE INDEX
CONCURRENTLY differs from regular index and has restrictions;
do not blindly put it inside Alembic transaction block.
Measure lock timeout, WAL/disk, replication lag and write
availability on representative staging.

## Negative tests
Old app after expand, new app before backfill, multiple
worker versions, missing/nullable column, invalid legacy
data, migration interrupted, stale prepared statements,
concurrent updates during backfill and delayed consumer.

Sources: https://www.postgresql.org/docs/current/sql-altertable.html ,
https://www.postgresql.org/docs/current/sql-createindex.html ,
https://alembic.sqlalchemy.org/en/latest/autogenerate.html .
