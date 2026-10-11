# Google Cloud IAM and Application Default Credentials — ADC, permissions and SDK usage

**Read when:** implementing application connectivity or debugging 401/403, project mismatch, IAM or API errors.

## Establish identity safely
Local: Run `gcloud auth login` for CLI and separately `gcloud auth application-default login` for Python ADC; those credentials can differ. Inspect `gcloud config get-value project` and the ADC quota project.
Production: Attach per-workload service account to Cloud Run/GKE/compute or use Workload Identity Federation for external CI; avoid downloadable JSON private keys. Federated direct resource access or service-account impersonation depends on API.
Common identity checks: `gcloud auth list` is **CLI**, while application code uses ADC; run `gcloud auth application-default print-access-token` only for authorized diagnostics and never record the token. `google.auth.default()` can reveal selected project without revealing secret; verify intended project and quota project. Use workload federation for CI/external hosts rather than persistent key files.

## Real service client
google-auth library / google.auth.default() and Google Cloud IAM resource policies. Required permissions: Least privileged predefined/custom role at project/bucket/service/secret scope. External federation requires trusted issuer, audience, attribute conditions and workload identity pool binding; service-account impersonation needs proper Token Creator policy.

~~~python
import google.auth
credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
# Authenticate to chosen Google client with credentials=credentials;
# confirm project and API-specific IAM roles before accessing data.
~~~

Code is illustrative: identifiers are environment/project configuration, required package versions must be pinned, and network calls should only run on approved accounts. Do not print tokens, password, response payload containing PII or raw secrets.

## Fail-safe diagnosis
401/no ADC vs 403 insufficient IAM/API disabled vs wrong project; distinguish OAuth access token for APIs from OIDC ID token for invoking private Cloud Run. Verify separate local impersonation and runtime identity.
Differentiate permission denied from disabled API, wrong project/region, missing network path and expired identity. Never grant Owner/Editor to work around an unknown AccessDenied.

## Official docs
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
- https://docs.cloud.google.com/iam/docs/workload-identity-federation
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
