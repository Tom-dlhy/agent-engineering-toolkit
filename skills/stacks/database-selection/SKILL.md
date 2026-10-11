---
name: database-selection
domain: stacks
version: "2.0.0"
description: >-
  Use when choosing or revising a primary database/storage engine for a stated workload, including relational SQL, document, KV, embedded, edge-managed or analytic persistence. Do not use for schema design inside a selected engine, SQL tuning, migration execution or a cloud provider choice without a database decision.
---

# Database selection — correctness, locality and operations before slogans

## Decision path
1. Inspect current schema/driver/ORM and deployment topology. Default to **keeping a sufficient existing engine**; switching is a migration with consistency, downtime, developer retraining and data-repair costs.
2. Characterize data and operation shape: entities/relationships, invariants, multirow atomicity, query patterns, write concurrency and hotspots, client/runtime location, offline-first needs, retention, throughput/latency percentiles, volume/growth, RPO/RTO, residency and tenant partitioning.
3. Define hard constraints and disqualifiers **before** candidate ranking: true transaction/isolation needs, multi-tenant access, durability, cross-region consistency, platform runtime, backup/restore, connection model, licensing and operator capability.
4. Compare credible engine families by documented guarantees **in the specific deployment**. PostgreSQL transactional semantics are not universal NoSQL guarantees; SQLite WAL permits readers with a writer but still only one writer; remote managed SQLite-like products have provider-specific limits/replication. Don't conclude from SQL syntax alone that runtimes have equal concurrency or reliability.
5. Separate **engine** from **managed service**: PostgreSQL protocol vs Neon/RDS/Cloud SQL, SQLite local file vs Cloudflare D1, KV cache vs authoritative storage, warehouse vs OLTP and search index vs system of record. Verify official provider/version/plan quotas and region-specific pricing when deciding.
6. Validate representative query/transaction/connection behavior. Model steady and burst load, cold start, connection pooling vs direct migration URLs, lock contention, read-after-write, backups and *tested restore*, not headline QPS from unrelated benchmarks.
7. Document exit plan: schema/type compatibility, migrations/dual writes only if justified, rollback and verification, export/egress costs, operational alerts and the owner of failure recovery. Never deploy, delete or backfill without permission.

## Deep routing
- [Workload → engine family, consistency and concurrency](references/workload-transactions-and-consistency.md) — **read when** discriminating Postgres/SQLite/document/KV/analytics by real invariants and contention.
- [Managed databases, pooling, serverless and edge tradeoffs](references/managed-serverless-and-edge-databases.md) — **read when** comparing Neon/Postgres, D1, hosted DB plans, drivers or database placement.
- [Migration, backup/restore and evidence-based benchmark](references/database-migration-and-validation.md) — **read when** selecting from an existing system, testing throughput, RPO/RTO, portability or rollback.

## Boundaries
`data/database-design` owns keys/constraints/RLS and tenant schemas; `data/schema-migrations` executes rollout; `data/postgres-performance` owns EXPLAIN and tuning; `data/analytics-modeling` owns mart/BI metrics; `backend/python-persistence` owns SQLAlchemy life cycle; `cloud/cloudflare-d1-database`, `cloud/aws-rds-postgres` and other provider skills own SDK/config. ORM/driver comparison is a supporting decision here or `technology-tradeoffs`, not a new ORM installation framework.

## Exit
A sourced engine/service choice for the actual workload, explicit rejected options, representative tests and operating/restore plan; no invented SLA, concurrency limit or benchmark.
