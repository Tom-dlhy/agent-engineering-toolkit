# Restartable data backfill under concurrent writes

**Read when:** populating schema columns, data corrections,
type conversion or large historical migration.

## Plan bounded work
Define immutable input snapshot if possible, a stable key
range, small transaction batch, version conflict policy,
durable checkpoint and verification. Whole-table UPDATE
can threaten locks, WAL and replication; chunk and monitor.

~~~sql
-- Conceptual Postgres SQL; parameters bound by application.
UPDATE events
SET event_day = event_at::date
WHERE event_id >= :lower AND event_id < :upper
  AND event_day IS NULL;
~~~

A production migration also needs timezone policy, affected-row
monitoring, permissions and concurrency controls. The placeholder
SQL must never be executed without an actual bound driver.

## Replay correctness
A checkpoint records last **committed** batch. A repeated
window should not duplicate history or overwrite a newer
source correction. Run against realistic synthetic data,
compare key uniqueness, null rates and checksum by partition,
check data retention and source version. If interrupted,
resume on known boundary and revalidate.

## Migration risk
Changing type can overflow or reinterpret timezone.
Renaming and deleting original fields may destroy rollback
data. Backfills must not call external email/payment service
as a side effect on every row. Track observed transaction
time, lag and storage, with operator stop criteria.

## Tests
Crash halfway, rerun range, concurrent writer, corrupt
legacy value, daylight saving, duplicate key, unexpected
NULL, old/new reader and rollback or forward repair.

Sources: https://alembic.sqlalchemy.org/en/latest/ops.html ,
https://www.postgresql.org/docs/current/sql-update.html ,
https://www.postgresql.org/docs/current/monitoring-stats.html .
