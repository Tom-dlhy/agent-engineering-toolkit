# Worker retry, scheduling and operational recovery

**Read when:** designing retries/DLQ/replay, increasing worker parallelism or diagnosing stuck tasks.

## At-least-once failure windows
| Crash window | Recovery |
|---|---|
| Before durable job claim | Redeliver |
| After claim before side effect | Lease timeout / reclaim |
| After external side effect before commit | Provider idempotency key or reconciliation |
| After DB commit before ACK | Consumer dedupe and ACK after verification |
| Poison payload | Bounded retries, DLQ quarantine, operator decision |
| Deployment while running | Graceful drain, visibility/lease extension, replay |

Retries must discriminate transient provider 429/network fault from invalid data/permanent authorization failure; jitter and capped attempts avoid avalanches. Max job timeout and broker visibility must be coordinated with external operation.

## Sizing worker pools
Workload rate × average duration determines average concurrency in stable conditions; p99 and burst require headroom. Capacity is ultimately bounded by DB, provider RPM/TPM, sockets and memory. Add replicas only after backpressure/concurrency limits and use lag oldest-age dashboards to show backlog health. Use rate-limited scheduling and per-tenant fairness for untrusted clients.

## Temporal/cron
Time zones, daylight-saving transitions, duplicate scheduler leaders and missed runs must be explicit. Cron trigger is not proof that exactly one job executed. Document replay window and operator ownership.

## Tests
Simulate worker kill before/after commit, duplicate event, interrupted model call, DLQ redrive, stale lease, clock shift and encrypted payload expired. Verify no duplicated irreversible writes.

References: https://docs.celeryq.dev/en/stable/ and https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html .
