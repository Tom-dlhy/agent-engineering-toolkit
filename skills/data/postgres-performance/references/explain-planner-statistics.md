# PostgreSQL EXPLAIN and planner statistics

**Read when:** investigating real SQL slowness, bad estimates,
unexpected sequential scans or parameter-sensitive plans.

## Safety first
EXPLAIN ANALYZE **executes** the given SQL. For UPDATE/INSERT/DELETE,
SELECT FOR UPDATE or volatile functions it may mutate/lock, even
when the output is just a plan. EXPLAIN without ANALYZE presents
estimates only. Use production EXPLAIN ANALYZE only under explicit
authorization, with safe query, bounded cost and role privileges.

~~~sql
-- Example on authorized read-only SELECT and controlled dataset.
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT order_id FROM orders
WHERE account_id = 42 AND created_at >= DATE '2026-01-01';
~~~

Interpret estimated vs actual rows/loops, buffers reads/hits,
join algorithm, sort/hash spill, IO waits, materialization and
parallelism. A changed plan is not a proven latency improvement.

## Source statistics and parameter skew
ANALYZE collects row stats for planner. Extended statistics
may help correlated columns. Check pg_stat_statements only
if extension installed/configured. Prepared custom/generic
plans and skewed parameters may produce very different p99.
Measure actual query fingerprint against realistic data,
both cold/warm conditions and concurrent load.

## Evidence
Collect DB major version, query and parameter shapes, rows,
table size, stats freshness, before/after p50/p95 and errors.
Consider write overhead and rollback when adding indexes.
Never copy customer PII into public EXPLAIN reports.

Sources: https://www.postgresql.org/docs/current/sql-explain.html ,
https://www.postgresql.org/docs/current/sql-analyze.html ,
https://www.postgresql.org/docs/current/planner-stats.html .
