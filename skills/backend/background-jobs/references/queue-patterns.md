# Python task queues — choosing a worker architecture

**Read when:** deciding FastAPI BackgroundTasks versus broker, or selecting Celery/RQ/Dramatiq/cloud queues.

## Decision
| Path | Suitable | Unsuitable |
|---|---|---|
| Inline sync/async call | Short request-budgeted work | Long unpredictable inference |
| FastAPI BackgroundTasks | Best-effort small post-response tasks | Durable jobs; crash/redeploy loses work |
| RQ / Redis-backed worker | Straightforward Python jobs with Redis | Assuming exactly-once, high resilience with no Redis ops |
| Celery | Mature distributed task workflow, schedules/complex routing | Under-resourced projects unable to operate broker/workers |
| Dramatiq | Brokered actor tasks, simple API | Without validation of required feature/version |
| Cloud queues (SQS/PubSub/Service Bus) | Managed infra, at-least-once delivery, cloud IAM | Assuming portability or atomic DB+queue writes |

Don't store huge user documents/PII directly in queue payload. Store authorized blob pointer, schema_version, job_id, tenant reference and correlation ID; verify auth again at execution, expire payload/retention appropriately.

## Worker contract
Validate input version and immutable parameters, claim idempotency in durable DB, check cancellation/lease, perform controlled work and commit outcome before acknowledge/delete. Define statuses queued/running/succeeded/failed/cancelled and recovery after worker crash.

## Security/ops
Separate job runner role/credentials from HTTP service where possible. Cap queue capacity and per-tenant admission. Provide job status to UI rather than keeping an HTTP connection alive for minutes; enforce storage TTL for results.

References: https://docs.celeryq.dev/en/stable/ and https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html .
