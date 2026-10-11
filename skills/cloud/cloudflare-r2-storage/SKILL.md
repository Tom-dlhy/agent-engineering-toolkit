---
name: cloudflare-r2-storage
domain: cloud
version: "0.1.0"
description: >-
  Use when integrating Cloudflare R2 object bucket bindings, uploads, downloads, presigned S3 API, private/public access and lifecycle. Do not use for AWS S3 IAM buckets or D1 SQL transactions.
---

# Cloudflare R2 object storage

## Implementation method
1. Confirm account/zone, deployment runtime, preview/production environment, resource binding and approved operations.
2. Inside Worker use `env.BUCKET` R2 binding; outside Worker use scoped R2 S3-compatible API token and account endpoint, not ordinary Cloudflare dashboard token.
3. R2 bucket binding rights derive from Worker deploy configuration; S3 API tokens are separately bucket-scoped. Bucket private by default; r2.dev public URL intended for development, not production custom-domain security control.
4. Use HTTP conditional headers, ETag/version management, size/multipart upload, object lifecycle/cost, retention, key validation and explicit public access gates. Worker binding API ≠ full AWS S3 API, SDK compatibility varies.
5. Test against local Wrangler and authorized preview plus production release plan; no deploying, DNS or permission changes without approval.

## Selective reference leaves
- [Bindings, credentials, code](references/connection-and-permissions.md) — **read when** wiring Cloudflare R2 object storage, API tokens and access scopes.
- [Operations and security QA](references/operations-and-recovery.md) — **read when** hardening data access, diagnosing, scaling or releasing.

## Boundary
cloudflare-platform routes cross-service concerns; frontend skills own UI; terraform-iac owns approved IaC. This skill owns Cloudflare R2 object storage API and runtime guarantees.

## Done
Binding/configuration and account identified, scoped access and no secrets in client bundles, negative tests, current limitations and safe rollout documented.
