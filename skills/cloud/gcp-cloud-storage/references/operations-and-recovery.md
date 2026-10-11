# Google Cloud Storage — operations and recovery verification

**Read when:** selecting production capacity, cost, rollback, monitoring or integration failure behavior.

## Service-specific engineering
Object generation/metageneration, bucket region, retention policies, customer-managed encryption, signed URL expiry, multipart/resumable upload, event notification and lifecycle. Avoid listing entire bucket for a single key.

## Identity and resilience constraints
Cloud Run/GKE service account with bucket-scoped IAM instead of JSON private key. V4 signed URLs have specific signing prerequisites; runtime credentials may not directly hold private key. Readers `roles/storage.objectViewer` on bucket, writers `roles/storage.objectCreator` or constrained objectUser as needed; bucket metadata/admin roles separate. Use object generation preconditions to prevent lost updates.

Measure p95/p99 latency, error/queue backlog, resource limits, regional availability, quota project and relevant billable units. A successful local SDK call is not proof of end-to-end authorization, service-to-service JWT identity or failover. For mutations, treat post-send network timeout as **unknown remote outcome** and reconcile before retry; use per-service preconditions/deduplication features where documented.

## Required negative and integration tests
1. Wrong project/region and revoked service-account grant cause deterministic denial.
2. Expired/incorrect identity and wrong resource produce safe error mapping, no credentials in logs.
3. Duplicate/reordered input, timeout after remote commit and cancellation preserve application invariant.
4. Provider regional quota/throttle and network fault trigger bounded retries or fail-closed result.
5. Production claim requires authorized sandbox check of actual IAM, configuration, SDK version and rollback procedure.

## Official docs
- https://docs.cloud.google.com/storage/docs/uploading-objects
- https://docs.cloud.google.com/storage/docs/request-preconditions
