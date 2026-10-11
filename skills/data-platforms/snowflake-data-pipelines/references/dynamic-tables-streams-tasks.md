# Dynamic Tables, Streams and Tasks — choose by semantics rather than fashion

Read when: building supported SQL refresh, procedural DML, MERGE, scheduled CDC consumption or downstream refresh dependencies in Snowflake.

## Decision matrix

| Requirement | Choose | Evidence to verify |
|---|---|---|
| SELECT-defined transform and automatically maintained result | Dynamic Table | SQL support, refresh mode, effective lag |
| Conditional MERGE, update, SCD2, external side effect | Stream + Task | Transactions, offsets, task privileges |
| One-base-table acceleration | Materialized View | Query eligibility, maintenance credits |
| Cron/special retry/dependency steps | Tasks | Schedule, overlap and idempotence |
| Source log replication outside Snowflake | CDC specialty | Source offset and delivered events |

Dynamic Tables use TARGET_LAG as a **best-effort staleness target**, not a fixed interval. Actual lag can exceed configured values, particularly with depth/compute constraints. Their result is not a mutable staging table: do not run direct INSERT/UPDATE/MERGE into the Dynamic Table output. Certain SQL patterns are incompatible with incremental refresh, and changing a definition can reinitialize expensive data.

Sandbox-only schema-creating example:

~~~sql
-- Requires a pre-existing authorized warehouse and schema.
CREATE DYNAMIC TABLE DEV_DB.PIPELINE.DT_VALID_ORDERS
  TARGET_LAG = '15 minutes'
  WAREHOUSE = DEV_TRANSFORM_WH
  REFRESH_MODE = INCREMENTAL
AS
SELECT ORDER_ID, CUSTOMER_ID, AMOUNT, ORDER_TS
FROM DEV_DB.RAW.ORDERS
WHERE AMOUNT >= 0;
~~~

Validate the query supports requested REFRESH_MODE (full or incremental), table ownership and freshness chain. DOWNSTREAM has no independent refresh schedule; it needs actual downstream consumers with lag targets or deliberate manual refresh.

Stream offset is transaction-scoped when consumed by committed DML. A plain SELECT from a stream is not equivalent to consuming it and advancing the offset. Test failure-after-read and transaction rollback, stream staleness due to retention and multi-consumer offsets. Multiple consumers may require their own streams.

Illustrative separate sandbox statement:

~~~sql
CREATE STREAM DEV_DB.PIPELINE.ORDERS_CHANGES
ON TABLE DEV_DB.RAW.ORDERS;
-- A separately defined task can guard on:
-- WHEN SYSTEM$STREAM_HAS_DATA('DEV_DB.PIPELINE.ORDERS_CHANGES')
-- and consume changes in INSERT/MERGE with tested restart behavior.
~~~

When matching source changes to a target with MERGE, pre-deduplicate matching keys with ROW_NUMBER and a **deterministic tie-breaker**; mixed inserts/updates/deletes require explicit metadata handling. Retrying tasks must not double-send emails, payments or external side effects. Test a true replay and exception path, not only green Task History.

## Production change prohibition

CREATE OR REPLACE can recreate pipelines and trigger refresh/reinitialization; DROP or stale stream offsets can cause lost change coverage. Require planned migration, preserved source, owner approval and rollback before any live task/pipe/table mutation.

Sources: https://docs.snowflake.com/en/user-guide/dynamic-tables-limitations and https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag and https://docs.snowflake.com/en/user-guide/streams-intro and https://docs.snowflake.com/en/user-guide/tasks-intro
