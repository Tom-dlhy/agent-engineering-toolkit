---
name: azure-integration
domain: cloud
version: "0.1.0"
description: >-
  Use when implementing Microsoft Azure integrations such as Blob Storage, Service Bus, Container Apps, Functions or Azure AI services. Do not use for projects that do not use Azure.
---

# azure-integration

## Identity
Prefer managed identities and Azure Identity credential chains over static connection strings and secrets. Scope Azure RBAC to necessary resource groups/resources. Avoid embedding Azure SDK models in business/domain entities; map responses at adapter boundaries.

## Reliability
Set explicit timeouts, retry policy and idempotency/deduplication according to each service's documented semantics. Model Service Bus message settlement and poison message handling. Validate storage security, private endpoints, networking and data residency.

## Deployment and test
Use declarative IaC with reviewed plans, environment-specific configuration, telemetry via appropriate Azure monitoring tools, and cost limits. Unit-test application ports without Azure access; run sandbox integration tests with least privilege. Never mutate subscriptions or IAM roles without user approval.
