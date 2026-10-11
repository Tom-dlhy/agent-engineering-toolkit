# Debezium PostgreSQL CDC: consistent snapshot and WAL lifecycle

**Read when:** configuring Postgres logical replication via Debezium,
replication slots, initial snapshot, offset recovery or CDC deletes.

## A database change stream is not a domain event
CDC emits committed row inserts/updates/deletes, including internal
representation; business consumers may need a separate curated
domain event. Downstream must not expose sensitive source columns
without authorization, masking, retention and schema review.

## Snapshot-to-stream transition
Debezium PostgreSQL normally takes an initial consistent snapshot
when offsets absent and then streams WAL changes from snapshot
position. Snapshot modes have different behavior; no_data without
complete retained history may omit old rows. Connector tracks LSN
offset and relies on Postgres replication slot publication.
Each independent connector requires managed slot/publication
configuration; default auto-publication behavior can demand
excessive permissions. Prefer dedicated least-privilege role
and DBA-managed publication.

## WAL retention is a production resource
Stalled connector/slot can retain WAL and exhaust database storage.
Monitor retained WAL bytes, slot status, connector lag, offsets,
snapshot progress and Kafka topic delivery; heartbeat may help
advance LSN in certain low-activity/high-activity databases.
Database failover/upgrade may invalidate/drop slots or create
history gaps requiring coordinated resnapshot. A backup alone
doesn't certify offset continuity.

## Sink semantics
Source row may update 3 times. CDC carries ordered changes within
documented source/partition scope, but consumers can replay after
crash. Use stable key+source position/version, upsert or delete
tombstone policy and idempotent sink. Snapshot events may be
read events with a different operation type than live updates.

## Test matrix
Insert during snapshot, connector crash before offset flush,
same source event twice, drop/recreate publication, WAL lost,
tombstone delete, schema column rename, primary-key update,
new tenant PII and consumer lag beyond retention.
Check Debezium **3.7 docs** against pinned deployed version.

Sources: https://debezium.io/documentation/reference/stable/connectors/postgresql.html ,
https://www.postgresql.org/docs/current/logicaldecoding.html .
