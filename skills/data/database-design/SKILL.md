---
name: database-design
domain: data
version: "0.2.0"
description: >-
  Use when designing transactional relational schemas, keys, constraints,
  relationships, tenant ownership, isolation and data retention.
  Do not substitute for warehouse dimensional grain, migration execution,
  query plan profiling or ORM lifecycle implementation.
---

# Relational database design — invariants that survive concurrency

## Model decision sequence
1. Understand domain entities/lifecycles, ownership, query/update patterns,
   expected contention, privacy boundaries, delete/retention and evolution.
2. Define natural/surrogate keys, compound uniqueness, foreign keys,
   check constraints, null semantics, cardinality and historical snapshots.
   Enforce invariants in DB where concurrent processes might bypass code.
3. Normalize transactional state enough to preserve correctness, then
   denormalize only when measured reads justify synchronization complexity.
   JSONB is useful for variable attributes but not a free replacement
   for relational queries/constraints.
4. Select correct transaction and isolation strategy based on actual
   anomalies (lost update, write skew, dirty/nonrepeatable/phantom reads),
   not vague "ACID means safe" reasoning.
5. Design tenant access at application and DB layers. PostgreSQL RLS
   applies only when enabled; table owners and BYPASSRLS roles require
   explicit evaluation. Test through **actual application DB role**.
6. Avoid cascade/delete surprises, PII in logs, unbounded exports and
   indefinite retention. Model ownership of encrypted fields and backups.
7. Plan migration through schema-migrations and performance through
   postgres-performance, not premature indexes on every column.

## Open on demand
- [Keys, constraints and relational boundaries](references/keys-constraints-and-normalization.md) —
  **read when** designing tables, relationships, unique constraints and denormalization.
- [Isolation, multi-tenancy and row security](references/transactions-and-tenant-isolation.md) —
  **read when** preventing races, enforcing RLS and ownership.
- [Retention, partitions and schema evolution](references/retention-and-data-lifecycle.md) —
  **read when** planning historic rows, deletion, audit data and retention.

## Boundaries
python-persistence owns SQLAlchemy session/ORM; schema-migrations owns
rollout and backfill; analytics-modeling owns fact/dimension and BI
semantic models; database-selection owns DB product tradeoffs.

## Done
Data model with keys and constraints, authorized negative tests,
concurrency risks, retention policy and intentional query profiles.
