---
name: postgres-performance
domain: data
version: "0.1.0"
description: >-
  Use when diagnosing PostgreSQL slow queries, index choices, locking or connection saturation. Do not add indexes speculatively without workload evidence.
---

# postgres-performance

## Diagnose
Capture representative slow query, planner stats, relevant table sizes and actual parameters. Use EXPLAIN (ANALYZE, BUFFERS) only where execution is safe. Check sequential scans, row estimate errors, loops, sort/spill and missing selectivity.
## Index
Consider composite indexes matching filtering and ordering; avoid write-amplifying redundant indexes. Assess hot paths, partial indexes, vacuum/autovacuum, pagination and connection pool limits.
## Concurrency
Evaluate locks, transaction length, isolation, deadlocks and idle-in-transaction sessions. Use bounded transactions and test migration lock risks.
## Evidence
Measure before/after on comparable datasets, report latency and plan differences, and document rollback or index removal if the optimization fails.
