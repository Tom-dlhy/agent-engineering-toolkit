# Cross-service AWS application patterns

**Read when:** a workflow spans several AWS services or the user requests an end-to-end architecture.

## Example: authenticated upload → process

1. API authenticates user and checks resource-level permission (not just possession of a URL).
2. Allocate opaque object key scoped to tenant and upload request. Store expected media type, size, checksum and workflow state in durable metadata.
3. Sign a narrowly scoped S3 operation with a short expiry; treat the presigned URL as a secret bearer capability.
4. Confirm object existence/metadata server-side; treat client-supplied "upload complete" as untrusted.
5. Emit a durable job request to SQS **after** metadata is committed or use an outbox/repair reconciler. Never assume a database write and SQS send are atomic.
6. SQS consumer claims idempotency key, checks object permissions/content and processes. Write result and mark completed atomically where possible; delete queue message only after durable success.
7. Worker failure: visibility timeout retry; poison-message detection and DLQ after justified maximum receives; operator replay procedure.

## Failure table

| Failure window | Consequence | Required recovery |
|---|---|---|
| Client received presigned URL but never uploaded | Orphan upload request | TTL cleanup / expiry |
| Object stored but database commit failed | Orphan object | Lifecycle reconciliation |
| DB committed but message send failed | Job stalled | Outbox poller or reconciliation |
| Work succeeded but SQS delete failed | Duplicate delivery | Idempotent workflow state check |
| Two consumers race | Duplicate side effects | Atomic claim, unique job key or conditional update |

Do not claim exactly-once delivery across SQS + Lambda + database. A unique request ID without durable deduplication is not sufficient.

## Boundary rules

- IAM is per role/resource; permissions must not silently cross tenant boundaries.
- Independent services are isolated failure domains. Create explicit timeouts, SLIs and correlation IDs across API, S3, SQS and worker.
- Use event contracts with schema version, event type, id, occurrence time and correlation id; validate payload in consumer.
- Event payloads contain object identifiers, not secrets or large personal data.
- Apply DLQ retention/replay controls, encryption and least privilege.
- Prefer AWS-managed capabilities when complexity savings justify the operational tradeoffs; do not build a generic event bus prematurely.

## Rehearsal

Inject failed upload, malformed object, duplicate job, expired IAM credentials, throttled SQS, consumer crash before and after commit. Confirm status transitions, duplicate suppression, alarms, cleanup, replay, and user-visible status match expectations.

Official references: https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html and https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html .
