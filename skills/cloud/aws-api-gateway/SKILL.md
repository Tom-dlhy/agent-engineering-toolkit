---
name: aws-api-gateway
domain: cloud
version: "0.1.0"
description: >-
  Use when exposing AWS HTTP/REST APIs, JWT/IAM/Lambda authorizers, routes, throttling and API-to-Lambda integration. Do not use for FastAPI application route logic or ALB/ECS service deployment.
---

# Amazon API Gateway — dedicated production skill

## Scope and first decisions
Confirm deployment type, AWS account/region, resource identifier and required operation. Identify whether this is a read-only diagnostic, business mutation or infrastructure change; **do not execute cloud changes without explicit authorization**.

## Connect and implement
1. Follow the workload role/Boto3 credential chain, not embedded static keys. Verify identity/account/region before diagnosing permissions.
2. Establish resource-specific permissions, TLS/network path and correct SDK operation. Separate deployment principal (apigateway management actions) from end-user JWT/IAM authorizers. Verify issuer, audience, scopes, custom domain and certificate.
3. Use a shared client at controlled lifetime; configure bounded retries/timeouts and translate cloud errors to application-level errors.
4. Compare HTTP vs REST API supported features/cost, separate authorizer cache/tenant identities, instrument 4xx/5xx/integration latency, canary/versioned routes and deny-by-default policies.
5. Verify with fake clients and test failures; only run authorized sandbox integration with a scoped identity.

## Only read task-specific references
- [Connection, SDK, CLI and IAM](references/connection-and-permissions.md) — **read when** configuring auth, SDK calls or AccessDenied.
- [Operations, failure modes and verification](references/operations-and-recovery.md) — **read when** sizing, debugging, recovering or deploying this service.

## Boundary
aws-integration coordinates multiple AWS services; aws-iam-security owns cross-service IAM; terraform-iac owns infrastructure plan/apply; this skill owns Amazon API Gateway semantics.

## Done
Verified caller identity and resource scope, permission matrix, explicit operation behavior, mock tests and documented unverified live connectivity.
