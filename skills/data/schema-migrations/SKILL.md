---
name: schema-migrations
domain: data
version: "0.1.0"
description: >-
  Use when altering persistent database schemas in applications with deployed instances or valuable data. Do not treat data migrations as reversible just because DDL has a down migration.
---

# schema-migrations

## Strategy
Prefer expand–migrate–contract for rolling deployments: add compatible schema, deploy dual-read/write or translation if needed, backfill idempotently, switch readers, then remove old paths after verification.
## Risks
Identify table size, lock duration, transaction scope, backfill checkpoints, uniqueness and null constraints. Separate schema changes from large data rewrites where possible.
## Backup and rollback
Validate backups and restoration, not just existence. Document how to revert application behavior without destroying data. Stop for destructive operations and request approval.
## Tests
Run migrations against realistic disposable datasets, check old/new application compatibility, measure lock/time cost and verify post-migration invariants.
