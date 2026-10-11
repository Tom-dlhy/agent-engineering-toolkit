---
name: authentication-solution-selection
domain: stacks
version: "1.0.0"
description: >-
  Use when selecting or revising an application's end-user authentication/session/identity solution, such as managed identity service, installed auth library, OIDC federation or edge-protected private app. Do not use for a specific provider API implementation, AWS IAM policies, authorization checks on an existing endpoint or building cryptographic login protocols from scratch.
---

# Authentication solution selection — identity boundary before vendors

## Decision and risk gates
1. Inventory existing identity and session provider, framework/runtime, deployment origins, audiences (consumer/B2B/employee/one-user internal), organization/tenant model, login methods, SSO/SCIM/MFA/passkeys needs and any legal data-processing/residency limits. **Preserve suitable existing identity**.
2. Distinguish **user authentication**, **federation (OIDC/SAML)**, **authorization of application resources**, **edge access policies**, **machine-to-machine identity** and **cloud IAM**. An authenticated account or Cloudflare Access token doesn't automatically authorize a tenant-owned record.
3. Compare only realistic classes: maintained framework-integrated library (e.g. Better Auth/Auth.js when compatible); managed identity platform (e.g. Clerk/Cognito/Firebase/Auth0 when requirements/terms fit); enterprise OIDC/SAML; edge gate (Cloudflare Access) for private tool. No DIY password hashing, token signature system, hand-rolled OAuth callbacks or homebuilt identity provider recommended as a shortcut.
4. Hard-filter for required auth methods, MFA/passkeys and phishing-resistance requirements, session revocation and theft recovery, account linking/deletion, tenant/org support, data region, regulatory/privacy controls, hosting/runtime compatibility and licensing/pricing. Do not assume every feature exists on a free tier or current SDK.
5. Require a real **session and authorization boundary**: trusted server validation (issuer/audience/signature/expiry for relevant tokens), secure HttpOnly cookie strategy or appropriate backend-for-frontend, CSRF protection, redirect allowlists, rate limiting, auditability, account recovery and step-up on sensitive actions. The chosen identity vendor does not substitute for object-level permission checks.
6. Cost includes active-user/organization tiers, SMS/email/verification, support, self-hosting and migration/integration effort. Verify vendor limits, version support and hosting adapters from current official docs instead of stale listicles.
7. Validate in a contained prototype: sign up/in/out, refresh/revoke session, failed/missing/expired token, password/passkey reset or recovery, cross-origin cookies, server route bypass, tenant/object isolation and provider outage. Choose smallest safe option with failure/exit plan, never enable identity redirects or DNS changes without approval.

## Read only required expert leaves
- [Identity architecture, federation and provider shortlist](references/identity-model-and-providers.md) — **read when** deciding managed versus library versus edge SSO, OIDC/SAML, and selecting a small credible shortlist.
- [Sessions, token validation, MFA and negative authorization cases](references/session-and-trust-boundaries.md) — **read when** evaluating browser/API session safety, lifecycle and failure paths.
- [Provider migration, tenant identity, compliance and exit](references/identity-migration-and-operations.md) — **read when** moving users across providers, comparing plan/cost/security, or requiring organization identity.

## Boundaries
`cloud/aws-iam-security` and cloud IAM specialists own service/principal permissions; `cloud/cloudflare-access-security` implements Zero Trust gate and JWT runtime; `frontend/<framework>` and `backend` implement installed auth adapters; `quality/secure-code-review` audits authorization vulnerabilities; `architecture/technology-tradeoffs` can compare provider economics. This is **selection**, not identity implementation or a replacement for security review.

## Completion
Risk-grounded fit matrix with versioned official sources, positive/negative integration test plan, chosen provider and rejected alternative, exit/recovery plan and explicit implementation authorization. Never assert NIST/OWASP certification because a library supports MFA.
