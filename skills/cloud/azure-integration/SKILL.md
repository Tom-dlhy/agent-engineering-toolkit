---
name: azure-integration
domain: cloud
version: "0.2.0"
description: >-
  Use when coordinating multiple Azure services, Entra identity, RBAC data/control-plane access and SDK clients. Do not use for a single Azure service with a dedicated specialist.
---

# Azure integration coordinator

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Route Entra/IAM to azure-identity-security, Container Apps to azure-container-apps, Blob to azure-blob-storage, Service Bus to azure-service-bus, Key Vault to azure-key-vault, Functions to azure-functions-runtime, Azure Foundry to azure-ai-foundry.
3. Use `DefaultAzureCredential` for local dev where suitable; prefer intended explicit `ManagedIdentityCredential` in deployed service with user-assigned identity. Check actual azure-identity version before use of AZURE_TOKEN_CREDENTIALS=prod. Ensure correct audience (data plane vs ARM).
4. Azure Contributor management role does not automatically grant storage Blob/Service Bus/Key Vault data roles. Check tenant, subscription, managed identity principal, network endpoint and RBAC propagation. IAM changes require approval.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns Azure integration coordinator cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
