---
name: background-jobs
domain: backend
version: "0.1.0"
description: >-
  Use when designing background jobs, task queues, scheduled workers and long-running asynchronous processing. Do not use when a synchronous request completes reliably within its latency budget.
---

# background-jobs

## Contract
Define task payload, unique ID, idempotency key, maximum duration, retry count, dead-letter behavior and job status. Do not pass unbounded serialized ORM objects to workers.
## Reliability
At-least-once delivery should be the default assumption. Use durable state, exponential backoff with jitter, timeout/cancellation semantics and a dead-letter queue or manual review path. Isolate side effects behind idempotent operations.
## Operations
Track queued/running/completed/failed counts, queue age, stalled leases and repeated poison jobs. Separate worker concurrency from web-server processes.
## Verify
Test duplicate delivery, partial failure, cancellation, worker restart, clock/time-zone edge cases and replay.
