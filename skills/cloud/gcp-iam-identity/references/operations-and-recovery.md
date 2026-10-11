# Google Cloud IAM and Application Default Credentials — operations and recovery verification

**Read when:** selecting production capacity, cost, rollback, monitoring or integration failure behavior.

## Service-specific engineering
401/no ADC vs 403 insufficient IAM/API disabled vs wrong project; distinguish OAuth access token for APIs from OIDC ID token for invoking private Cloud Run. Verify separate local impersonation and runtime identity.

## Identity and resilience constraints
Attach per-workload service account to Cloud Run/GKE/compute or use Workload Identity Federation for external CI; avoid downloadable JSON private keys. Federated direct resource access or service-account impersonation depends on API. Least privileged predefined/custom role at project/bucket/service/secret scope. External federation requires trusted issuer, audience, attribute conditions and workload identity pool binding; service-account impersonation needs proper Token Creator policy.

Measure p95/p99 latency, error/queue backlog, resource limits, regional availability, quota project and relevant billable units. A successful local SDK call is not proof of end-to-end authorization, service-to-service JWT identity or failover. For mutations, treat post-send network timeout as **unknown remote outcome** and reconcile before retry; use per-service preconditions/deduplication features where documented.

## Required negative and integration tests
1. Wrong project/region and revoked service-account grant cause deterministic denial.
2. Expired/incorrect identity and wrong resource produce safe error mapping, no credentials in logs.
3. Duplicate/reordered input, timeout after remote commit and cancellation preserve application invariant.
4. Provider regional quota/throttle and network fault trigger bounded retries or fail-closed result.
5. Production claim requires authorized sandbox check of actual IAM, configuration, SDK version and rollback procedure.

## Official docs
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
- https://docs.cloud.google.com/iam/docs/workload-identity-federation
