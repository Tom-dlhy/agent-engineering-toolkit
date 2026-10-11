---
name: snowflake-data-pipelines
domain: data-platforms
version: "1.0.0"
description: >-
  Use when implementing or troubleshooting Snowflake ingestion and incremental ELT with COPY INTO, Snowpipe, Dynamic Tables, Streams, Tasks, MERGE or backfills. Do not use for generic Airflow orchestration, CDC source capture or metrics-only dbt modeling without Snowflake-specific services.
---

# Snowflake data pipelines — decide by refresh semantics and recovery

## Mission

Build replayable, correct, observable ingestion and transformation across Snowflake-managed primitives. Do **not** equate "job succeeded" with durable business correctness or "TARGET_LAG = 10 minutes" with a cron schedule/guaranteed SLA. Distinguish data arrival, source event time, load time, publication time and query visibility.

## Choose the right mechanism

1. Inventory source: staged files (S3/Azure/GCS), connectors, change stream, latency, data volume, schema volatility, PII, permissions and ownership.
2. For bulk scheduled staged loads: consider COPY INTO with warehouse, file format, load validation and explicit file manifests. For continuously arriving staged files: evaluate Snowpipe notification/REST and pipe history; Snowpipe is micro-batch, not magic per-record transactional streaming.
3. For declarative supported SQL transforms and target freshness: consider **Dynamic Tables**. Test supported query constructs and actual incremental/full refresh mode; target lag is a best-effort freshness target.
4. For procedural MERGE, upsert, SCD2, stored procedures, conditional actions, external effects or precise dependencies: choose **Streams + Tasks**. A stream tracks table change metadata/offset; consuming within a committed DML transaction advances its offset. Mismanaged retries or stale streams can lose coverage.
5. For event streaming/CDC outside Snowflake, hand off to streaming-cdc-engineering; once staged inside Snowflake, this skill owns platform-specific load semantics.
6. Define publication boundary: immutable staging, dedupe and business keys, correction/delete handling, replay window, initial snapshot and source schema contract. Never assume file name metadata guarantees business idempotency.

## Operational flow

~~~text
SOURCE + PERMISSIONS
 -> STAGE / FILE MANIFEST / RAW CONTRACT
 -> COPY or SNOWPIPE + LOAD VALIDATION
 -> TRANSFORM (DYNAMIC TABLES or STREAMS/TASKS)
 -> RECONCILE COUNTS / UNIQUE KEYS / DELETIONS
 -> PUBLISH AT AGREED FRESHNESS
 -> MONITOR LOAD/REFRESH / COST / ERROR / REPLAY
~~~

Test duplicate-file replay, renamed/reused filename, overlapping merge keys, out-of-order arrival, schema change, zero rows, delete/tombstone, interrupted task and backfill overlapping live ingestion. Strict business keys matter: Snowflake standard tables do not generally enforce UNIQUE/PRIMARY KEY constraints as one might assume from OLTP engines. Prefer an explicit deduplication and reconciliation contract.

## Deep references, read selectively

- [Stages, COPY and Snowpipe load/replay contract](references/stages-copy-snowpipe.md) — **read when** creating file-load pipeline, preventing duplicates, or debugging ingestion.
- [Dynamic Tables versus Streams/Tasks and MERGE](references/dynamic-tables-streams-tasks.md) — **read when** choosing SQL refresh/update semantics or task scheduling.
- [Backfill, monitoring and publication verification](references/backfill-observability-and-qa.md) — **read when** repairing stale data, orchestrating replays or assessing quality SLIs.

## Boundaries

data/data-pipeline-quality owns general contracts and freshness SLI; lakehouse-engineering owns table-format and cross-engine choices; analytics-modeling owns marts/business metrics; streaming-cdc-engineering owns source WAL and log offsets. This skill owns **Snowflake implementation**, including platform-specific load history, refresh conditions and permissions. No automatic creation/replacement of stages, tasks, integrations, or deletion of files/streams on production.

## Done

Document chosen primitives, least-privilege role, source/storage integration, valid SQL and versions, business grain/keys, rollback/backfill and data reconciliation. Provide actual negative test results or label them unrun. Confirm actual lag, not just requested lag, and cost controls before unattended operation.
