# Incremental ingestion and restartable backfill

**Read when:** using dbt incremental, MERGE, timestamp watermark,
late event lookback, historic replay and delete propagation.

## Timestamp alone is not a correctness guarantee
Filtering with updated_at greater than max(target) misses
equal-time changes and late/out-of-order records; clock skew
can worsen it. Use source commit position or a bounded overlap,
stable key/version ordering and reconciliation. Deduplicate
per actual business grain before merge.

dbt is_incremental() requires an existing target table, an
incremental materialization and no full-refresh flag. An
optional unique_key influences update behavior by strategy;
it is **not** a uniqueness constraint. Null composite keys
and duplicate source records can silently break upsert.

~~~sql
-- Conceptual warehouse SQL; actual dialect syntax/locking varies.
MERGE INTO clean_orders target
USING staged_deduplicated_orders source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET
  amount = source.amount, source_version = source.source_version
WHEN NOT MATCHED THEN INSERT (order_id, amount, source_version)
VALUES (source.order_id, source.amount, source.source_version);
~~~

The sketch assumes source uniqueness and no stale overwrite;
real code needs version predicates, deletes, permissions
and transaction semantics suited to the engine.

## Backfill protocol
Choose immutable source snapshot and time partition range,
preflight counts/checksums, bounded staging batches,
resumable checkpoint after durable write, reconcile totals,
atomic swap/merge only where supported, then audit/cleanup.
Backfill must not issue duplicate emails/payments or
accidentally overwrite more recent corrections.

## Tests
Same input twice, equal timestamp/different key,
late correction, tombstone delete, conflicting duplicate,
checkpoint crash, current + historic overlap, full-refresh
comparison and idempotent partial rerun. Budget cost and
retention for large historic replay.

Sources: https://docs.getdbt.com/docs/build/incremental-models ,
https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html .
