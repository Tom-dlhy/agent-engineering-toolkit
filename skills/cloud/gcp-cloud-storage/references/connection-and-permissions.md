# Google Cloud Storage — ADC, permissions and SDK usage

**Read when:** implementing application connectivity or debugging 401/403, project mismatch, IAM or API errors.

## Establish identity safely
Local: ADC login (`gcloud auth application-default login`) and explicit bucket/project and location, signed URL identity as appropriate.
Production: Cloud Run/GKE service account with bucket-scoped IAM instead of JSON private key. V4 signed URLs have specific signing prerequisites; runtime credentials may not directly hold private key.
Common identity checks: `gcloud auth list` is **CLI**, while application code uses ADC; run `gcloud auth application-default print-access-token` only for authorized diagnostics and never record the token. `google.auth.default()` can reveal selected project without revealing secret; verify intended project and quota project. Use workload federation for CI/external hosts rather than persistent key files.

## Real service client
google-cloud-storage `storage.Client` / Bucket / Blob client. Required permissions: Readers `roles/storage.objectViewer` on bucket, writers `roles/storage.objectCreator` or constrained objectUser as needed; bucket metadata/admin roles separate. Use object generation preconditions to prevent lost updates.

~~~python
from google.cloud import storage
client = storage.Client(project=PROJECT_ID)
blob = client.bucket(BUCKET_NAME).blob(OBJECT_KEY)
metadata = blob.reload()  # performs an authorized metadata request
# For upload, specify if_generation_match=0 for create-only idempotence.
~~~

Code is illustrative: identifiers are environment/project configuration, required package versions must be pinned, and network calls should only run on approved accounts. Do not print tokens, password, response payload containing PII or raw secrets.

## Fail-safe diagnosis
Object generation/metageneration, bucket region, retention policies, customer-managed encryption, signed URL expiry, multipart/resumable upload, event notification and lifecycle. Avoid listing entire bucket for a single key.
Differentiate permission denied from disabled API, wrong project/region, missing network path and expired identity. Never grant Owner/Editor to work around an unknown AccessDenied.

## Official docs
- https://docs.cloud.google.com/storage/docs/uploading-objects
- https://docs.cloud.google.com/storage/docs/request-preconditions
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
