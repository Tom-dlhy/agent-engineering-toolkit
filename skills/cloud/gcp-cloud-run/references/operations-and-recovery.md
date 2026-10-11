# Google Cloud Run — operations and recovery verification

**Read when:** selecting production capacity, cost, rollback, monitoring or integration failure behavior.

## Service-specific engineering
Cloud Run public vs authenticated IAM gate; startup probe, concurrency per instance, max/min instances, outbound VPC path, request timeout, cold start, revision traffic split and shutdown/DB connection amplification. ID-token audience for custom path must remain service URL.

## Identity and resilience constraints
Attach service identity to caller workload; pass Google-signed OIDC ID token with audience target SERVICE_URL, not arbitrary API OAuth access token. Caller service account needs `roles/run.invoker` scoped to target service. Deployment principal requires separate create/update/Artifact Registry/IAM grants; runtime service account owns access to downstream services.

Measure p95/p99 latency, error/queue backlog, resource limits, regional availability, quota project and relevant billable units. A successful local SDK call is not proof of end-to-end authorization, service-to-service JWT identity or failover. For mutations, treat post-send network timeout as **unknown remote outcome** and reconcile before retry; use per-service preconditions/deduplication features where documented.

## Required negative and integration tests
1. Wrong project/region and revoked service-account grant cause deterministic denial.
2. Expired/incorrect identity and wrong resource produce safe error mapping, no credentials in logs.
3. Duplicate/reordered input, timeout after remote commit and cancellation preserve application invariant.
4. Provider regional quota/throttle and network fault trigger bounded retries or fail-closed result.
5. Production claim requires authorized sandbox check of actual IAM, configuration, SDK version and rollback procedure.

## Official docs
- https://docs.cloud.google.com/run/docs/authenticating/service-to-service
- https://docs.cloud.google.com/run/docs/configuring/concurrency
