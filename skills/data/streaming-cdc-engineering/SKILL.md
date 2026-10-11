---
name: streaming-cdc-engineering
domain: data
version: "0.1.0"
description: >-
  Use when building database change-data capture or stateful
  stream processing with Debezium, Flink, Kafka, source offsets,
  snapshots, watermarks, windows and checkpoint recovery.
  Do not use for merely publishing business domain events
  or a scheduled batch DAG without stream state.
---

# CDC and stream processing — offsets, event time and recovery

## Decision method
1. Determine if source-of-truth changes are needed (CDC), or if a
   business domain event contract suffices. Assess exact tables,
   snapshot consistency, update/delete tombstones, ordering and PII.
2. For PostgreSQL Debezium, plan consistent initial snapshot,
   replication slot/publication, retained WAL, scoped permissions,
   durable Kafka Connect offsets and monitored connector lag.
   Each independent connector needs appropriate slot management.
3. Define logical primary key, source commit position and schema
   evolution; deduplicate replays and propagate delete/upsert
   semantics to sink. Row-level CDC isn't automatically the
   domain event your product consumers should understand.
4. For stateful Flink, explicitly distinguish **event time**
   and processing time, define watermark/allowed lateness,
   windowing, state TTL and backfill reconciliation. Newer
   DataStream API V2 is described as experimental in current docs:
   confirm actual stable API before choosing.
5. Configure durable checkpoints/savepoints and connector/sink
   semantics. Flink exactly-once **state updates** do not imply
   exactly-once writes to arbitrary downstream HTTP providers.
6. Size Kafka partitions/state backend, catch up burst, WAL
   retention, schema registry and quota. Plan resnapshot on
   lost offsets, slot invalidation or incompatible evolution.
7. Test snapshot→stream cutover, duplicate/reordering, late event,
   schema change, outage/restore and delete propagation end-to-end.

## Reference routing
- [Postgres Debezium snapshot and WAL lifecycle](references/debezium-cdc-and-wal.md) —
  **read when** configuring CDC source snapshots, slots and offsets.
- [Flink event-time windows and watermarks](references/flink-event-time-and-state.md) —
  **read when** building stateful event-time transforms.
- [Checkpoints, exactly-once scope and sink replay](references/recovery-and-sink-semantics.md) —
  **read when** designing durable stream recovery and consistency.

## Boundaries
event-driven-design owns domain event/outbox meaning;
data-pipeline-quality owns broader data validation/lineage;
lakehouse-engineering owns sink table/storage format.

## Exit
Documented event/offset key, snapshot correctness, watermark
and replay policy, connector-specific guarantees and fault tests.
