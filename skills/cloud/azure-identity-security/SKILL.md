---
name: azure-identity-security
domain: cloud
version: "0.1.0"
description: >-
  Use when configuring Microsoft Entra workload identity, managed identity, local Azure credential chains or resource-specific Azure RBAC. Do not use for AWS IAM, GCP ADC and application business permissions.
---

# Azure Identity, Entra and RBAC — Azure-specific implementation

## Procedure
1. Inspect tenant, subscription, resource group, resource URI/FQDN, region, runtime and SDK version.
2. Use local Azure CLI identity only for development. In production attach and select a scoped Managed Identity; **do not rely on accidental developer credential fallbacks**.
3. Data plane vs ARM management roles differ. Azure RBAC assignment can propagate with delay. `AZURE_TOKEN_CREDENTIALS=prod` (azure-identity >=1.23) narrows DefaultAzureCredential chain; explicit ManagedIdentityCredential reduces ambiguity further.
4. Build a resource-specific SDK/host adapter and bound retries/timeouts; separate data plane from ARM management, and preserve idempotency/unknown remote outcome semantics.
5. Wrong tenant/subscription, unrelated developer credential chosen by DefaultAzureCredential, missing Managed Identity assignment, wrong token audience, resource firewall/private endpoint or eventual RBAC propagation.
6. Test denied identity, wrong tenant, network firewall and duplicate/timeout before authorized integration; never create cloud/IAM resources without approval.

## Targeted references
- [Identity, SDK and data-plane permissions](references/connection-and-permissions.md) — **read when** configuring Azure Identity, Entra and RBAC connectivity or 401/403.
- [Scale, operations and negative tests](references/operations-and-recovery.md) — **read when** diagnosing outages or preparing a release.

## Ownership
azure-integration owns shared Azure tenant/SDK coordination; terraform-iac owns infra plans, this skill owns Azure Identity, Entra and RBAC semantics.

## Completion
Chosen credential, resource ID/region, minimum roles, working SDK contract and explicitly scoped sandbox evidence.
