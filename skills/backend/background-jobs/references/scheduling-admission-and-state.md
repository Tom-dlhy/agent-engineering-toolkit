# Durable job contract, scheduling and backpressure

**Read when:** adding long-lived Python inference, cron,
tenanted workers, progress tracking or overload controls.

## Job payload is a stable API
Define job_id, idempotency_key, tenant identity reference,
operation/schema_version, secure blob pointer, requested_at,
deadline, max retries, cancellation policy and retention.
Don't serialize arbitrary Pydantic/ORM Python objects or
embed large private documents into broker payloads.

## Request status state machine

~~~text
QUEUED → RUNNING → SUCCEEDED
   |        |   \
   v        v    v
CANCELLED FAILED RETRY_QUEUED
~~~

State transitions must be recorded durably; worker restart
must distinguish lease expired from actively running.
Expose authenticated status endpoint and replay strategy,
not infinite HTTP request waiting.

## Admission and capacities

Little's law can estimate mean work-in-flight under stable
arrival/processing conditions, but p99 and bursts demand
empirical headroom. Provider model token-per-minute and
request-per-minute quotas, DB connections and memory may
bottleneck far before CPU; more replicas can accelerate
rate-limit exhaustion. Use per-tenant budgets and bounded
queues/worker concurrency with fair scheduling.

## Cron/delay
Use explicit timezone, DST/skipped occurrence policy,
single active scheduler leadership or durable deduplication,
catch-up vs skip after outage and periodic renewal.
A cron expression is not a uniqueness guarantee.

## Failure tests
Duplicate schedule firing, expired lease, worker killed after
remote model commit, canceled job resuming, poison schema
version, queue overflow and privileged status access from
another tenant. Test DLQ replay under approved synthetic data.

Sources: https://docs.celeryq.dev/en/stable/userguide/tasks.html ,
https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html and
https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html .
