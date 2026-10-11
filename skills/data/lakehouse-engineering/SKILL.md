---
name: lakehouse-engineering
domain: data
version: "0.1.0"
description: >-
  Use when designing analytic storage and compute choices across
  Parquet, Iceberg, catalogs, Snowflake or BigQuery, including
  partitioning, snapshots, refresh modes and warehouse cost.
  Do not use for OLTP indexes, generic SQL metric definitions
  or CDC source capture configuration.
---

# Lakehouse and warehouse engineering — data layout, table semantics, cost

## Method
1. Identify ingestion/write frequency, analytic query shapes,
   engines, catalog, storage ownership, privacy/residency,
   retention and actual freshness/cost SLO.
2. Separate file **encoding** (Parquet columnar), lakehouse
   **table format** (Iceberg snapshot/schema/partition metadata)
   and managed **warehouse engine** (Snowflake/BigQuery). They are
   not interchangeable choices.
3. Decide snapshot/transaction/concurrency/evolution capabilities
   needed across writers/readers; verify engine version compatibility
   with Iceberg format features, catalog and permission model.
4. On Snowflake select **Dynamic Tables** for declarative refresh
   when query supported; **Streams + Tasks** for procedural MERGE,
   external calls and explicit scheduling; materialized views for
   single-table query acceleration when appropriate. TARGET_LAG
   is a target, not a guaranteed periodic schedule.
5. On BigQuery choose partitions/clustering from actual filters,
   size distribution and cost model; LIMIT alone may not reduce
   on-demand scan cost for unclustered tables.
6. Control file sizes/compaction, vacuum/expiration snapshots
   (avoid deleting referenced files), access policies and
   query bytes/credits. Compare actual price/limits by region.
7. Run engine-specific query plans, correctness at snapshot boundary,
   evolution/backfill tests and billable-resource budgets.

## References
- [Parquet, Iceberg and snapshot evolution](references/columnar-lakehouse-table-formats.md) —
  **read when** selecting file/table format, catalog and maintenance.
- [Snowflake Dynamic Tables versus Streams/Tasks](references/snowflake-refresh-and-incremental.md) —
  **read when** engineering Snowflake declarative/procedural pipelines.
- [BigQuery partitioning, pruning and costs](references/bigquery-partitions-and-cost.md) —
  **read when** optimizing BigQuery analytic storage/query billing.

## Boundaries
analytics-modeling owns SQL fact/dimension grain; data-pipeline-quality
owns data correctness SLIs; streaming-cdc-engineering owns source
change log and stream-time semantics; cloud specialists own IAM/deploy.

## Exit
Format/engine versions, state guarantees, data recovery and warehouse
cost/latency evidence; no invented throughput or price.
