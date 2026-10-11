---
name: aws-rds-postgres
domain: cloud
version: "0.1.0"
description: >-
  Use when connecting Python applications to RDS/Aurora PostgreSQL, IAM DB authentication, private endpoints, backups or DB failover. Do not use for SQLAlchemy ORM design, general SQL optimization or Cloud SQL/Azure database tasks.
---

# Amazon RDS for PostgreSQL — dedicated production skill

## Scope and first decisions
Confirm deployment type, AWS account/region, resource identifier and required operation. Identify whether this is a read-only diagnostic, business mutation or infrastructure change; **do not execute cloud changes without explicit authorization**.

## Connect and implement
1. Follow the workload role/Boto3 credential chain, not embedded static keys. Verify identity/account/region before diagnosing permissions.
2. Establish resource-specific permissions, TLS/network path and correct SDK operation. Use runtime IAM Role via boto3 Session; DB connection still requires PostgreSQL database role and TLS; `rds-db:connect` is distinct from `rds:DescribeDBInstances`. IAM auth requires role `rds_iam` on PostgreSQL DB user, explicit RDS host:port and short-lived generated token.
3. Use a shared client at controlled lifetime; configure bounded retries/timeouts and translate cloud errors to application-level errors.
4. Use measured pool size × replicas, RDS Proxy when connection churn justifies, Multi-AZ/recovery test, backups/PITR and max_connections headroom. IAM token is generated for NEW DB connection; don't reuse expired token for new connections.
5. Verify with fake clients and test failures; only run authorized sandbox integration with a scoped identity.

## Only read task-specific references
- [Connection, SDK, CLI and IAM](references/connection-and-permissions.md) — **read when** configuring auth, SDK calls or AccessDenied.
- [Operations, failure modes and verification](references/operations-and-recovery.md) — **read when** sizing, debugging, recovering or deploying this service.

## Boundary
aws-integration coordinates multiple AWS services; aws-iam-security owns cross-service IAM; terraform-iac owns infrastructure plan/apply; this skill owns Amazon RDS for PostgreSQL semantics.

## Done
Verified caller identity and resource scope, permission matrix, explicit operation behavior, mock tests and documented unverified live connectivity.
