---
name: cloudflare-platform
domain: cloud
version: "0.1.0"
description: >-
  Use when building or deploying Cloudflare Pages, Workers, R2, D1 or Access-protected applications. Do not use when Cloudflare is not part of the target architecture.
---

# cloudflare-platform

## Boundaries
Check runtime compatibility (Workers APIs vs Node), database bindings, egress and CPU constraints before choosing libraries. Scope secrets and environment bindings per preview/staging/production.
## Data
For R2, plan access policies, object lifecycle, upload limits and explicit metadata. For D1, consider SQLite semantics, schema migrations, consistency and workload suitability. Access protection does not replace authorization inside the app.
## Deployment
Use isolated preview deployments, reviewed configuration and a documented promotion path; avoid exposing admin routes in preview without controls. Treat browser-to-Worker requests as untrusted.
## Verify
Run tests against relevant Workers emulator/preview, validate permissions and secrets, and inspect release artifacts and zone/dns assumptions. Confirm current quotas/pricing in official docs.
