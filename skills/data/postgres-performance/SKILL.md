---
name: postgres-performance
domain: data
version: "0.2.0"
description: >-
  Use when diagnosing measured PostgreSQL query latency, locking,
  planner decisions, indexes, VACUUM, WAL or connection saturation.
  Do not recommend indexes or production EXPLAIN ANALYZE blindly.
---

# PostgreSQL — evidence-driven planner, index and capacity decisions

## Method
1. Identify **actual server major version**, query fingerprint, bind
   parameter distribution, sizes, selectivity, latency SLO and workload.
2. Inspect pg_stat_statements/metrics where installed and permitted.
   Use EXPLAIN without ANALYZE for nonexecuting inspection. **EXPLAIN
   ANALYZE runs the statement**; writing DML, volatile functions or
   row-locking queries may mutate or block, even inside transactions.
3. Compare estimated versus actual rows/loops, BUFFERS, I/O, sort
   spills, join algorithms, parallelism, materialization and parameter
   sensitivity. Check ANALYZE statistics and extended stats before
   assuming a missing index.
4. Choose B-tree, partial, covering/INCLUDE, BRIN, GIN, multicolumn
   indexes by query and data distribution, not intuition. Account for
   write amplification, HOT updates, VACUUM and index maintenance.
5. Examine locks, deadlocks, idle-in-transaction and pool wait;
   workers × replicas × pool capacity must fit DB max connections.
6. Validate before/after with representative safe workloads,
   concurrent writers, write cost and rollback. A planner plan changing
   does not automatically imply the query became faster.

## Deep reference routing
- [Safe EXPLAIN and planner statistics](references/explain-planner-statistics.md) —
  **read when** investigating slow queries or estimates.
- [Index and table layout decisions](references/indexes-partitioning-vacuum.md) —
  **read when** designing indexes, partitioning or vacuum policy.
- [Locks, pools and PostgreSQL observability](references/locks-and-capacity.md) —
  **read when** dealing with deadlocks, pool saturation or production signals.

## Boundaries
database-design owns schema invariants, schema-migrations owns DDL rollout,
python-persistence owns SQLAlchemy engine/session and query use-case.

## Completion
Safe captured plans, representative inputs, measured latency/errors
and write costs; explicit server version and untested load cases.
