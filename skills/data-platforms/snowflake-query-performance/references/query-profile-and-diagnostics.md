# Query History and Query Profile — reproduce the performance diagnosis

Read when: identifying a Snowflake query latency, queue, scan, join, spill or compilation bottleneck from measurements.

## Baseline before changing SQL

Collect account region, role, warehouse, size and concurrency, query ID/hash, SQL version, bound parameters, table size/partition distribution, error status, desired p95 and cost limit. Query elapsed, execution, compilation, overloaded queue, warehouse provisioning, result cache and client fetch times are different observables. A fast reused result cache is not evidence that the underlying execution got faster. Avoid publishing SQL text with private literal values.

Read-only sample, requiring permission to query ACCOUNT_USAGE and subject to reporting latency:

~~~sql
SELECT QUERY_ID, WAREHOUSE_NAME, WAREHOUSE_SIZE,
       TOTAL_ELAPSED_TIME, EXECUTION_TIME, COMPILATION_TIME,
       QUEUED_PROVISIONING_TIME, QUEUED_OVERLOAD_TIME,
       BYTES_SCANNED, PARTITIONS_SCANNED, PARTITIONS_TOTAL,
       BYTES_SPILLED_TO_LOCAL_STORAGE, BYTES_SPILLED_TO_REMOTE_STORAGE,
       ROWS_PRODUCED, ERROR_CODE
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
  AND WAREHOUSE_NAME = 'ANALYTICS_WH'
ORDER BY TOTAL_ELAPSED_TIME DESC
LIMIT 100;
~~~

Time columns above are milliseconds. Actual access may require appropriate database roles; ACCOUNT_USAGE is not instantaneous, so do not interpret missing recent rows as no recent queries.

## Hypothesis by operator

| Observation | Hypothesis to falsify | Evidence or next action |
|---|---|---|
| Scan touches most partitions | Poor pruning / small table | Inspect filter predicates and clustering overlap |
| JOIN output >> input | Duplicate dimensions / many-to-many grain | Validate key uniqueness, row counts, fanout |
| Aggregate or Sort spilled | State size or data skew / memory pressure | Reduce early rows, inspect actual operator |
| Query queued | Warehouse overloaded, not necessarily SQL slow | Compare overlapping sessions and sizing/cluster config |
| Compilation dominates | Huge generated statement or complicated plan | Reduce needless SQL generation in controlled branch |
| Query fast, app slow | Client fetch/serialization or huge result | Instrument application span |
| Remote spill nonzero | Potential out-of-memory; service-specific behavior | Check actual profile before blaming memory |

Query Profile displays operator execution; EXPLAIN alone is a plan, not measured latency. Test semantic equivalence, especially NULL, timezone and privilege-dependent row visibility.

## Controlled experiment output

~~~text
BASELINE: query IDs, input distribution, cold/warm conditions, warehouse
CHANGE: one reversible SQL or resource setting, done in authorized environment
PROOF: same business keys and aggregates and no access-policy regression
MEASURE: repeated p50/p95, scan, spilled bytes, queue and cost estimate
RESULT: observed / inconclusive / unrun, with exact date and environment
ROLLBACK: restore SQL version or authorized test warehouse configuration
~~~

Sources: https://docs.snowflake.com/en/user-guide/ui-query-profile and https://docs.snowflake.com/en/sql-reference/account-usage/query_history and https://docs.snowflake.com/en/user-guide/performance-query-warehouse-memory
