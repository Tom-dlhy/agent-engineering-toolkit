# Stream checkpoint recovery, exactly-once scope and sinks

**Read when:** designing checkpoint storage, sink commits,
state restoration, Kafka/Flink delivery or resumable replay.

## Precisely scope "exactly once"
Flink checkpointing can provide exactly-once state updates
only for cooperating replayable sources and supported
checkpointing semantics. End-to-end exactly-once delivery
also needs sink participating in checkpoint/transaction
mechanism. A random HTTP/third-party payment sink doesn't
become transactional merely because the Flink graph uses
exactly-once state. Connector capabilities are version-specific.

## Fault-tolerance design
Choose durable checkpoint location, interval, retention,
savepoints for upgrades, restart strategy and recovery
SLO. Understand snapshot barriers, source offsets, parallel
state repartition and sink transaction commits. Unaligned
checkpoints and alternative backends may change performance/
resource tradeoffs; don't enable based on hearsay.

## Sink type decisions
- Kafka transactions where connector/config support exactly-once
  for designated source→sink flow, version-matched.
- Relational sink: upsert with key/version, DB transaction and
  dedupe/reconciliation, not universal global ACID.
- Iceberg sink: atomic snapshot commit semantics depend on
  engine/catalog and concurrent writers.
- HTTP webhook/payment: need durable outbox/retry reconciliation
  and provider idempotency if external side effect matters.

## Crash injection
Snapshot prepared then worker killed, record processed but
not checkpointed, sink commit before checkpoint completion,
consumer replay after restored offset, key repartition on
scaling, poison schema, end-to-end sink unavailable.
Compare final state to independent source ledger, not just
reported "checkpoint completed". Unavailable sink can
induce backpressure and retention pressure upstream.

## Operational evidence
Record source/sink connector version, checkpoint mode,
storage durability, last completed checkpoint/savepoint,
recovery duration, duplicate/late counts and sink state
after replay. Never promise global exactly-once without
a witnessed end-to-end test and scoped guarantee.

Sources: https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/ ,
https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/guarantees/ .
