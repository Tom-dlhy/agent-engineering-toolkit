---
name: schema-migrations
domain: data
version: "0.2.0"
description: >-
  Use when releasing database schema/data changes across running
  application versions, with migrations, online backfill and recovery.
  Do not assume a down migration can undo destructive or external effects.
---

# Schema migration — coexistence, locks, backfill and recovery

## Controlled rollout
1. Record current schema version, application versions, replicas,
   constraints, data volume, DB dialect, existing migration tool,
   backup/restore evidence and change authorization.
2. **Expand** first: additive nullable columns/new tables/indexes
   using dialect-supported online mechanisms. Old application code
   must continue to function alongside new schema.
3. **Backfill** in bounded, restartable batches with stable checkpoint
   and idempotence. Handle concurrent writes, late data, NULL/key
   violations, replication lag and partial progress explicitly.
4. **Switch** application read/write paths with version/feature flags
   and monitor invariants, error rates and compatibility with old code.
5. **Contract** only after consumers are migrated and destructive
   changes explicitly approved. Deleting/renaming a column cannot
   necessarily be reversed by a generated downgrade.
6. Review DDL locking, transactional DDL support, migration job
   concurrency and connection pool; run migration once in controlled
   release job, never once per autoscaled worker.
7. Test old/new service compatibility, DDL/data correctness, dry-run,
   safe rollback/roll-forward and actual restore where authorized.

## Targeted references
- [Expand/contract with application compatibility](references/expand-contract-and-locks.md) —
  **read when** changing columns, constraints, indexes or rolling deploy.
- [Restartable backfill and verification](references/backfills-and-data-migration.md) —
  **read when** migrating populated tables or data formats.
- [Tooling, approvals, rollback and recovery](references/tooling-and-rollback.md) —
  **read when** using Alembic/Drizzle/Flyway or staging/production cutover.

## Boundaries
database-design owns data model; postgres-performance owns plan/index
performance; python-persistence owns ORM migration integration;
release-readiness owns final GO/NO-GO authorization.

## Exit
Reviewed forward migration, coexistence test, bounded data step,
restore evidence, stop criteria, unverified risks; no production
mutation without explicit approval.
