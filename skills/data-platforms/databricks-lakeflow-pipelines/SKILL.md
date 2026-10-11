---
name: databricks-lakeflow-pipelines
domain: data-platforms
version: "1.0.0"
description: >-
  Use when building Databricks Lakeflow Spark Declarative Pipelines, Auto Loader, Lakeflow Jobs, AUTO CDC, SCD2, streaming tables or expectations with recovery. Do not use for Debezium WAL source capture, generic Airflow-only orchestration, Snowpipe or isolated Spark SQL tuning.
---

# Databricks Lakeflow — replayable ingestion, declarative CDC and quality

## Mission

Own **Databricks-specific processing state and operational reliability** from sources to published Delta tables. Distinguish Auto Loader file discovery, Lakeflow Spark Declarative Pipelines transformations, Lakeflow Jobs scheduling, and AUTO CDC ordering. An execution marked SUCCESS is not proof of freshness, correct business keys or complete data.

## Choose the primitive by source/semantics

1. Classify source: immutable staged files, changed files, Kafka/event feed, CDC changelog, periodic snapshots or batch query. Capture business keys, ordering, event/availability/publish time, delete semantics, lineage, PII and freshness SLO.
2. For cloud files, use Auto Loader where applicable, with schemaLocation/checkpoint or managed Lakeflow state. Auto Loader's documented exactly-once processing into Delta does **not** automatically dedupe identical business records in different files. Changing a checkpoint path effectively starts a new stream state.
3. For declarative transforms choose streaming tables vs materialized views based on required freshness, source mutability and supported SQL. Confirm runtime/serverless feature support.
4. For CDC choose **AUTO CDC**, which supersedes legacy APPLY CHANGES for new work. Configure KEYS, SEQUENCE BY (deterministic source ordering), deletion/tombstones, SCD type 1 vs type 2, NULL updates, and a valid initial snapshot.
5. For snapshot-based change detection, prefer documented AUTO CDC FROM SNAPSHOT where valid; it is not the same as reading a source transaction log.
6. Expectations are explicit WARN / DROP / FAIL decisions tied to criticality. Dropping finance/security rows to keep a pipeline green is an unacceptable default.
7. Lakeflow Jobs orchestrate dependencies/retries; external side effects need their own idempotency. A restarted stream does not guarantee exactly-once writes to third-party APIs.

## Operational proof

~~~text
SOURCE CONTRACT / VERSIONED EVENT ORDER
 -> AUTO LOADER or CDC SNAPSHOT/FEED
 -> STREAMING TABLE / MATERIALIZED VIEW / AUTO CDC
 -> EXPECTATION ACTION AND QUARANTINE
 -> RECONCILE KEYS, DELETES, COUNTS AND METRICS
 -> EFFECTIVE FRESHNESS / JOBS ALERTING / REPLAY
~~~

Test same file notification twice, different files with same business key, out-of-order CDC, ties in sequence, delete, type/schema drift, invalid checkpoint, partial failure and concurrent backfill with streaming updates. Configure a bounded replay and lineage-rich exceptions instead of clearing a production checkpoint.

## References (read selectively)

- [Auto Loader schema, file identity and checkpoint recovery](references/auto-loader-and-schema.md) — **read when** ingesting cloud files or evolving schema.
- [AUTO CDC, SCD1/SCD2, expectations and publishing](references/auto-cdc-and-expectations.md) — **read when** modeling ordered changes, deletes and data-quality actions.
- [Lakeflow Jobs, monitoring, backfill and recovery](references/jobs-observability-and-recovery.md) — **read when** restoring pipeline health and proving freshness.

## Boundaries and completion

data/data-pipeline-quality owns generic quality tests; data/streaming-cdc-engineering owns source WAL/Kafka/Flink; databricks-spark-delta owns physical optimization; databricks-automation-bundles owns deployment packaging.

Return source/target contract, stable keys and sequence, SCD and expectation choices, checkpoint and replay path, business reconciliation, actual versus target lag, observed/UNRUN tests, compute cap and approved recovery. Do not reset live checkpoints, drop tables or launch large backfills without human permission.
