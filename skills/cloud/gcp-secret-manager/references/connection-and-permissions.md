# Google Secret Manager — ADC, permissions and SDK usage

**Read when:** implementing application connectivity or debugging 401/403, project mismatch, IAM or API errors.

## Establish identity safely
Local: `gcloud auth application-default login` with proper project; verify secret version name and appropriate per-secret grant, no printing secret value.
Production: Attach runtime service account and grant secret-specific accessor. Avoid downloading static JSON keys; use secret volume/env injection or SDK retrieval per rotation needs.
Common identity checks: `gcloud auth list` is **CLI**, while application code uses ADC; run `gcloud auth application-default print-access-token` only for authorized diagnostics and never record the token. `google.auth.default()` can reveal selected project without revealing secret; verify intended project and quota project. Use workload federation for CI/external hosts rather than persistent key files.

## Real service client
`google.cloud.secretmanager.SecretManagerServiceClient` with ADC. Required permissions: `roles/secretmanager.secretAccessor` on chosen secret; secret creation/rotation roles separate. API enablement and project/service account selection must be verified.

~~~python
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
resource = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
response = client.access_secret_version(request={"name": resource})
payload = response.payload.data  # sensitive bytes; never log or display
~~~

Code is illustrative: identifiers are environment/project configuration, required package versions must be pinned, and network calls should only run on approved accounts. Do not print tokens, password, response payload containing PII or raw secrets.

## Fail-safe diagnosis
`latest` may rotate between calls, handle explicitly pinned versions for reproducibility when necessary. Verify CRC32C as official sample shows, cache TTL/refresh, forbidden vs nonexistent secrets, secret version disabled/destroyed and retention.
Differentiate permission denied from disabled API, wrong project/region, missing network path and expired identity. Never grant Owner/Editor to work around an unknown AccessDenied.

## Official docs
- https://docs.cloud.google.com/secret-manager/docs/access-secret-version
- https://docs.cloud.google.com/secret-manager/docs/best-practices
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
