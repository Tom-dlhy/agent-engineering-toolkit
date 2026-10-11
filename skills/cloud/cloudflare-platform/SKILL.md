---
name: cloudflare-platform
domain: cloud
version: "0.2.0"
description: >-
  Use when coordinating Workers, Pages, R2, D1, Access and cross-resource bindings, environments or deployments. Do not use for a single R2/D1/Workers/Access operation with an individual skill.
---

# Cloudflare integration coordinator

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Route runtime/Pages to cloudflare-workers-runtime, R2 to cloudflare-r2-storage, D1 to cloudflare-d1-database, Access to cloudflare-access-security. KV/Queues/Durable Objects remain explicit future candidate only when real implementation demand exists.
3. Worker runtime receives env bindings and secrets; Wrangler/deployment accesses Cloudflare control plane via scoped token or developer OAuth. Runtime binding credentials are not dashboard tokens. Preview/prod env can bind different databases/buckets.
4. Access protecting /admin doesn't grant per-resource app authorization; verify token signature and audience for origin; protect preview/admin routes and confirm deployed route/domain and CMS-specific constraints. Workers Node compatibility is not full Node process.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns Cloudflare integration coordinator cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
