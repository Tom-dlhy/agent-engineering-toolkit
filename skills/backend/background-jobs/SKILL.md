---
name: background-jobs
domain: backend
version: "2.0.0"
description: >-
  Use when designing Python durable background tasks, schedulers and queues (Celery, RQ, Dramatiq, cloud queues), including timeouts, idempotency, worker scale and DLQ. Do not use for a quick synchronous operation that fits its deadline.
---

# Python background jobs — durability boundaries

## Choose
1. If quick best-effort local noncritical task, framework background task may suffice with acknowledged loss on worker crash; otherwise choose durable external queue.
2. Define job ID, schema version, tenant, idempotency, max runtime, retry count, deadline, DLQ, cancellation and ownership.
3. Select worker/task system by broker deployment, ecosystem, scheduling, Python task needs and operational experience, not popularity.
4. Separate HTTP admission/status from worker concurrency and actual external side effects.
5. Measure queue age and retry storm behavior, ensure replay and poison handling, and test worker restart.

## Deep references
- [Queue selection and execution contract](references/queue-patterns.md) — read when picking Celery/RQ/Dramatiq/cloud queues or designing payloads and worker state.
- [Recovery, idempotency, scaling and operations](references/job-recovery-and-capacity.md) — read when dealing with duplicates, DLQ, scheduling and realistic load.

## Exit
At-least-once assumption explicit, durable state for important tasks, bounded retries, recovery plan, monitoring and tested failure windows.
