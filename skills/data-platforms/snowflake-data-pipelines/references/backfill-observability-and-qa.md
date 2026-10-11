# Snowflake replay and pipeline QA — reconcile before publication

Read when: implementing historical backfill, repairing stale or wrong data, validating late changes, or defining task/pipe/Dynamic Table observability.

## Correctness and freshness contract

Separate source event time, source availability, Snowflake ingestion timestamp and consumer publication time. Define a source-of-truth table/file manifest, business key and grain, data retention/legal requirements, expected late arrivals, error budget and **actual** freshness SLO. Target lag is an aspirational service setting, not observed SLO.

Replay a window only if source is versioned or immutable enough to reconstruct the same meaning. A naive MAX(last_loaded_at) watermark may miss late corrections and deletes. Use durable checkpoints, bounded lookbacks plus merge by source version, or full reconciliation by business key.

## Rehearse before production

~~~text
SOURCE & SNAPSHOT: immutable manifest/version and authoritative counts
WINDOW: half-open UTC bounds, estimated rows/bytes, consumers
WRITE CONFLICT: live pipeline during replay? pause/dual-read/merge plan
BUSINESS KEY: dedup ordering and delete semantics
LOAD PATH: stage/COPY/Snowpipe versus Dynamic Tables/Streams/Tasks
QUARANTINE: invalid/corrupt data and producer reconciliation
BUDGET: warehouse cap, runtime, observer and stop trigger
PUBLISH: versioned output/safe cutover and rollback with owner
VERIFY: count, distinct keys, finance totals, partitions and access policy
~~~

Do not edit production pipelines on behalf of a test suite. Keep backfill and live ingestion independent until reconciliation is proven.

## Negative fixtures

- Duplicate source record, distinct filenames → one canonical row or explicit versioned history.
- Arrives out of order → latest source version wins, not highest load timestamp.
- Deleted ID/tombstone → removal/historical retention per policy.
- Transaction fails before stream consumption commit → offset not silently lost.
- Stream retention exceeded → fail loudly, restore from authoritative snapshot; don't fake offset repair.
- Dynamic Table reinitializes → effective lag and consumer correctness monitored.
- Permission revoked/stage unavailable → alert and no false “fresh” green signal.
- Concurrent backfill/live update → deterministic key conflict rule.

## Instrument the real pipeline

Observe stage notifications, files seen vs loaded, source watermark, COPY/Snowpipe load errors and backlog, task history states plus **records produced**, stream backlog and staleness, Dynamic Table refresh history/effective lag, output reconciliation and warehouse/serverless credits. Different history views can be delayed and require grants; document source/latency of each SLI.

A conceptual readiness predicate:
~~~text
ready =
  (latest_published_source_timestamp >= latest_expected_source_timestamp - SLO)
  AND (critical_missing_keys == 0)
  AND (critical_duplicate_keys == 0)
  AND (reconciliation_mismatch == 0)
~~~
Actual expected source timestamp must be validated separately: if upstream hasn't sent data, a self-referential last-ingested watermark may hide an outage.

A green pipeline with bad business metrics is a **failed publication**. Alert with a named owner, instructions to quarantine/replay and data consumers to notify, where appropriate. Missing account access means state must be marked UNVERIFIED.

Sources: https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro and https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag and https://docs.snowflake.com/en/user-guide/tasks-intro and https://docs.snowflake.com/en/user-guide/dynamic-tables-monitor
