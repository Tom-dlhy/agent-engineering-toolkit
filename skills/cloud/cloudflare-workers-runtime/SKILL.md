---
name: cloudflare-workers-runtime
domain: cloud
version: "0.1.0"
description: >-
  Use when deploying TypeScript Workers, Pages Functions, bindings, environments, secrets, routes and request execution. Do not use for Cloudflare R2, D1, Access policy semantics or Node-only backend deployment.
---

# Cloudflare Workers and Pages runtime

## Implementation method
1. Confirm account/zone, deployment runtime, preview/production environment, resource binding and approved operations.
2. wrangler CLI authenticated with a narrowly scoped Cloudflare API token; runtime services via bindings passed as env, not a management API token.
3. Token permissions scoped to intended account/zone/Workers edit for deployment; production runtime secret binding not equivalent to dashboard/API token. Separate preview/production vars and domains.
4. Workers runtime APIs may differ from Node full modules; enable nodejs_compat only when supported. Preserve Request/Response streaming, CPU/subrequest/memory limits, Pages build outputs and preview secrets isolation; avoid exposing /admin preview routes.
5. Test against local Wrangler and authorized preview plus production release plan; no deploying, DNS or permission changes without approval.

## Selective reference leaves
- [Bindings, credentials, code](references/connection-and-permissions.md) — **read when** wiring Cloudflare Workers and Pages runtime, API tokens and access scopes.
- [Operations and security QA](references/operations-and-recovery.md) — **read when** hardening data access, diagnosing, scaling or releasing.

## Boundary
cloudflare-platform routes cross-service concerns; frontend skills own UI; terraform-iac owns approved IaC. This skill owns Cloudflare Workers and Pages runtime API and runtime guarantees.

## Done
Binding/configuration and account identified, scoped access and no secrets in client bundles, negative tests, current limitations and safe rollout documented.
