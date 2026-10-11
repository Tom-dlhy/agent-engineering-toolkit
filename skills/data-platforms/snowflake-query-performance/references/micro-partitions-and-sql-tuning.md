# Micro-partitions, pruning, clustering and query rewrite

Read when: scanned partitions, selectivity or data-layout choices dominate a measured Snowflake analytic workload.

## Understand the engine rather than treating it like PostgreSQL

Snowflake manages micro-partitions and columnar metadata. User-designed clustering keys are not ordinary B-tree indexes and may add maintenance credits. Natural ingestion order may already provide enough pruning. Recommend a clustering key only for sufficiently large and repeatedly filtered tables with evidence from Query Profile, distribution and expected maintenance cost.

Decision order:
1. Preserve actual business grain and SQL result before optimization.
2. Inspect scanned / total micro-partitions and whether predicates enable pruning.
3. Try a semantically equivalent bounded predicate and projection before permanent table-layout changes.
4. Investigate fanout (many-to-many joins), wide VARIANT columns and unnecessary sort/aggregate state.
5. Evaluate actual clustering depth, selective workloads and key cardinality before clustering.
6. Consider Search Optimization only for supported selective patterns, materialized views for eligible repeated single-table computations, and QAS only where supported and cost-justified.
7. Measure benefit versus credits, query frequency and mutation overhead.

Illustrative read-only query to validate actual timezone/type semantics:

~~~sql
SELECT ACCOUNT_ID, COUNT(*) AS PURCHASES
FROM ANALYTICS.EVENTS
WHERE EVENT_TS >= '2026-01-01'::TIMESTAMP_NTZ
  AND EVENT_TS <  '2026-02-01'::TIMESTAMP_NTZ
GROUP BY ACCOUNT_ID;
~~~

This half-open filter is not guaranteed faster: it depends on EVENT_TS type, micro-partition arrangement and original filter semantics. If business reporting uses a local timezone, convert the requested period correctly before using an NTZ comparison. A rewrite that produces different totals is a failure regardless of speed.

| Option | Choose only if | Reject/stop if |
|---|---|---|
| SQL rewrite | Output equal, fewer scans/joins | Changed null/calendar semantics |
| Clustering | Large frequently scanned table benefits sustainably | Maintenance exceeds savings |
| Search Optimization | Supported selective access and query shape | Bulk scans dominate |
| Materialized view | Eligible precomputed stable query | Unsupported logic, maintenance penalty |
| Larger warehouse | Measured compute/memory saturation | Actual fault is bad pruning or queue contention |

Never CREATE, ALTER or recluster an expensive production table as the first diagnostic. Use sandbox copies and plan cost first.

Sources: https://docs.snowflake.com/en/user-guide/tables-micro-partitions and https://docs.snowflake.com/en/user-guide/tables-clustering-keys and https://docs.snowflake.com/en/user-guide/search-optimization-service and https://docs.snowflake.com/en/user-guide/views-materialized
