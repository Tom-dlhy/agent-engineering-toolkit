---
name: gcp-cloud-storage
domain: cloud
version: "0.1.0"
description: >-
  Use when reading, uploading and controlling Google Cloud Storage objects, signed URLs, bucket IAM and lifecycle. Do not use for S3 or Azure Blob implementation or analytical warehouse table design.
---

# Google Cloud Storage

## Decision and connection procedure
1. Identify GCP organization/project, resource ID, region, API enablement, runtime and whether this is a data-plane read/write or IAM/infra operation.
2. Authenticate using ADC and a per-workload identity; local developer ADC ≠ gcloud CLI login. Cloud Run/GKE service account with bucket-scoped IAM instead of JSON private key. V4 signed URLs have specific signing prerequisites; runtime credentials may not directly hold private key.
3. Apply **service-specific IAM** and, where relevant, database or application authorization. Readers `roles/storage.objectViewer` on bucket, writers `roles/storage.objectCreator` or constrained objectUser as needed; bucket metadata/admin roles separate. Use object generation preconditions to prevent lost updates.
4. Choose API/SDK client with explicit deadlines, replay/idempotency semantics, bounds and cleanup. Object generation/metageneration, bucket region, retention policies, customer-managed encryption, signed URL expiry, multipart/resumable upload, event notification and lifecycle. Avoid listing entire bucket for a single key.
5. Verify behavior in mocks/emulator then an explicitly authorized sandbox project; never create/delete resources or modify IAM without approval.

## Deep references only when needed
- [Identity, connection and API examples](references/connection-and-permissions.md) — **read when** connecting to Google Cloud Storage, IAM failures or SDK invocation.
- [Operational limits, security and recovery](references/operations-and-recovery.md) — **read when** deploying, scaling, securing or diagnosing this service.

## Boundaries
gcp-integration coordinates cross-service ADC and projects; data skills own DB/warehouse modeling; terraform-iac owns infrastructure apply.

## Exit
Project/region/identity and IAM actions verified, scoped connection, replay policy, negative tests, and unsupported live assumptions listed.
