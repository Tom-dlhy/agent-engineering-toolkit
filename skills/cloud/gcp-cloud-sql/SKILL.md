---
name: gcp-cloud-sql
domain: cloud
version: "0.1.0"
description: >-
  Use when connecting Cloud Run/GCP workloads to Cloud SQL PostgreSQL with IAM, private IP, connector, SQLAlchemy or failover. Do not use for general PostgreSQL SQL tuning or AWS RDS and Azure PostgreSQL integrations.
---

# Google Cloud SQL for PostgreSQL

## Decision and connection procedure
1. Identify GCP organization/project, resource ID, region, API enablement, runtime and whether this is a data-plane read/write or IAM/infra operation.
2. Authenticate using ADC and a per-workload identity; local developer ADC ≠ gcloud CLI login. Service account with Cloud SQL Client role + Cloud SQL Connector using ADC; DB credentials/role (or IAM DB auth if configured) remain separate from Google IAM.
3. Apply **service-specific IAM** and, where relevant, database or application authorization. `roles/cloudsql.client` for connector; database user/privileges separate, use Secret Manager or IAM database authentication configuration. Private IP requires network reachability/VPC setup; connector isn't bypass of private routing.
4. Choose API/SDK client with explicit deadlines, replay/idempotency semantics, bounds and cleanup. Pool connection fanout, auth token/DB TLS, instance/project mismatch, private IP/VPC egress, failover connections, migration/version compatibility, PITR/backups and read replica lag. Avoid DB master account in app.
5. Verify behavior in mocks/emulator then an explicitly authorized sandbox project; never create/delete resources or modify IAM without approval.

## Deep references only when needed
- [Identity, connection and API examples](references/connection-and-permissions.md) — **read when** connecting to Google Cloud SQL for PostgreSQL, IAM failures or SDK invocation.
- [Operational limits, security and recovery](references/operations-and-recovery.md) — **read when** deploying, scaling, securing or diagnosing this service.

## Boundaries
gcp-integration coordinates cross-service ADC and projects; data skills own DB/warehouse modeling; terraform-iac owns infrastructure apply.

## Exit
Project/region/identity and IAM actions verified, scoped connection, replay policy, negative tests, and unsupported live assumptions listed.
