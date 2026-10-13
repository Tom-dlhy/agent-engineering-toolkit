# Azure Service Bus — production reliability, security and recovery

**Read when:** planning scaling, identity propagation, service monitoring, rollback or incident diagnosis.

## Service-specific failure modes
Message lock expires before processing, duplicate delivery after settlement failure, max delivery count/DLQ, session ordering, auth role pending, connection namespace `*.servicebus.windows.net` and network policy.

### Consumer lock and settlement contract
Choose PeekLock for explicit settlement; ReceiveAndDelete accepts transfer
loss. Bound processing/prefetch and renewal; renewal does not guarantee a
valid lock.

After *detected* lock loss, start no new business effect for that delivery.
If an effect already committed, preserve its durable operation result:
failed Complete is not a rollback. On redelivery, reconcile the stable
business operation ID before replay. An in-memory flag is insufficient.

Complete after durably recording success, with the receiver connection open.
Recover a lost lock on a fresh delivery, rather than repeatedly settling
a stale delivery. Shutdown must preserve recovery evidence.

Test both directions: lock loss **before** a new effect means no effect from
that delivery; committed effect followed by settlement failure and
redelivery means one business effect **only when external idempotency is
enforced**. Lock loss during an already-started effect does not provide
perfect fencing. Pin actual SDK exceptions and verify provider behavior in
an explicitly authorized disposable namespace.

Source reviewed 2026-10-13:
https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement

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
