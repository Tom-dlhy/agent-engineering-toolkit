---
name: aws-vpc-networking
domain: cloud
version: "0.1.0"
description: >-
  Use when designing security groups, subnets, routing, PrivateLink/VPC endpoints, NAT and connectivity for Lambda/ECS/RDS. Do not use for application-level identity policy, Kubernetes CNI internals or Azure VNets.
---

# Amazon VPC networking — dedicated production skill

## Scope and first decisions
Confirm deployment type, AWS account/region, resource identifier and required operation. Identify whether this is a read-only diagnostic, business mutation or infrastructure change; **do not execute cloud changes without explicit authorization**.

## Connect and implement
1. Follow the workload role/Boto3 credential chain, not embedded static keys. Verify identity/account/region before diagnosing permissions.
2. Establish resource-specific permissions, TLS/network path and correct SDK operation. Use STS identity and scoped EC2 Describe permissions for diagnostics; VPC resource changes require separate approved IaC role.
3. Use a shared client at controlled lifetime; configure bounded retries/timeouts and translate cloud errors to application-level errors.
4. Use route table + subnet + SG + NACL + endpoint policy end-to-end; prefer endpoints where viable, assess NAT egress cost and AZ resilience, measure connectivity without revealing credentials.
5. Verify with fake clients and test failures; only run authorized sandbox integration with a scoped identity.

## Only read task-specific references
- [Connection, SDK, CLI and IAM](references/connection-and-permissions.md) — **read when** configuring auth, SDK calls or AccessDenied.
- [Operations, failure modes and verification](references/operations-and-recovery.md) — **read when** sizing, debugging, recovering or deploying this service.

## Boundary
aws-integration coordinates multiple AWS services; aws-iam-security owns cross-service IAM; terraform-iac owns infrastructure plan/apply; this skill owns Amazon VPC networking semantics.

## Done
Verified caller identity and resource scope, permission matrix, explicit operation behavior, mock tests and documented unverified live connectivity.
