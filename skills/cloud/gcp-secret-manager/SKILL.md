---
name: gcp-secret-manager
domain: cloud
version: "0.1.0"
description: >-
  Use when accessing GCP Secret Manager secret versions, workload IAM, rotation, payload integrity or secret injection. Do not use for AWS Secrets Manager or Azure Key Vault.
---

# Google Secret Manager

## Decision and connection procedure
1. Identify GCP organization/project, resource ID, region, API enablement, runtime and whether this is a data-plane read/write or IAM/infra operation.
2. Authenticate using ADC and a per-workload identity; local developer ADC ≠ gcloud CLI login. Attach runtime service account and grant secret-specific accessor. Avoid downloading static JSON keys; use secret volume/env injection or SDK retrieval per rotation needs.
3. Apply **service-specific IAM** and, where relevant, database or application authorization. `roles/secretmanager.secretAccessor` on chosen secret; secret creation/rotation roles separate. API enablement and project/service account selection must be verified.
4. Choose API/SDK client with explicit deadlines, replay/idempotency semantics, bounds and cleanup. `latest` may rotate between calls, handle explicitly pinned versions for reproducibility when necessary. Verify CRC32C as official sample shows, cache TTL/refresh, forbidden vs nonexistent secrets, secret version disabled/destroyed and retention.
5. Verify behavior in mocks/emulator then an explicitly authorized sandbox project; never create/delete resources or modify IAM without approval.

## Deep references only when needed
- [Identity, connection and API examples](references/connection-and-permissions.md) — **read when** connecting to Google Secret Manager, IAM failures or SDK invocation.
- [Operational limits, security and recovery](references/operations-and-recovery.md) — **read when** deploying, scaling, securing or diagnosing this service.

## Boundaries
gcp-integration coordinates cross-service ADC and projects; data skills own DB/warehouse modeling; terraform-iac owns infrastructure apply.

## Exit
Project/region/identity and IAM actions verified, scoped connection, replay policy, negative tests, and unsupported live assumptions listed.
