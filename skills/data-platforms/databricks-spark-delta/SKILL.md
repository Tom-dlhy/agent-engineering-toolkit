---
name: databricks-spark-delta
domain: data-platforms
version: "1.0.0"
description: >-
  Use when optimizing Databricks Spark SQL, PySpark execution, joins, shuffles, Delta Lake tables, liquid clustering, Photon, data files and runtime cost. Do not use for Snowflake Query Profile, generic data metrics, Lakeflow CDC orchestration or unaudited production VACUUM.
---

# Databricks Spark/Delta — correct distributed execution at measurable cost

## Mission and engine gate

Own Spark/Delta **physical execution and transaction semantics** on Databricks, not all data architecture. Confirm deployment cloud, Databricks Runtime (DBR) and Spark version, classic/serverless compute, Photon/Adaptive Query Execution (AQE), Unity Catalog/legacy metastore, Delta protocol and table type. Feature availability and billing change with runtime, workload and cloud; document exact environment. Never infer that passing SQL compiles on every warehouse/runtime.

## Establish correctness and performance baseline

1. Define query/business grain, key uniqueness, data size and file count, update/delete mix, target latency/freshness and budget.
2. Capture reproducible SQL/PySpark, input snapshot, query ID/execution environment, Spark UI stages and SQL profile where available. EXPLAIN is a plan, not measured execution.
3. Compare scan/filter pushdown, file pruning, joins, exchanges, skewed tasks, shuffle bytes, local/remote spill, stage/driver time and result fetch. A fast query that duplicates aggregates or omits filtered rows is incorrect.
4. Decide by evidence: skew -> join cardinality/AQE/salting only if proven; small files -> file maintenance; selective filters -> data skipping/layout; long queues -> capacity/concurrency; joins -> validated broadcast/statistics.
5. Record cold/warm caches, representative concurrency and actual DBU + underlying cloud billing. No fabricated speedup ratios.

## Delta maintenance and layout decisions

- Delta snapshot isolation, transaction log and table protocol enable time travel, schema changes and concurrent operations under specific limitations. Confirm deletion vectors/change data feed requirements before upgrading protocol.
- OPTIMIZE compacts files. For eligible Unity Catalog managed tables, predictive optimization may perform OPTIMIZE automatically. Don't schedule redundant compaction over the same managed tables without measured need.
- Databricks recommends **liquid clustering** for many new Delta tables (DBR and feature gates required), rather than static partitions or ZORDER. Liquid clustering is incompatible with partitioning and ZORDER on the same table. Cluster key changes don't automatically rewrite historical data.
- VACUUM deletes files needed for historical retention. Determine streaming-reader lag, time-travel SLA, legal retention and restore plan before authorizing it; shortened retention is not a cheap default.
- MERGE and schema evolution must handle duplicate source matches, NULLs, idempotent replay and protocol compatibility; test with negative fixtures, not just happy-path insert.

## Experiment and operational method

~~~text
SNAPSHOT + QUERY/PIPELINE ID
 -> PLAN AND PROFILE (scan, join, skew, spill, files)
 -> SEMANTIC EQUIVALENCE / ACCESS INVARIANTS
 -> ONE REVERSIBLE CHANGE IN DEV
 -> MULTI-RUN TIME, DBU, SHUFFLE, FILES, COST
 -> COMPARE REGRESSIONS, RELEASE GATE, BACKOUT
~~~

A resize is not automatically a win; AQE may already coalesce partitions and adjust joins. Confirm actual final adaptive plan and version-specific behavior rather than enforcing shuffle partition numbers arbitrarily.

## Targeted references

- [Spark plans, AQE, skew and query performance](references/spark-plans-joins-and-skew.md) — **read when** interpreting actual stages, skew, joins and Photon.
- [Delta transactions, schema/CDF and safe maintenance](references/delta-transactions-and-maintenance.md) — **read when** upgrading table protocol, performing DML or managing time travel.
- [Liquid clustering, OPTIMIZE, compute and cost](references/liquid-clustering-and-cost.md) — **read when** designing table layout or comparing maintenance versus compute spend.

## Boundaries and exit

data/lakehouse-engineering owns cross-engine file/table-format choices; analytics-modeling owns metric grain; databricks-lakeflow-pipelines owns Auto Loader/AUTO CDC and recovery; databricks-unity-catalog owns access. No live OPTIMIZE FULL, VACUUM, cluster resizing, ALTER TABLE or full refresh without owner authorization.

Output measured bottleneck and profile evidence (or UNRUN), a justified one-change experiment, business-equivalence checks, cost limits, runtime/protocol gate and rollback.
