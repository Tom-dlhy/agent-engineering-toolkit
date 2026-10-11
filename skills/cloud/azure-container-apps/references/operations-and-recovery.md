# Azure Container Apps — production reliability, security and recovery

**Read when:** planning scaling, identity propagation, service monitoring, rollback or incident diagnosis.

## Service-specific failure modes
Ingress public by accident, image pull denied, secret not available to revision, revision traffic split, minReplicas=0 scaling to zero with ingress disabled, KEDA poll and cooldown misunderstood, egress/private endpoints.

## Role and resource boundary
Deployer requires approved Container Apps/resource group scope; runtime MI receives narrow Key Vault/Blob/Service Bus data roles. Container registry pull requires correct AcrPull/identity; secrets references and ingress policy separate.

## Operational selection
Use observed p95/p99, error rates, in-flight operations, downstream quotas, regional availability and current cost calculator — never fixed user-count scaling rules. Retrying a mutation after timeout can duplicate side effects if remote commit succeeded; use conditional request, idempotency and durable reconciliation supported by this service. Distinguish route ingress auth, data access RBAC and application tenant-level authorization.

## Fault and release checks
1. 401/403 for wrong tenant/role; no fallback to unapproved credentials.
2. Wrong resource/region and firewall deny with actionable logs without secrets.
3. Retry/duplicate/timeout/error surfaces safe application exception, no blind side-effect replay.
4. Test shutdown, concurrency, cost saturation and recovery in disposable resource group or mock provider.
5. Production operations (deploy, delete, IAM change, network rule) require reviewed plan and explicit consent.

## Official docs
- https://learn.microsoft.com/en-us/azure/container-apps/managed-identity
- https://learn.microsoft.com/en-us/azure/container-apps/scale-app
