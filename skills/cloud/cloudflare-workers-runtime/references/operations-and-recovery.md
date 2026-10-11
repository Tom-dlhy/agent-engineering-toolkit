# Cloudflare Workers and Pages runtime — release, limits, security and incident recovery

**Read when:** deploying, troubleshooting production behavior or validating security/consistency.

## Service-specific failure modes
Workers runtime APIs may differ from Node full modules; enable nodejs_compat only when supported. Preserve Request/Response streaming, CPU/subrequest/memory limits, Pages build outputs and preview secrets isolation; avoid exposing /admin preview routes.

## Trust and tenancy
Token permissions scoped to intended account/zone/Workers edit for deployment; production runtime secret binding not equivalent to dashboard/API token. Separate preview/production vars and domains.

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
- https://developers.cloudflare.com/workers/configuration/secrets/
- https://developers.cloudflare.com/workers/runtime-apis/bindings/
