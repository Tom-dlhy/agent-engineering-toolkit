# Celery ACK, retries and worker-loss semantics

**Read when:** configuring Celery acks_late, autoretry,
broker delivery policy or guaranteeing repeatable job effects.

## Do not conflate three mechanisms
- ACK says the broker may remove/redeliver a message.
- Task.retry requests a subsequent execution according
  to policy; not identical to broker redelivery.
- acks_late changes acknowledgment timing. Celery
  may ACK task on certain child process termination
  even with late ACK; check task_reject_on_worker_lost
  and broker/worker pool semantics in pinned version.

Official Celery 5.6 task guide explicitly requires
**idempotent tasks** if acknowledging after execution and
documents worker-loss behavior exceptions.

~~~python
from celery import shared_task

@shared_task(bind=True, autoretry_for=(TimeoutError,),
             retry_backoff=True, retry_jitter=True,
             retry_kwargs={"max_retries": 4})
def fetch_partner_document(self, document_id: str):
    # Illustrative: in production validate permissions, tenant,
    # bounded provider timeout and durable job effects.
    return fetch_with_deadline(document_id)
~~~

The fetch_with_deadline function is project-specific, not a complete
runnable production job. Automatic retry class selection must
match actual SDK transient error taxonomy. Avoid retry on
invalid data, forbidden auth and unpredictable external
effect without stable provider idempotency.

## Failure windows
Worker dies before effect, after effect before durable
checkpoint, broker redelivers after ACK lost, poison
payload, prefetch monopolizes fair scheduling and queue
visibility/lease expires mid-task. Verify process pool
and broker version behavior in a disposable integration
environment rather than inferring exactly-once.

## Policy
Set task time/soft time limits, connect/read/deadline,
bounded attempts, jitter and operator-owned DLQ/replay.
Never rely on in-memory seen-ID set under multiple
replicas or restarted workers.

Sources: https://docs.celeryq.dev/en/stable/userguide/tasks.html and
https://docs.celeryq.dev/en/stable/userguide/configuration.html .
