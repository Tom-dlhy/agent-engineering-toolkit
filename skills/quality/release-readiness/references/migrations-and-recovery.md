# Migrations, backward compatibility and recovery

**Read when:** shipping schema or data migrations, rotating secrets,
migrating providers or changing persistent/irreversible state.

## Expand → migrate → contract

1. Deploy additive backward-compatible schema first.
2. Make readers/writers support old and new shape as required.
3. Backfill with bounded resumable batches and progress metrics.
4. Validate referential/business invariants and old/new app compatibility.
5. Only then enforce constraints/drop legacy columns in a later step.

Auto-generated Alembic/ORM migration scripts are drafts. Review lock
duration, DDL transactional behavior, index creation and data volume.
Deploy migration as controlled job, **not** at every autoscaled replica
startup. Snapshot recovery and test a restore to a *working* staging
environment; a backup file alone isn't a verified rollback.

## Rollback is not always possible

Rolling back a container image does not reverse executed emails,
money movements, client data writes or irreversible schema changes.
Prefer feature flag/routing stop, roll forward compatibility and
compensating/reconciliation tasks when needed. Maintain durable
idempotency keys for repeated external actions and retention-aware
deletion/recovery.

## Failure injection

Backfill interrupted at row 500, concurrent writes during schema
change, service built against old contract, expired identity token,
read model lagging, and transaction committed before queue publish.
Validate dual-write/outbox and retry dedupe where appropriate.
Rehearsal must be against synthetic/sanitized realistic data and
explicitly authorized resources, not production data by default.

## Decision output

Migration revision, expected lock/lag, roll-forward and rollback
steps, data-loss/reconciliation risk, restore evidence, dependency
compatibility matrix, operator and stop conditions.

Official: https://alembic.sqlalchemy.org/en/latest/ and
https://docs.sqlalchemy.org/en/20/orm/session_transaction.html and
https://docs.github.com/en/actions/deployment/about-deployments/deploying-with-github-actions .
