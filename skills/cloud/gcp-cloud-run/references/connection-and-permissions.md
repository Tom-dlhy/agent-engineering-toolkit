# Google Cloud Run — ADC, permissions and SDK usage

**Read when:** implementing application connectivity or debugging 401/403, project mismatch, IAM or API errors.

## Establish identity safely
Local: `gcloud auth application-default login` for caller SDK and project; inspect target Cloud Run service URL, region and permitted `roles/run.invoker`.
Production: Attach service identity to caller workload; pass Google-signed OIDC ID token with audience target SERVICE_URL, not arbitrary API OAuth access token.
Common identity checks: `gcloud auth list` is **CLI**, while application code uses ADC; run `gcloud auth application-default print-access-token` only for authorized diagnostics and never record the token. `google.auth.default()` can reveal selected project without revealing secret; verify intended project and quota project. Use workload federation for CI/external hosts rather than persistent key files.

## Real service client
Python HTTPX/requests with google.oauth2.id_token.fetch_id_token() for private service-to-service calls. Required permissions: Caller service account needs `roles/run.invoker` scoped to target service. Deployment principal requires separate create/update/Artifact Registry/IAM grants; runtime service account owns access to downstream services.

~~~python
import google.auth.transport.requests
import google.oauth2.id_token
import httpx
audience = SERVICE_URL  # exact Cloud Run receiver URL
token = google.oauth2.id_token.fetch_id_token(google.auth.transport.requests.Request(), audience)
resp = httpx.get(SERVICE_URL + "/health", headers={"Authorization": f"Bearer {token}"}, timeout=5)
resp.raise_for_status()
~~~

Code is illustrative: identifiers are environment/project configuration, required package versions must be pinned, and network calls should only run on approved accounts. Do not print tokens, password, response payload containing PII or raw secrets.

## Fail-safe diagnosis
Cloud Run public vs authenticated IAM gate; startup probe, concurrency per instance, max/min instances, outbound VPC path, request timeout, cold start, revision traffic split and shutdown/DB connection amplification. ID-token audience for custom path must remain service URL.
Differentiate permission denied from disabled API, wrong project/region, missing network path and expired identity. Never grant Owner/Editor to work around an unknown AccessDenied.

## Official docs
- https://docs.cloud.google.com/run/docs/authenticating/service-to-service
- https://docs.cloud.google.com/run/docs/configuring/concurrency
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
