# Lineage, privacy and operation of data pipelines

**Read when:** incidents affect freshness/data quality, datasets
need provenance, or retention includes replicated data.

## Capture replayable provenance
Record run ID, source version/snapshot, code SHA, schema revision,
input partitions and key counts, validation gate results,
published output version and downstream affected consumers.
OpenLineage supports interoperable lineage events; a producer
integration doesn't guarantee complete semantic or column lineage.

## Distinct operational SLOs
Availability means consumers can read a validated snapshot.
Freshness is event/source arrival to validated publication,
not just DAG success. Completeness is expected partitions/
keys; correctness is reconciled business values. A "green"
DAG that reuses yesterday's input may violate SLO.

## Sensitive data lifecycle
Classify PII before ingest, set legitimate purposes and
access roles, enforce masking, deletion/retention for raw
staging, mart, logs, backups, CDC, temporary exports and
third-party copies. Soft delete alone is not necessarily
data erasure, and removing identifiers doesn't automatically
make data anonymous.

## Incident runbook
Identify impacted source snapshot/commit and consumers;
stop unsafe publication, preserve last good version;
backfill with bounded replay and reconciliation; verify
freshness/quality gates; notify owners and document
eventual downstream repair. Avoid destructive historic
rewrite without approval and recovery evidence.

## Negative scenarios
Partial publication, source updated but extraction stalled,
privacy leak through invalid-row logs, stale lineage,
source downtime, bad schema revision, failed replay,
retention request with still-existing backup/export.
Track resolution and any irrecoverable historical gap.

Sources: https://openlineage.io/docs/ ,
https://docs.getdbt.com/docs/deploy/source-freshness ,
https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html .
