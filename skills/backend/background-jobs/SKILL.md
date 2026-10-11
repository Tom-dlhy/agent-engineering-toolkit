---
name: background-jobs
domain: backend
version: "2.1.0"
description: >-
  Use when selecting and implementing durable Python background jobs, Celery,
  broker workers, schedulers and retry/recovery with operational guarantees.
  Do not turn a quick local noncritical post-response operation into a queue.
---

# Background jobs — choose loss semantics before queue library

## Method
1. Separate best-effort request-local work from **durable business job**.
   FastAPI BackgroundTasks executes in application process and isn't
   a durable broker: may be lost on crash/redeployment.
2. Decide broker, worker, persistence and schedule based on latency,
   replay, service availability, expected job duration and infra ownership.
3. Define job identity, tenant, authorization, input schema version,
   cancellation, deadline, deduplication, per-tenant caps and result retention.
4. Celery `acks_late` delays ACK, **does not call retry automatically**.
   Even with `acks_late`, process termination behavior varies;
   `task_reject_on_worker_lost` may alter redelivery. Confirm
   actual Celery and broker version before choosing.
5. Handle the side-effect-then-crash window with durable idempotency
   and reconciliation, never blanket exactly-once claims.
6. Configure bounded retry/backoff/Jitter, visibility/lease vs timeout,
   DLQ, worker drain, poison event handling, scheduling timezones and
   admission/backpressure for provider rate/TPM constraints.
7. Test job replay, cancellation, duplicate, worker kill, payload
   migrations, stuck lease, callback failure and startup/shutdown.

## References
- [Broker/task selection](references/queue-patterns.md) — read when choosing Celery/RQ/Dramatiq/cloud queues.
- [Recovery and capacity](references/job-recovery-and-capacity.md) — read when planning retries, DLQ and scaling.
- [Celery ACK/retry failure semantics](references/celery-delivery-and-worker-crashes.md) — read when configuring acks_late/retry.
- [Scheduling, backpressure and job contracts](references/scheduling-admission-and-state.md) — read when dealing with long jobs, throttling or recovery.

## Boundaries
event-driven-design owns distributed business event contracts,
python-persistence owns DB outbox/locking, release-readiness owns deployment.

## Exit
Durable state/authority boundaries, bounded capacity and timeout,
correct delivery assumptions, observed recovery and negative tests.
