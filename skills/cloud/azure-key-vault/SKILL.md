---
name: azure-key-vault
domain: cloud
version: "0.1.0"
description: >-
  Use when reading, versioning and rotating secrets/certificates/keys using Azure Key Vault. Do not use for AWS Secrets Manager or GCP Secret Manager.
---

# Azure Key Vault — Azure-specific implementation

## Procedure
1. Inspect tenant, subscription, resource group, resource URI/FQDN, region, runtime and SDK version.
2. Use local Azure CLI identity only for development. In production attach and select a scoped Managed Identity; **do not rely on accidental developer credential fallbacks**.
3. `Key Vault Secrets User` (data-plane read) at vault or scoped resource where supported; `Key Vault Secrets Officer` needed to manage secrets; choose RBAC mode or legacy access policy per vault configuration, never assume both.
4. Build a resource-specific SDK/host adapter and bound retries/timeouts; separate data plane from ARM management, and preserve idempotency/unknown remote outcome semantics.
5. RBAC propagation, wrong vault tenant, disabled/soft-deleted secret, rotation cache stale, firewall/private endpoint blocked, leaked exception/debug logs and version alias confusion.
6. Test denied identity, wrong tenant, network firewall and duplicate/timeout before authorized integration; never create cloud/IAM resources without approval.

## Targeted references
- [Identity, SDK and data-plane permissions](references/connection-and-permissions.md) — **read when** configuring Azure Key Vault connectivity or 401/403.
- [Scale, operations and negative tests](references/operations-and-recovery.md) — **read when** diagnosing outages or preparing a release.

## Ownership
azure-integration owns shared Azure tenant/SDK coordination; terraform-iac owns infra plans, this skill owns Azure Key Vault semantics.

## Completion
Chosen credential, resource ID/region, minimum roles, working SDK contract and explicitly scoped sandbox evidence.
