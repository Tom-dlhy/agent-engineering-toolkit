---
name: database-design
domain: data
version: "0.1.0"
description: >-
  Use when choosing relational schema, migrations, transactions, constraints, indexing or persistence boundaries. Do not use for a trivial one-off CSV transformation.
---

# database-design

## Schema design
Identify entities and lifecycle, cardinality, uniqueness, consistency and data retention. Prefer database-enforced constraints for invariants that must survive concurrency. Choose indexes based on actual queries and EXPLAIN plans, not speculation.

## Migrations
Plan backward-compatible expand/migrate/contract steps for deployed systems. Consider locks, long-running backfills, duplicate processing, rollback and cutover verification. Protect personally identifiable information and credentials; validate tenant isolation and row-level access when applicable.

## Transactions
Use the correct isolation level, transaction scope and retry/idempotency behavior. Keep external network calls outside long transactions. Model pagination, N+1 queries and connection limits explicitly.

## Verification
Test real migration up/down paths in staging or disposable DB, validate representative query performance and confirm backup/recovery assumptions.
