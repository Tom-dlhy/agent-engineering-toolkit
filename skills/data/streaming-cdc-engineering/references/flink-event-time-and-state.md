# Flink event-time processing, watermarks and lateness

**Read when:** computing windows/aggregates from unordered streams,
with out-of-order events, event time and stateful operators.

## Event time is distinct from processing time
Event time is timestamp business event occurred; processing time
is when the system observed event. Network delays and backfills
can reorder records. Watermarks indicate *stream event-time
progress*, letting windows emit results after a threshold.
A too-aggressive watermark causes valid late events to be
considered late; too-conservative may delay result and
inflate state/latency.

## Window and lateness contract
Choose tumbling/sliding/session windows by business definition,
partition key and allowed lateness. Decide what happens after
watermark: late side output, update/retraction or backfill.
For accurate revenue, silent late-event drops may be unacceptable.
State TTL is a business correctness decision: short TTL can lose
dedupe/history; unbounded TTL may exhaust state backend.

## API compatibility caution
Flink **DataStream API V2** watermark documentation explicitly
labels the new API experimental and not fully production-ready
at source review time. Pin actual Flink release and select
supported API and connector versions; don't copy experimental
Watermark objects into older stable DataStream jobs.

## Backpressure/operations
Monitor busy/backpressured/idle operators, watermark lag,
checkpoint age, state size, key skew and sink latency.
A hot partition key can bottleneck entire job. Repartitioning
alters ordering guarantees and state rescaling cost.
Try representative skewed synthetic traffic before rollout.

## Tests
In-order vs out-of-order same set, event late inside/outside
allowed window, no events on one partition, idle source,
duplicate message, clock skew, watermark progression,
state expiry, failover and restored window totals.

Sources: https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/ ,
https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream-v2/watermark/ .
