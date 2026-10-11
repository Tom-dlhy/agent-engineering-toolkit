# S3 security, events, retention and operations

**Read when:** securing buckets, configuring lifecycle/versioning or triggering background workflows from S3.

## Access control

- Default to **private bucket and Block Public Access** at account/bucket scope, unless public distribution is deliberate and reviewed.
- Prefer IAM role permissions with appropriate resource ARNs (`bucket` for ListBucket, `bucket/key` for object operations).
- Use bucket policy conditions for specific networks/endpoints, encryption expectations and signed-request constraints only when supported by the operation.
- For SSE-KMS, assess both the IAM permission and KMS key policy; S3 permission alone may not be enough.
- Never rely on a confidential-looking S3 key as authentication, or bypass per-tenant checks when generating signed URLs.

## Retention, versioning, deletion

| Need | Mechanism | Caveat |
|---|---|---|
| Recover overwritten objects | Bucket versioning | Delete markers and noncurrent versions continue to affect cost |
| Temporary uploads | Lifecycle expiration | Asynchronous expiry; do not promise immediate cleanup |
| Abandoned multipart transfers | AbortIncompleteMultipartUpload lifecycle rule | Recover explicit API abort for user-cancel path |
| Regulatory retention | Object Lock + governance/compliance modes where supported | Requires deliberate legal/operational design; test deletion expectations |
| Cross-region recovery | Replication where justified | Additional permissions/costs and non-instant behavior |

Define RPO/RTO and restore tests; versioning alone is not a complete backup strategy.

## S3 event to SQS pattern

S3 notifications are asynchronous and can be duplicated or arrive out of order. Consumers must use idempotency keyed to durable object identity/version/event, and validate current object state. Do not assume exactly-once event delivery or perfect ordering. Avoid processing objects while they are still marked unverified in the application.

- If an object upload event should drive an SQS consumer, ensure event notification configuration, queue policy allowing the service principal under constrained source account/ARN and the worker's read permissions.
- Use a metadata DB or outbox when business transaction completion and event production must be coupled reliably.
- Alert on event backlog, DLQ, missing object, checksum failure and abandoned uploads.

## Security and cost checklist

Audit public grants/access points, lifecycle rules, encryption/KMS key rotation requirements, bucket access logging/data events per workload, request counts, large object egress and transfer patterns. Avoid logging presigned query strings and confidential object keys.

## Negative testing

Attempt cross-tenant access, GET without grant, public ACL/bucket policy leakage, broken SSE-KMS policy, canceled multipart upload, duplicate notification and deletion of a retained object.

Official: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html and https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html .
