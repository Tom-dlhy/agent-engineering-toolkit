---
name: cloudflare-access-security
domain: cloud
version: "0.1.0"
description: >-
  Use when protecting private Cloudflare-hosted apps, Workers/Pages admin routes, Access policies, JWT validation or service tokens. Do not use for in-application object RBAC, OAuth token minting for Azure or general network firewall selection.
---

# Cloudflare Access Zero Trust

## Implementation method
1. Confirm account/zone, deployment runtime, preview/production environment, resource binding and approved operations.
2. Configure Access app and Include/Require/Exclude policies via scoped Zero Trust console/API; origin verify Access JWT signature/issuer/audience as required, don't trust bare email headers.
3. Access policy controls who passes proxy; per-resource tenant authorization stays in origin code. Service tokens for machine-to-machine and interactive identity are distinct; service token credentials stay secrets.
4. Policy Include/Require/Exclude interactions need explicit tests, OTP/IdP mail delivery vs login eligibility, session expiry, bypass routes, JWT validation if origin exposed, no reliance on CF-Access headers from arbitrary direct traffic.
5. Test against local Wrangler and authorized preview plus production release plan; no deploying, DNS or permission changes without approval.

## Selective reference leaves
- [Bindings, credentials, code](references/connection-and-permissions.md) — **read when** wiring Cloudflare Access Zero Trust, API tokens and access scopes.
- [Operations and security QA](references/operations-and-recovery.md) — **read when** hardening data access, diagnosing, scaling or releasing.

## Boundary
cloudflare-platform routes cross-service concerns; frontend skills own UI; terraform-iac owns approved IaC. This skill owns Cloudflare Access Zero Trust API and runtime guarantees.

## Done
Binding/configuration and account identified, scoped access and no secrets in client bundles, negative tests, current limitations and safe rollout documented.
