---
name: cloudflare-d1-database
domain: cloud
version: "0.1.0"
description: >-
  Use when writing Cloudflare D1 queries, prepared statements, SQLite migrations, bindings, replica/session consistency and Worker database access. Do not use for PostgreSQL/Snowflake relational performance or R2 blob storage.
---

# Cloudflare D1 SQLite database

## Implementation method
1. Confirm account/zone, deployment runtime, preview/production environment, resource binding and approved operations.
2. Bind database in wrangler JSON/TOML and access via `env.DB` in Worker; deployment uses scoped Cloudflare account API token for migrations, not a SQL username/password.
3. Binding attached to Worker allows querying configured database; management/migrations via scoped Wrangler deployment account token. Never interpolate raw SQL query parameters, use `.bind()` and validate identifiers.
4. D1 uses SQLite semantics, not PostgreSQL isolation or multi-tenant authorization by default. Bound query/row size, migration strategy, index/performance, read replication/session consistency, backup/restore and env preview DB separation.
5. Test against local Wrangler and authorized preview plus production release plan; no deploying, DNS or permission changes without approval.

## Selective reference leaves
- [Bindings, credentials, code](references/connection-and-permissions.md) — **read when** wiring Cloudflare D1 SQLite database, API tokens and access scopes.
- [Operations and security QA](references/operations-and-recovery.md) — **read when** hardening data access, diagnosing, scaling or releasing.

## Boundary
cloudflare-platform routes cross-service concerns; frontend skills own UI; terraform-iac owns approved IaC. This skill owns Cloudflare D1 SQLite database API and runtime guarantees.

## Done
Binding/configuration and account identified, scoped access and no secrets in client bundles, negative tests, current limitations and safe rollout documented.
