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

## Change window, compatibility and rollback rehearsal

**Read when:** application or infrastructure rollout changes durable
state, schema, external effects or availability characteristics.

### Preflight and authorization packet

Record old and target version/digest, dependencies, health baseline,
SLO and business invariant, deployment owner, approval authority,
exact backup/restore evidence, irreversible operations and
an explicit STOP threshold. Version a deployable artifact and
promote the tested digest, not an unverified rebuild.

When schema compatibility spans releases, prefer a staged
expand/backfill/migrate-consumers/contract sequence with rollback-safe
transitions. Verify what older app versions do during migration
and whether backfill rerun is idempotent. A binary rollback does not
undo deleted columns, charges or notifications.

### Rehearsal matrix

| Failure point | Required observation |
|---|---|
| Before rollout | Known-good health and version baseline |
| New version partial rollout | Compatibility of old/new readers and writers |
| Migration interrupted halfway | Resumable and consistent state or documented repair |
| Remote effect accepted but response lost | No duplicate on retry, reconciliation available |
| Revert requested | Defined safe rollback or forward-repair procedure |

### GO/NO-GO

A release remains NO-GO when critical failures, unverified restore for
irreversible data paths or missing approvals persist. CONDITIONAL GO
must name specific accepted risk and owner, never assume acceptance.
Use actual staged metrics and stop thresholds; no universal 5%/10%
rollout cadence fits all infrastructures.

Example: queue consumer upgrade changes event schema. Deploy dual
reader first, then producer, confirm dead-letter/replay behavior,
finally remove compatibility after measured old-consumer retirement.
Do not unconditionally force a code rollback when accumulated
messages already use the new event shape.

Inspiration:
https://github.com/github/awesome-copilot/tree/main/skills/devops-rollout-plan
