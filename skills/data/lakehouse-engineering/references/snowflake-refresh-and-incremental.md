# Snowflake incremental choices: Dynamic Tables vs Streams + Tasks

**Read when:** choosing warehouse-native transformations, CDC
consumption, refresh goals or orchestrating procedural work.

## Choose native feature by operations
Official Snowflake guidance:
- Dynamic Tables: define declarative SELECT pipeline with
  target lag and supported incremental/full refresh behavior.
- Streams + Tasks: procedural steps, MERGE, stored procedure,
  external calls, conditional branching, strict schedule.
- Materialized Views: single-table query acceleration where
  supported, not general join pipeline/orchestration.
TARGET_LAG sets a freshness goal, **not** exactly every N
minutes and not a zero-lag guarantee.

## Verify actual refresh mode
Incremental eligibility depends on SQL operators, sources,
table type and account features. AUTO may resolve to
FULL despite code hoping incremental; check SHOW DYNAMIC
TABLES resolved REFRESH_MODE and query history/refresh status.
A full-refresh dynamic table is not supported as source
for streams-on-dynamic-table pattern described by Snowflake.

## Streams on dynamic tables
When supported, create stream ON DYNAMIC TABLE, not ON TABLE.
Standard streams capture net changes between consumed offsets,
not every intermediate update. An inserted-and-updated row
may appear only at final state; **streams aren't audit logs**.
If consumer requires each state transition, ingest append-only
audit/change events at original source.

## Cost, operations and QA
Measure credits/warehouse size, refresh volume, failures,
downstream lag, stale stream, reinitialization and replay
idempotence. For a dynamic-table→stream→triggered-task
pipeline, task needs robust upsert/dedupe after recovery.
Separate privileges for warehouse, stream and task.
Validate actual account/version rather than invented pricing.

Sources:
https://docs.snowflake.com/en/user-guide/dynamic-tables/decision-guide ,
https://docs.snowflake.com/en/user-guide/dynamic-tables/streams-on-dts ,
https://docs.snowflake.com/en/user-guide/dynamic-tables/migrate-streams-tasks .
