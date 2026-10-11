# Relational data lifecycle, partition retention and restore

**Read when:** designing time-series history, audit records,
PII retention, archival and database partitioning.

## Retention has many copies
Operational table, history and snapshots, CDC logs, warehouse,
backups and analytics exports all need data-access and
retention decisions. Lawful retention/deletion depends on
purpose and jurisdiction; consult authorized legal/security
owner rather than claiming automatic regulatory compliance.

## Partition when warranted
Postgres partitioning can reduce scanned data and make
old-window retention manageable, but adds planning/maintenance
cost, constraint rules and per-partition index choices.
Check actual query predicates and partition pruning with
representative plans. Too many small partitions or no
partition-filtered queries can be worse than simpler design.

## Safe delete/backups
Dropping a partition or archive snapshot may be destructive.
Before cleanup check dependent consumers, legal holds,
pending backfill and restore window. A backup exists ≠
a restore works. Record RPO/RTO, test staging restore
and account for sensitive data in archived backups.

## History design
If preserving event audit, append-only history of domain
transitions differs from mutable current-state table.
Use version/source timestamp and corrections policy.
Soft deletion is a product state, not automatically
complete erasure of replicated personal information.

## Verification
Boundaries at partition rollover, old/new readers,
FK cascades, legal hold, timed restore, multitenant export,
delete propagation to downstream marts, retention
expiration and concurrent writes during archive cutover.

Sources: https://www.postgresql.org/docs/current/ddl-partitioning.html ,
https://www.postgresql.org/docs/current/continuous-archiving.html .
