# Cloudflare R2 object storage — release, limits, security and incident recovery

**Read when:** deploying, troubleshooting production behavior or validating security/consistency.

## Service-specific failure modes
Use HTTP conditional headers, ETag/version management, size/multipart upload, object lifecycle/cost, retention, key validation and explicit public access gates. Worker binding API ≠ full AWS S3 API, SDK compatibility varies.

## Trust and tenancy
R2 bucket binding rights derive from Worker deploy configuration; S3 API tokens are separately bucket-scoped. Bucket private by default; r2.dev public URL intended for development, not production custom-domain security control.

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
- https://developers.cloudflare.com/r2/api/workers/workers-api-reference/
- https://developers.cloudflare.com/r2/buckets/public-buckets/
