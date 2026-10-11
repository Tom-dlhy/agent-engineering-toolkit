# Google Secret Manager — operations and recovery verification

**Read when:** selecting production capacity, cost, rollback, monitoring or integration failure behavior.

## Service-specific engineering
`latest` may rotate between calls, handle explicitly pinned versions for reproducibility when necessary. Verify CRC32C as official sample shows, cache TTL/refresh, forbidden vs nonexistent secrets, secret version disabled/destroyed and retention.

## Identity and resilience constraints
Attach runtime service account and grant secret-specific accessor. Avoid downloading static JSON keys; use secret volume/env injection or SDK retrieval per rotation needs. `roles/secretmanager.secretAccessor` on chosen secret; secret creation/rotation roles separate. API enablement and project/service account selection must be verified.

Measure p95/p99 latency, error/queue backlog, resource limits, regional availability, quota project and relevant billable units. A successful local SDK call is not proof of end-to-end authorization, service-to-service JWT identity or failover. For mutations, treat post-send network timeout as **unknown remote outcome** and reconcile before retry; use per-service preconditions/deduplication features where documented.

## Required negative and integration tests
1. Wrong project/region and revoked service-account grant cause deterministic denial.
2. Expired/incorrect identity and wrong resource produce safe error mapping, no credentials in logs.
3. Duplicate/reordered input, timeout after remote commit and cancellation preserve application invariant.
4. Provider regional quota/throttle and network fault trigger bounded retries or fail-closed result.
5. Production claim requires authorized sandbox check of actual IAM, configuration, SDK version and rollback procedure.

## Official docs
- https://docs.cloud.google.com/secret-manager/docs/access-secret-version
- https://docs.cloud.google.com/secret-manager/docs/best-practices
