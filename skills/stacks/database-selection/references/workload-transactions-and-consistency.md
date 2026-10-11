# Persistence workloads: invariants, writers, reads and consistency

Read when: choosing transactional PostgreSQL/SQLite, document, key-value or warehouse storage for a specific correctness and workload profile.

## The database decision starts with invariants
Declare multirow atomicity, conflict semantics, referential constraints, natural vs query-centric data access, latency distribution, replication/freshness and recovery obligations. A DB can technically support a query while being a poor operational fit for the load and failure model.

| Shape | Plausible candidates | Verify before recommending |
|---|---|---|
| Interrelated mutable entities, cross-record invariants | PostgreSQL / other ACID relational | Isolation anomalies, migrations, locks, query workload |
| Embedded/local single-file/offline data | SQLite | File ownership, concurrency, WAL/checkpoint and backup |
| Distributed key/value access with simple lookups | provider KV/document database | Per-key/transaction semantics, eventual consistency, hot partitions |
| Historical analytic scans | warehouse/lakehouse | ETL cost, freshness, analytical grain, cost per scan |
| Cache of recomputable values | Redis/KV | TTL, eviction, cold start and source of truth |
| Search index | purpose-built search or DB text search | Reindex pipeline, stale result, authoritative DB |

**SQLite WAL** supports concurrent readers with a writer, **but only one writer at a time** in the same WAL file. It is inappropriate to claim unlimited concurrent writers merely because WAL is on. Some managed SQLite-compatible services differ: do not transfer native SQLite guarantees to D1/Turso without provider documentation. <https://www.sqlite.org/wal.html>.

**PostgreSQL** supports multiple transaction isolation levels; `SERIALIZABLE` can require application retries on serialization failures, and common `READ COMMITTED` does not automatically ensure an application's multi-request business invariant. See exact current PostgreSQL docs instead of using the word "ACID" as proof all races disappear.

## Threat to correctness fixtures
- Two clients decrement same last inventory item: prevented by atomic conditional update/lock/constraints or suitable isolation.
- Concurrent tenant inserts: unique tenant+external ID must survive races.
- Event ingestion duplicates after worker retry: idempotency at durable boundary.
- Replica serves stale account state after immediate write: state whether read-after-write consistency is required.
- Restore point older than paid order: quantify tolerated loss (RPO), not simply "backups enabled".

The engine selection doesn't implement schema constraints; hand off to `data/database-design` and `data/schema-migrations`.

Sources: https://www.postgresql.org/docs/18/transaction-iso.html and https://www.postgresql.org/docs/18/tutorial-transactions.html and https://www.sqlite.org/wal.html
