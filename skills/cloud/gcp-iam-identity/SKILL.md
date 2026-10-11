---
name: gcp-iam-identity
domain: cloud
version: "0.1.0"
description: >-
  Use when setting up Google Cloud authentication, ADC, service accounts, workload identity federation or cross-project permissions. Do not use for AWS IAM, Azure managed identities or project business authorization.
---

# Google Cloud IAM and Application Default Credentials

## Decision and connection procedure
1. Identify GCP organization/project, resource ID, region, API enablement, runtime and whether this is a data-plane read/write or IAM/infra operation.
2. Authenticate using ADC and a per-workload identity; local developer ADC ≠ gcloud CLI login. Attach per-workload service account to Cloud Run/GKE/compute or use Workload Identity Federation for external CI; avoid downloadable JSON private keys. Federated direct resource access or service-account impersonation depends on API.
3. Apply **service-specific IAM** and, where relevant, database or application authorization. Least privileged predefined/custom role at project/bucket/service/secret scope. External federation requires trusted issuer, audience, attribute conditions and workload identity pool binding; service-account impersonation needs proper Token Creator policy.
4. Choose API/SDK client with explicit deadlines, replay/idempotency semantics, bounds and cleanup. 401/no ADC vs 403 insufficient IAM/API disabled vs wrong project; distinguish OAuth access token for APIs from OIDC ID token for invoking private Cloud Run. Verify separate local impersonation and runtime identity.
5. Verify behavior in mocks/emulator then an explicitly authorized sandbox project; never create/delete resources or modify IAM without approval.

## Deep references only when needed
- [Identity, connection and API examples](references/connection-and-permissions.md) — **read when** connecting to Google Cloud IAM and Application Default Credentials, IAM failures or SDK invocation.
- [Operational limits, security and recovery](references/operations-and-recovery.md) — **read when** deploying, scaling, securing or diagnosing this service.

## Boundaries
gcp-integration coordinates cross-service ADC and projects; data skills own DB/warehouse modeling; terraform-iac owns infrastructure apply.

## Exit
Project/region/identity and IAM actions verified, scoped connection, replay policy, negative tests, and unsupported live assumptions listed.
