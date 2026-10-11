# Lakeflow Jobs — alerting, retries, backfill and publication readiness

Read when: setting production job dependencies, restarting Lakeflow, assessing freshness, or recovering CDC/Auto Loader state.

## Orchestrator != source truth
A green job run says code completed, not that source was current or target metrics reconcile. Assign source SLO, event-to-publish SLI, exceptions, owner and rollback. Use Jobs task graphs/retries for durable orchestration; avoid non-idempotent external actions inside retried tasks.

## Recovery decision tree
1. Identify latest **accepted source event**, discovery/read watermark, last committed sink version and actual query/table version.
2. Determine failed layer: notification/permissions, schema inference, stream checkpoint, CDC sequence, expectation failure, target compute or downstream consumer.
3. If schema evolution stopped Auto Loader, confirm contract and permitted restart; don't reset checkpoint to bypass a strict fail.
4. If checkpoint expired/incompatible, determine authoritative replay source and snapshot boundary; new checkpoint can re-ingest historical files, requiring explicit dedupe and cutover.
5. If historical correction/backfill, define half-open window, stable source sequence, overlap policy with live stream, estimate compute and source retention.
6. Verify record-level and metric-level reconciliation before publishing and restart alerts.

## Operational template
~~~text
PIPELINE / OWNER / TARGET / CLOUD / RUNTIME:
SOURCE: immutable manifest, version, expected heartbeat and CDC sequence
STATE: checkpoint, current table version and reader retention
BACKFILL: window, source snapshot, rows/bytes, compute/DBU cap
LIVE TRAFFIC: isolation/snapshot/merge conflict resolution
QUALITY: unique keys, deletes, SCD history, critical metric totals
OBSERVABILITY: event log, pipeline progress, job history and alert channel
ROLLBACK: previous version/pointer + consumer impact + authorized operator
~~~

## Failure tests
- Upstream outage but jobs succeed with zero changes -> freshness alert (not “all green”).
- Schema new column -> controlled restart/quarantine without silent data loss.
- Duplicate business events across cloud files -> deterministic target, not double count.
- Concurrent replay/live CDC -> latest source version wins with tested SCD2 intervals.
- Job retry after side effect -> idempotency token prevents repeated external action.
- Permission loss to UC external location -> no silent success or privilege escalation.

Never run full refresh, delete checkpoints, alter production streams or change job identity without approval. A backfill is a production data change, not simply an innocent diagnostic.

Sources: https://docs.databricks.com/aws/en/ldp/concepts/how-to-use-pipelines and https://docs.databricks.com/aws/en/ldp/best-practices and https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/best-practices
