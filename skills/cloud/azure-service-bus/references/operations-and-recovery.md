# Azure Service Bus — production reliability, security and recovery

**Read when:** planning scaling, identity propagation, service monitoring, rollback or incident diagnosis.

## Service-specific failure modes
Message lock expires before processing, duplicate delivery after settlement failure, max delivery count/DLQ, session ordering, auth role pending, connection namespace `*.servicebus.windows.net` and network policy.

## Role and resource boundary
`Azure Service Bus Data Sender` for send and `Azure Service Bus Data Receiver` for settlement/receive; manage entities with separate control-plane role. Sessions, queues and topic subscriptions require corresponding permissions.

## Operational selection
Use observed p95/p99, error rates, in-flight operations, downstream quotas, regional availability and current cost calculator — never fixed user-count scaling rules. Retrying a mutation after timeout can duplicate side effects if remote commit succeeded; use conditional request, idempotency and durable reconciliation supported by this service. Distinguish route ingress auth, data access RBAC and application tenant-level authorization.

## Fault and release checks
1. 401/403 for wrong tenant/role; no fallback to unapproved credentials.
2. Wrong resource/region and firewall deny with actionable logs without secrets.
3. Retry/duplicate/timeout/error surfaces safe application exception, no blind side-effect replay.
4. Test shutdown, concurrency, cost saturation and recovery in disposable resource group or mock provider.
5. Production operations (deploy, delete, IAM change, network rule) require reviewed plan and explicit consent.

## Official docs
- https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
- https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement
