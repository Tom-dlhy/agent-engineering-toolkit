# PostgreSQL lock contention, pool saturation and incident signals

**Read when:** observing blocked transactions, deadlocks,
high tail latency, connection leaks or replica lag.

## Locate actual bottleneck
Distinguish CPU/IO bottleneck, SQL lock wait, pool checkout
wait, idle-in-transaction and replica replay lag. Inspect
pg_stat_activity, pg_locks, pg_stat_database and optional
pg_stat_statements under least privilege. Wait event types
are useful clues; avoid leaking raw sensitive parameters.

## Connection capacity
Potential connections ≈ replicas × workers × each process
pool max, plus jobs, admin and migration headroom. Adding
connections can increase DB scheduling/lock contention;
size by observed saturation and query duration. Connection
poolers can help but transaction pooling affects session
state, prepared statements, temporary tables and auth setup.

## Transaction hygiene
Short-lived transactions, stable lock order, bounded
statement/lock/idle-in-transaction timeouts and sensible
retry of SQLSTATE serialization/deadlock only when entire
business transaction is replay-safe. Don't kill live
sessions without operator authority/incident procedure.

## Verification
Test two conflicting writes in disposable PG, timeout/
deadlock and retry, pool exhaustion only in approved
staging, migration DDL while reads run, and long transaction
pressure on vacuum. Report measured wait chain and fix,
not speculative diagnosis.

Sources: https://www.postgresql.org/docs/current/monitoring-stats.html ,
https://www.postgresql.org/docs/current/explicit-locking.html ,
https://www.postgresql.org/docs/current/runtime-config-connection.html .
