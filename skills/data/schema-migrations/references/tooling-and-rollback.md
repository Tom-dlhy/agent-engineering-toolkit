# Alembic, migration approvals, rollback and restoration

**Read when:** using schema tooling, reviewing migration SQL,
deployment cutover or data backup/recovery.

## Tool automation isn't correctness proof
Alembic autogenerate emits *candidate* changes. It may not
understand column/table renames as intended, data transforms
or full business semantics. Compare schema revisions and
generated DDL manually. Other tools (Flyway, Drizzle) have
different transactional and compatibility behavior.
Run schema upgrade via controlled job, never per replica
startup or untrusted PR with production credentials.

## Go/no-go checklist
Know source/target revision, all still deployed binaries,
dataset size, rewrite/lock impact, backup and restore
evidence, available storage and WAL, rollback/roll-forward
plan, release owner, permitted window and alert thresholds.
Test old and new code against expanded schema before removing
legacy field.

## Down scripts and recoverability
A down() dropping new columns cannot recreate old content
unless preserved. Remote effects of migrations (email,
external export) aren't reversed by DB transaction. Restore
tested under stated RTO/RPO is stronger evidence than merely
possessing an archive. For irreversible changes, prefer
safe roll forward/feature gates and explicit risk sign-off.

## Evidence
Stage upgrade + rollback on disposable DB, migration
lock measurements, error injection after partial batch,
restore drill and old/new API compatibility. Document
missing integration evidence rather than saying "ready".

Sources: https://alembic.sqlalchemy.org/en/latest/autogenerate.html ,
https://docs.sqlalchemy.org/en/20/core/ddl.html ,
https://www.postgresql.org/docs/current/continuous-archiving.html .
