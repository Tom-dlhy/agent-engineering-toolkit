---
name: snowflake-query-performance
domain: data-platforms
version: "1.0.0"
description: >-
  Use when investigating Snowflake SQL Query Profile, micro-partition pruning, warehouse queueing or spill, clustering and credits for a particular analytic workload. Do not use for generic PostgreSQL tuning, dataset metric definitions or changing warehouse size before collecting query evidence.
---

# Snowflake query performance — measure before resizing

## Mission and diagnosis contract

Optimize an observed Snowflake query workload under correctness, latency, concurrency and credit-cost constraints. SQL engine behavior and cost depend on account edition, warehouse, query shape and physical data distribution. Never present generic tuning folklore or invented benchmark scores as evidence; avoid expensive EXPLAIN-versus-execution confusion and protect live data. Treat a slow query, a busy warehouse and high monthly spend as three separate problems until proven related.

## Intake and baseline

1. Record SQL/query IDs, account region/edition and actual active role (never credentials), data sizes, table type, selected warehouse/cluster configuration, users, concurrency, incident interval and target p50/p95 versus allowed credits.
2. Inspect Query History and Query Profile (only for authorized account/role). Distinguish execution, queue/provisioning, compilation, result caching and network/client fetch time. Profile timings do not necessarily equal end-user round-trip.
3. Capture stable baseline: query hash or exact version, warehouse, filters, parameter selectivity, cold/warm cache assumptions, row counts, bytes/partitions scanned, spilled bytes, queue times, error codes and run date. Don't use an unrelated one-off timing to claim an improvement.
4. Map downstream semantic invariants (joins, aggregation grain, access policies); any rewrite must preserve output and permissions before speed matters.

## Root-cause decision tree

- High partitions scanned relative to prunable range? Inspect predicates, types, expression wrappers, micro-partition overlap and actual table clustering. Check pruning benefit before paying for automatic clustering or Search Optimization.
- High data shuffled/join amplification? Examine join cardinality, data skew, unnecessary cross joins, CTE reuse, filters applied too late and dimensions with duplicate keys. Never remove a JOIN without demonstrating semantic equivalence.
- Local/remote spilling? Identify operator and concurrency/warehouse memory pressure. First reduce data footprint or improve shape; test a larger warehouse only if measurements support it. Some services can cause remote spill metadata even without classic out-of-memory symptoms.
- Query queued? Distinguish concurrency saturation from one badly shaped query. Consider multi-cluster concurrency separately from warehouse size; scaling up is not the same as scaling out.
- Repeated small selective lookups? Check realistic Search Optimization and table type availability/economics, not an automatic index analogue.
- Compilation/client time dominates? Query size, app fetching and caching may be the real issue, not compute.

## Execute an evidence-based experiment

Write a reversible hypothesis and expected signature, change one dimension at a time, preserve result equivalence and compare multiple representative runs at consistent settings. Record confidence, memory/credits and production caveats. Use query tags for controlled attribution where authorized. Avoid running full scans or resizing production warehouses just to benchmark.

## Targeted deep references

- [Query history, profile and measured root causes](references/query-profile-and-diagnostics.md) — **read when** finding queueing, spill, scan cost, joins or representative baselines.
- [Pruning, clustering, search acceleration and rewrite](references/micro-partitions-and-sql-tuning.md) — **read when** choosing a physical/data-layout intervention.
- [Warehouse sizing, credit attribution and safe experiments](references/warehouse-cost-and-workload.md) — **read when** balancing latency, concurrency and spend or proposing warehouse changes.

## Ownership and negative triggers

data/lakehouse-engineering owns cross-engine warehouse/formats choice; data/analytics-modeling owns metric grain; cloud/finops-engineering handles multi-provider budgets; quality/performance-profiling covers generic runtime profiling. This skill owns **Snowflake-specific execution diagnosis**. Snowflake external-table/Iceberg permissions and vendor edition/availability must be checked in official documentation at decision time.

## Completion gate

Report baseline and exact query IDs or anonymized reproducible SQL, evidence from Query Profile, hypothesis, applied versus proposed changes, semantic equivalence checks, measured improvement/credits and rollback. No claim of optimization without observed runs, and no production changes without approval.
