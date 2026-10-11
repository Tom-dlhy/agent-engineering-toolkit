---
name: aws-dynamodb
domain: cloud
version: "0.1.0"
description: >-
  Use when designing or integrating DynamoDB tables, partition keys, conditional writes, queries, TTL and change streams. Do not use for relational transactions, generic warehouse modeling or SQLAlchemy implementation.
---

# Amazon DynamoDB — dedicated production skill

## Scope and first decisions
Confirm deployment type, AWS account/region, resource identifier and required operation. Identify whether this is a read-only diagnostic, business mutation or infrastructure change; **do not execute cloud changes without explicit authorization**.

## Connect and implement
1. Follow the workload role/Boto3 credential chain, not embedded static keys. Verify identity/account/region before diagnosing permissions.
2. Establish resource-specific permissions, TLS/network path and correct SDK operation. Default Boto3 credentials from role, account and explicit region. IAM permissions target table/index ARNs; Streams may require separate stream ARN actions.
3. Use a shared client at controlled lifetime; configure bounded retries/timeouts and translate cloud errors to application-level errors.
4. Choose keys from access patterns and hot-key distribution, evaluate GSI costs, compare strongly-consistent reads where supported, use optimistic conditions, capacity/autoscaling and stream idempotent processing.
5. Verify with fake clients and test failures; only run authorized sandbox integration with a scoped identity.

## Only read task-specific references
- [Connection, SDK, CLI and IAM](references/connection-and-permissions.md) — **read when** configuring auth, SDK calls or AccessDenied.
- [Operations, failure modes and verification](references/operations-and-recovery.md) — **read when** sizing, debugging, recovering or deploying this service.

## Boundary
aws-integration coordinates multiple AWS services; aws-iam-security owns cross-service IAM; terraform-iac owns infrastructure plan/apply; this skill owns Amazon DynamoDB semantics.

## Done
Verified caller identity and resource scope, permission matrix, explicit operation behavior, mock tests and documented unverified live connectivity.
