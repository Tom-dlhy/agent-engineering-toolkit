---
name: aws-eventbridge
domain: cloud
version: "0.1.0"
description: >-
  Use when publishing, filtering and routing AWS business events using event buses, rules, targets or schedules. Do not use for SQS queue visibility/DLQ consumer mechanics or domain-level saga choreography.
---

# Amazon EventBridge — dedicated production skill

## Scope and first decisions
Confirm deployment type, AWS account/region, resource identifier and required operation. Identify whether this is a read-only diagnostic, business mutation or infrastructure change; **do not execute cloud changes without explicit authorization**.

## Connect and implement
1. Follow the workload role/Boto3 credential chain, not embedded static keys. Verify identity/account/region before diagnosing permissions.
2. Establish resource-specific permissions, TLS/network path and correct SDK operation. Role-based AWS SDK to chosen account, bus ARN and region. Producer and target invoke roles/resource policies are different permission layers.
3. Use a shared client at controlled lifetime; configure bounded retries/timeouts and translate cloud errors to application-level errors.
4. Choose EventBridge rules vs Scheduler for schedules, target retry/DLQ configs, idempotent consumer with event ID, metrics FailedInvocations and delivery latency. Verify new Custom Event Bus/Subscriber support before assuming Classic rule/target behavior.
5. Verify with fake clients and test failures; only run authorized sandbox integration with a scoped identity.

## Only read task-specific references
- [Connection, SDK, CLI and IAM](references/connection-and-permissions.md) — **read when** configuring auth, SDK calls or AccessDenied.
- [Operations, failure modes and verification](references/operations-and-recovery.md) — **read when** sizing, debugging, recovering or deploying this service.

## Boundary
aws-integration coordinates multiple AWS services; aws-iam-security owns cross-service IAM; terraform-iac owns infrastructure plan/apply; this skill owns Amazon EventBridge semantics.

## Done
Verified caller identity and resource scope, permission matrix, explicit operation behavior, mock tests and documented unverified live connectivity.
