---
name: data-pipeline-quality
domain: data
version: "0.2.0"
description: >-
  Use when designing and validating reliable batch ETL/ELT, ingestion,
  data quality, freshness, lineage, contracts and replay/backfills.
  Do not use for only database schema design, dashboard metric grain,
  broker CDC internals or ephemeral notebook exploration.
---

# Data pipeline quality — business-correct, replayable, observable data

## Before implementation
Identify source/owner, lawful use, downstream consumers, business grain,
time semantics, schema/version, expected availability, freshness SLO and
acceptable loss. Distinguish event time, extraction time and load time.
Choose batch or streaming from **latency/business need**, not fashion.

## Execution decisions
1. **Contract:** expected fields/types/nullability, primary/business keys,
   referential integrity, allowed values, uniqueness and drift policy.
   Schema checks do not prove semantic business correctness.
2. **Ingest safely:** immutable raw copy/manifest as warranted, bounded
   parsing, quarantine invalid records and clear source provenance.
   Protect PII and retention; avoid raw private examples in test logs.
3. **Idempotent transforms:** key-based merge or deterministic partition
   overwrite; watermark and lookback for late data; explicit delete policy.
   A timestamp-only max watermark can silently lose out-of-order updates.
4. **Test dimensions:** schema, uniqueness, relationships, freshness,
   completeness, reconciliation, volume anomaly and metric invariants.
   Severity per owner: block publication, quarantine, warn or alert.
5. **Orchestrate:** retry atomic tasks, no partially published files,
   remote object references instead of local executor state; backfills
   use bounded windows and consistent versioned logic.
6. **Observe:** ingestion-to-availability lag, oldest source snapshot,
   dropped/duplicate counts, batch checkpoints, lineage and alerts with
   a real recovery procedure.
7. **Verify:** baseline and negative tests for duplicate, late, missing,
   deleted and schema-changed input; re-run and compare checksums/keys.

## Targeted reference router
- [Ingestion contracts and quality checks](references/contracts-and-tests.md) —
  **read when** defining data contracts, dbt/GX test gates and freshness.
- [Incremental loads, replay and backfill](references/incremental-and-backfills.md) —
  **read when** implementing watermark, UPSERT, late arrival or correction.
- [Airflow orchestration and safe task retries](references/airflow-and-orchestration.md) —
  **read when** building DAGs, schedules and retry-safe task outputs.
- [Operations, privacy, lineage and incident recovery](references/lineage-privacy-and-operations.md) —
  **read when** monitoring pipelines, troubleshooting stale/partial data,
  protecting sensitive records or determining restore/rollback.

## Boundaries
analytics-modeling owns fact/dimension grain and consumer metric definitions.
streaming-cdc-engineering owns WAL/CDC and event-time state/checkpoint behavior;
lakehouse-engineering owns storage format/catalog and warehouse optimization.
test-strategy owns generic testing, event-driven-design owns business events.

## Completion
Source and output contract, durable/replay policy, tests with negative
cases, runbook, owner and realistic cost/latency constraints. No
production-quality claim solely from YAML or successful DAG parse.
