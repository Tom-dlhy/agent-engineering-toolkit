---
name: aws-s3-storage
domain: cloud
version: "2.0.0"
description: >-
  Use when implementing or diagnosing Amazon S3 buckets, object APIs, presigned uploads/downloads, encryption, event notifications, multipart transfer or object lifecycle. Do not use for general database schemas or non-S3 object stores.
---

# aws-s3-storage

## Scope

Storage design, key naming, bucket policies, presigned URLs, uploads, read semantics, metadata, encryption, lifecycle and event-driven processing. Choose S3 for objects, not for transactional relational records.

## Decision procedure

1. Identify ownership and trust boundary: private per user/tenant, public static assets or machine-to-machine.
2. Design object keys independent of untrusted display names; select key namespacing, access controls and retention.
3. Choose upload strategy: server SDK for small/server-held uploads, presigned PUT/POST for direct browser uploads, multipart for large transfers.
4. Set size/type/checksum validation **server-side**, not just front-end validation.
5. Define encryption, visibility, CORS, lifecycle/versioning, overwrite/duplicate behavior and cleanup/reconciliation.
6. Test authorized and unauthorized access, expiration, object-not-found, stale credentials, cancel/retry and large transfer behavior.

## References — targeted activation

- [S3 object operations and safe presigning](references/object-api-and-uploads.md) — open for SDK code, PUT/GET, direct browser uploads, multipart and signed URLs.
- [S3 security, events and lifecycle](references/security-and-lifecycle.md) — open for bucket policies, encryption, event processing, lifecycle, compliance and backup/recovery.

## Integration

For IAM policies use `aws-iam-security`; for object events driving queue processing use `aws-sqs-messaging` and cross-service patterns. Do not load unrelated AWS skills automatically.

## Exit criteria

Object access scoped; keys are not trusted as tenant authorization; server validates actual content; signed capabilities are limited; event retries and cleanup specified; negatives tested and logs do not expose signed URLs.
