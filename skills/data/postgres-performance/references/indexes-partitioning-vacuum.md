# PostgreSQL indexes, table layout and vacuum

**Read when:** choosing B-tree/BRIN/GIN/partial indexes,
partitioning and maintenance under measured workloads.

## Index selection by predicates
B-tree fits common equality/range/order. Multicolumn order
and selectivity matter; PostgreSQL 18 introduced more
multicolumn skip-scan possibilities, but validate server
version and plan. Partial index requires queries whose
predicate implies indexed subset; parameterization may
affect planner matching. INCLUDE can cover columns but
adds size/write cost; index-only scans also depend on
visibility map. GIN fits appropriate JSONB/array/search
operators. BRIN fits physically correlated large ranges.

## DDL and operational trade-offs
CREATE INDEX CONCURRENTLY may reduce blocking of writers,
but has restrictions, can be slower and can leave INVALID
index after failure. Review tool/migration transaction
behavior: don't execute concurrently-index build inside
unsupported transaction blocks. Every index slows some
writes and consumes storage/WAL/maintenance.
Partitioning helps when pruning or time-based retention
is useful, but too many small partitions can worsen
planning and constraints.

## Vacuum and dead tuples
Postgres MVCC leaves dead rows; autovacuum and ANALYZE
keep table/storage/stats viable. Long-running transactions
can prevent cleanup and amplify bloat. Avoid disabling
autovacuum or making global settings without real evidence.

## Tests
Compare before/after plans and wall latency with realistic
data, low/high selectivity, concurrent writes, index size,
lock behavior and no unauthorized mutation. If no material
improvement or write regression, revert index safely.

Sources: https://www.postgresql.org/docs/current/indexes.html ,
https://www.postgresql.org/docs/current/sql-createindex.html ,
https://www.postgresql.org/docs/current/routine-vacuuming.html .
