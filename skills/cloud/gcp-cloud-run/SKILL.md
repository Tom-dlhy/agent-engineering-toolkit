---
name: gcp-cloud-run
domain: cloud
version: "0.1.0"
description: >-
  Use when deploying and invoking authenticated Cloud Run HTTP services or Jobs, controlling concurrency, revisions, scaling and network egress. Do not use for Cloud Functions triggers without Cloud Run or Azure Container Apps.
---

# Google Cloud Run

## Decision and connection procedure
1. Identify GCP organization/project, resource ID, region, API enablement, runtime and whether this is a data-plane read/write or IAM/infra operation.
2. Authenticate using ADC and a per-workload identity; local developer ADC ≠ gcloud CLI login. Attach service identity to caller workload; pass Google-signed OIDC ID token with audience target SERVICE_URL, not arbitrary API OAuth access token.
3. Apply **service-specific IAM** and, where relevant, database or application authorization. Caller service account needs `roles/run.invoker` scoped to target service. Deployment principal requires separate create/update/Artifact Registry/IAM grants; runtime service account owns access to downstream services.
4. Choose API/SDK client with explicit deadlines, replay/idempotency semantics, bounds and cleanup. Cloud Run public vs authenticated IAM gate; startup probe, concurrency per instance, max/min instances, outbound VPC path, request timeout, cold start, revision traffic split and shutdown/DB connection amplification. ID-token audience for custom path must remain service URL.
5. Verify behavior in mocks/emulator then an explicitly authorized sandbox project; never create/delete resources or modify IAM without approval.

## Deep references only when needed
- [Identity, connection and API examples](references/connection-and-permissions.md) — **read when** connecting to Google Cloud Run, IAM failures or SDK invocation.
- [Operational limits, security and recovery](references/operations-and-recovery.md) — **read when** deploying, scaling, securing or diagnosing this service.

## Boundaries
gcp-integration coordinates cross-service ADC and projects; data skills own DB/warehouse modeling; terraform-iac owns infrastructure apply.

## Exit
Project/region/identity and IAM actions verified, scoped connection, replay policy, negative tests, and unsupported live assumptions listed.
