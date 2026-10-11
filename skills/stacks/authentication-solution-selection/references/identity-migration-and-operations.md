# Auth provider migration, multi-tenant identity and operations

Read when: migrating current accounts/sessions to a new provider, evaluating enterprise SSO/org membership or reviewing lock-in and cost.

## Identity is high-impact migration
Inventory existing stable account IDs and ownership claims; email address alone is often **not** a durable unique security identifier. Provider-specific subject IDs may change; design immutable app-user mapping with explicit account linking controls. Verify verified-email policies, email change and lost account recovery; avoid automatic merge based solely on matching unverified email.

## Cross-provider migration gates
1. Decide destination provider only after seeing SSO/SCIM/organization, user volume, data residency, legal and pricing constraints.
2. Map `old issuer + old sub -> internal user ID -> new issuer + new sub`; preserve audit provenance. Never trust arbitrary `sub` from an unsigned client request.
3. Plan account linking, credential reset (password hashes may be nonportable), active-session invalidation, session expiry, MFA/passkey re-enrollment, org membership and permission revocation.
4. Preserve authorization invariants during transition. A new provider's `organization` concept may not match product tenant ownership.
5. Dry run with test users, including wrong tenant, duplicate email, revoked account, expired email link, stolen cookie, missing provider, idempotent webhook, recovery escalation and rollback.
6. Price actual active-user/tenant tiers, OTP/SMS traffic, SSO enterprise plans, support, staff operations and downtime; verify contractual support and export/delete features in official docs.
7. Log operational identity failures (without tokens or PII) and define incident owner, signing key rotation, provider outage behavior, backstop/recovery and audit retention. Managed service never replaces app-level access checks.

## Private single-operator case
Consider existing platform's protected-access service before building a username/password database, but confirm actual access policy, identity login method, source/origin bypass, session expiry and backend permissions. HTTP Basic Auth alone may be easy to deploy yet creates important credential rotation, browser storage and fine-grained control limitations; do not claim it equals managed MFA and audit controls.

## Exit
Selected provider, migration/rollback and user notification plan, test accounts and negative checks, session/tenant invariants, cost unknowns, security reviewer and permission to run. No real user export, DNS change, key rotation or login migration without explicit approval.

Sources: https://openid.net/specs/openid-connect-core-1_0.html and https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html and https://clerk.com/docs/guides/secure/session-options and https://pages.nist.gov/800-63-4/sp800-63b/introduction/
