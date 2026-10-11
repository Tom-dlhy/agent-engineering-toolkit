---
name: azure-service-bus
domain: cloud
version: "0.1.0"
description: >-
  Use when sending or settling messages in Azure Service Bus queues/topics with locks, sessions, DLQs and retries. Do not use for GCP Pub/Sub, AWS SQS or generic business event schema design.
---

# Azure Service Bus — Azure-specific implementation

## Procedure
1. Inspect tenant, subscription, resource group, resource URI/FQDN, region, runtime and SDK version.
2. Use local Azure CLI identity only for development. In production attach and select a scoped Managed Identity; **do not rely on accidental developer credential fallbacks**.
3. `Azure Service Bus Data Sender` for send and `Azure Service Bus Data Receiver` for settlement/receive; manage entities with separate control-plane role. Sessions, queues and topic subscriptions require corresponding permissions.
4. Build a resource-specific SDK/host adapter and bound retries/timeouts; separate data plane from ARM management, and preserve idempotency/unknown remote outcome semantics.
5. Message lock expires before processing, duplicate delivery after settlement failure, max delivery count/DLQ, session ordering, auth role pending, connection namespace `*.servicebus.windows.net` and network policy.
6. Test denied identity, wrong tenant, network firewall and duplicate/timeout before authorized integration; never create cloud/IAM resources without approval.

## Targeted references
- [Identity, SDK and data-plane permissions](references/connection-and-permissions.md) — **read when** configuring Azure Service Bus connectivity or 401/403.
- [Scale, operations and negative tests](references/operations-and-recovery.md) — **read when** diagnosing outages or preparing a release.

## Ownership
azure-integration owns shared Azure tenant/SDK coordination; terraform-iac owns infra plans, this skill owns Azure Service Bus semantics.

## Completion
Chosen credential, resource ID/region, minimum roles, working SDK contract and explicitly scoped sandbox evidence.
