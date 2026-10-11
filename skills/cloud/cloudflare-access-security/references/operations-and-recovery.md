# Cloudflare Access Zero Trust — release, limits, security and incident recovery

**Read when:** deploying, troubleshooting production behavior or validating security/consistency.

## Service-specific failure modes
Policy Include/Require/Exclude interactions need explicit tests, OTP/IdP mail delivery vs login eligibility, session expiry, bypass routes, JWT validation if origin exposed, no reliance on CF-Access headers from arbitrary direct traffic.

## Trust and tenancy
Access policy controls who passes proxy; per-resource tenant authorization stays in origin code. Service tokens for machine-to-machine and interactive identity are distinct; service token credentials stay secrets.

Runtime Access/Zero Trust controls are not equivalent to application authorization of objects. Synthetic tests should simulate a denied caller, wrong tenant, expired token, missing binding and preview/prod crossed configuration. Never return provider secrets, bearer tokens, raw signed URLs beyond intended audience or unrestricted storage objects.

## Scale and cost
Check actual official Cloudflare limits, CPU/subrequest/storage operations, consistency/availability and account-specific plan in the region/date of execution. Avoid hardcoded pricing or made-up user-count thresholds. If an operation times out after an external mutation, verify idempotency and reconcile state before repeating.

## Release/fault tests
- Wrong binding/resource must fail without granting extra permissions.
- Unauthorized/anonymous access must be rejected at intended boundary.
- Duplicate write, content size, pagination/query limits and network/proxy errors must be handled.
- Verify preview secrets/routing isolation and protected admin URL on production.
- Rollback and data retention/deletion tested in a dedicated environment.

## Official docs
- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/
- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/application-token/
