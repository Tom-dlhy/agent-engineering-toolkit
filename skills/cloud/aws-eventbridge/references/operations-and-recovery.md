# Amazon EventBridge — operations, reliability and failure recovery

**Read when:** hardening a production workload, evaluating scale, handling outages or running negative integration tests.

## Service-specific pitfalls
Partial success within PutEvents batch, event schema drift, unexpected rule pattern, target not authorized, DLQ/failed target delivery, at-least-once/replay and regional bus mismatch.

## Capacity, reliability and cost
Choose EventBridge rules vs Scheduler for schedules, target retry/DLQ configs, idempotent consumer with event ID, metrics FailedInvocations and delivery latency. Verify new Custom Event Bus/Subscriber support before assuming Classic rule/target behavior.

Measure real regional quotas, p95/p99 and spend before selecting capacity or making user-count scaling claims. Separate control-plane resource changes from data-plane business effects. Cloud SDK retries may obscure an outcome after a network timeout: reconcile before replaying potentially committed mutations, and use idempotency/conditional guards where supported.

## Security and observability
Log structured operation type, request ID, resource alias, latency, retry/circuit state and error category, never secret values or raw private payload. Use approved CloudTrail/CloudWatch diagnostic mechanisms with appropriate retention. Confirm relevant encryption/KMS and region/residency assumptions.

## Fault-injection acceptance
1. Missing permission and wrong account/region must fail closed without mutation.
2. Wrong resource/endpoint/network path yields actionable diagnosis, not wildcard IAM escalation.
3. Transient throttle/timeout triggers bounded retry under total deadline; unknown commit result does not blindly replay.
4. Duplicate, stale request and concurrent operation preserve documented invariants.
5. Restore/failover or new version rollout has an explicit tested plan in authorized staging.

## References
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus-perms.html
