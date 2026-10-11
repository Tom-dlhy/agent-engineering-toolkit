# Azure Blob Storage — production reliability, security and recovery

**Read when:** planning scaling, identity propagation, service monitoring, rollback or incident diagnosis.

## Service-specific failure modes
Storage firewall/private endpoint, wrong cloud endpoint, 403 role assignment delay, overwrite race without ETag, SAS leakage/expiry, multipart/large blob cost, lifecycle and public access settings.

## Role and resource boundary
Reader: Storage Blob Data Reader; writer: Storage Blob Data Contributor scoped container/account as supported. SAS signing/service permissions differ; avoid account shared keys, grant user delegation key only where needed.

## Operational selection
Use observed p95/p99, error rates, in-flight operations, downstream quotas, regional availability and current cost calculator — never fixed user-count scaling rules. Retrying a mutation after timeout can duplicate side effects if remote commit succeeded; use conditional request, idempotency and durable reconciliation supported by this service. Distinguish route ingress auth, data access RBAC and application tenant-level authorization.

## Fault and release checks
1. 401/403 for wrong tenant/role; no fallback to unapproved credentials.
2. Wrong resource/region and firewall deny with actionable logs without secrets.
3. Retry/duplicate/timeout/error surfaces safe application exception, no blind side-effect replay.
4. Test shutdown, concurrency, cost saturation and recovery in disposable resource group or mock provider.
5. Production operations (deploy, delete, IAM change, network rule) require reviewed plan and explicit consent.

## Official docs
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-upload-python
