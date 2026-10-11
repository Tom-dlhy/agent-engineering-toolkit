# Azure Functions (Python v2) — production reliability, security and recovery

**Read when:** planning scaling, identity propagation, service monitoring, rollback or incident diagnosis.

## Service-specific failure modes
Python v1 function.json vs v2 decorator confusion, bindings extension version, event retry/poison queue, host.json scaling, function keys mistaken for user auth, `AzureWebJobsStorage` misconfigured, worker timeout.

## Role and resource boundary
Runtime system-assigned MI with scoped storage/queue/etc roles; function host storage has separate permissions. Deployment principal needs publish/manage rights, not shared with function runtime.

## Operational selection
Use observed p95/p99, error rates, in-flight operations, downstream quotas, regional availability and current cost calculator — never fixed user-count scaling rules. Retrying a mutation after timeout can duplicate side effects if remote commit succeeded; use conditional request, idempotency and durable reconciliation supported by this service. Distinguish route ingress auth, data access RBAC and application tenant-level authorization.

## Fault and release checks
1. 401/403 for wrong tenant/role; no fallback to unapproved credentials.
2. Wrong resource/region and firewall deny with actionable logs without secrets.
3. Retry/duplicate/timeout/error surfaces safe application exception, no blind side-effect replay.
4. Test shutdown, concurrency, cost saturation and recovery in disposable resource group or mock provider.
5. Production operations (deploy, delete, IAM change, network rule) require reviewed plan and explicit consent.

## Official docs
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference
