---
name: azure-container-apps
domain: cloud
version: "0.1.0"
description: >-
  Use when deploying containers to Azure Container Apps, revisions, KEDA scaling, ingress or managed identity. Do not use for Azure Functions programming model, Kubernetes clusters or AWS ECS.
---

# Azure Container Apps — Azure-specific implementation

## Procedure
1. Inspect tenant, subscription, resource group, resource URI/FQDN, region, runtime and SDK version.
2. Use local Azure CLI identity only for development. In production attach and select a scoped Managed Identity; **do not rely on accidental developer credential fallbacks**.
3. Deployer requires approved Container Apps/resource group scope; runtime MI receives narrow Key Vault/Blob/Service Bus data roles. Container registry pull requires correct AcrPull/identity; secrets references and ingress policy separate.
4. Build a resource-specific SDK/host adapter and bound retries/timeouts; separate data plane from ARM management, and preserve idempotency/unknown remote outcome semantics.
5. Ingress public by accident, image pull denied, secret not available to revision, revision traffic split, minReplicas=0 scaling to zero with ingress disabled, KEDA poll and cooldown misunderstood, egress/private endpoints.
6. Test denied identity, wrong tenant, network firewall and duplicate/timeout before authorized integration; never create cloud/IAM resources without approval.

## Targeted references
- [Identity, SDK and data-plane permissions](references/connection-and-permissions.md) — **read when** configuring Azure Container Apps connectivity or 401/403.
- [Scale, operations and negative tests](references/operations-and-recovery.md) — **read when** diagnosing outages or preparing a release.

## Ownership
azure-integration owns shared Azure tenant/SDK coordination; terraform-iac owns infra plans, this skill owns Azure Container Apps semantics.

## Completion
Chosen credential, resource ID/region, minimum roles, working SDK contract and explicitly scoped sandbox evidence.
