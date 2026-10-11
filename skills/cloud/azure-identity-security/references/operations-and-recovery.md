# Azure Identity, Entra and RBAC — production reliability, security and recovery

**Read when:** planning scaling, identity propagation, service monitoring, rollback or incident diagnosis.

## Service-specific failure modes
Wrong tenant/subscription, unrelated developer credential chosen by DefaultAzureCredential, missing Managed Identity assignment, wrong token audience, resource firewall/private endpoint or eventual RBAC propagation.

## Role and resource boundary
Data plane vs ARM management roles differ. Azure RBAC assignment can propagate with delay. `AZURE_TOKEN_CREDENTIALS=prod` (azure-identity >=1.23) narrows DefaultAzureCredential chain; explicit ManagedIdentityCredential reduces ambiguity further.

## Operational selection
Use observed p95/p99, error rates, in-flight operations, downstream quotas, regional availability and current cost calculator — never fixed user-count scaling rules. Retrying a mutation after timeout can duplicate side effects if remote commit succeeded; use conditional request, idempotency and durable reconciliation supported by this service. Distinguish route ingress auth, data access RBAC and application tenant-level authorization.

## Fault and release checks
1. 401/403 for wrong tenant/role; no fallback to unapproved credentials.
2. Wrong resource/region and firewall deny with actionable logs without secrets.
3. Retry/duplicate/timeout/error surfaces safe application exception, no blind side-effect replay.
4. Test shutdown, concurrency, cost saturation and recovery in disposable resource group or mock provider.
5. Production operations (deploy, delete, IAM change, network rule) require reviewed plan and explicit consent.

## Official docs
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/user-assigned-managed-identity
