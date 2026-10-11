---
name: azure-functions-runtime
domain: cloud
version: "0.1.0"
description: >-
  Use when building Azure Functions Python triggers/bindings, identity-based connections, timers, queues and deployment. Do not use for Azure Container Apps generic HTTP apps or AWS Lambda-specific mechanics.
---

# Azure Functions (Python v2) — Azure-specific implementation

## Procedure
1. Inspect tenant, subscription, resource group, resource URI/FQDN, region, runtime and SDK version.
2. Use local Azure CLI identity only for development. In production attach and select a scoped Managed Identity; **do not rely on accidental developer credential fallbacks**.
3. Runtime system-assigned MI with scoped storage/queue/etc roles; function host storage has separate permissions. Deployment principal needs publish/manage rights, not shared with function runtime.
4. Build a resource-specific SDK/host adapter and bound retries/timeouts; separate data plane from ARM management, and preserve idempotency/unknown remote outcome semantics.
5. Python v1 function.json vs v2 decorator confusion, bindings extension version, event retry/poison queue, host.json scaling, function keys mistaken for user auth, `AzureWebJobsStorage` misconfigured, worker timeout.
6. Test denied identity, wrong tenant, network firewall and duplicate/timeout before authorized integration; never create cloud/IAM resources without approval.

## Targeted references
- [Identity, SDK and data-plane permissions](references/connection-and-permissions.md) — **read when** configuring Azure Functions (Python v2) connectivity or 401/403.
- [Scale, operations and negative tests](references/operations-and-recovery.md) — **read when** diagnosing outages or preparing a release.

## Ownership
azure-integration owns shared Azure tenant/SDK coordination; terraform-iac owns infra plans, this skill owns Azure Functions (Python v2) semantics.

## Completion
Chosen credential, resource ID/region, minimum roles, working SDK contract and explicitly scoped sandbox evidence.
