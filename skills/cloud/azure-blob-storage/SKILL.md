---
name: azure-blob-storage
domain: cloud
version: "0.1.0"
description: >-
  Use when implementing Azure Blob uploads, downloads, SAS, RBAC, lifecycle and private containers. Do not use for Amazon S3, Google Cloud Storage or database transaction design.
---

# Azure Blob Storage — Azure-specific implementation

## Procedure
1. Inspect tenant, subscription, resource group, resource URI/FQDN, region, runtime and SDK version.
2. Use local Azure CLI identity only for development. In production attach and select a scoped Managed Identity; **do not rely on accidental developer credential fallbacks**.
3. Reader: Storage Blob Data Reader; writer: Storage Blob Data Contributor scoped container/account as supported. SAS signing/service permissions differ; avoid account shared keys, grant user delegation key only where needed.
4. Build a resource-specific SDK/host adapter and bound retries/timeouts; separate data plane from ARM management, and preserve idempotency/unknown remote outcome semantics.
5. Storage firewall/private endpoint, wrong cloud endpoint, 403 role assignment delay, overwrite race without ETag, SAS leakage/expiry, multipart/large blob cost, lifecycle and public access settings.
6. Test denied identity, wrong tenant, network firewall and duplicate/timeout before authorized integration; never create cloud/IAM resources without approval.

## Targeted references
- [Identity, SDK and data-plane permissions](references/connection-and-permissions.md) — **read when** configuring Azure Blob Storage connectivity or 401/403.
- [Scale, operations and negative tests](references/operations-and-recovery.md) — **read when** diagnosing outages or preparing a release.

## Ownership
azure-integration owns shared Azure tenant/SDK coordination; terraform-iac owns infra plans, this skill owns Azure Blob Storage semantics.

## Completion
Chosen credential, resource ID/region, minimum roles, working SDK contract and explicitly scoped sandbox evidence.
