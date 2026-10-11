# Azure Key Vault — production reliability, security and recovery

**Read when:** planning scaling, identity propagation, service monitoring, rollback or incident diagnosis.

## Service-specific failure modes
RBAC propagation, wrong vault tenant, disabled/soft-deleted secret, rotation cache stale, firewall/private endpoint blocked, leaked exception/debug logs and version alias confusion.

## Role and resource boundary
`Key Vault Secrets User` (data-plane read) at vault or scoped resource where supported; `Key Vault Secrets Officer` needed to manage secrets; choose RBAC mode or legacy access policy per vault configuration, never assume both.

## Operational selection
Use observed p95/p99, error rates, in-flight operations, downstream quotas, regional availability and current cost calculator — never fixed user-count scaling rules. Retrying a mutation after timeout can duplicate side effects if remote commit succeeded; use conditional request, idempotency and durable reconciliation supported by this service. Distinguish route ingress auth, data access RBAC and application tenant-level authorization.

## Fault and release checks
1. 401/403 for wrong tenant/role; no fallback to unapproved credentials.
2. Wrong resource/region and firewall deny with actionable logs without secrets.
3. Retry/duplicate/timeout/error surfaces safe application exception, no blind side-effect replay.
4. Test shutdown, concurrency, cost saturation and recovery in disposable resource group or mock provider.
5. Production operations (deploy, delete, IAM change, network rule) require reviewed plan and explicit consent.

## Official docs
- https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python
- https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide
