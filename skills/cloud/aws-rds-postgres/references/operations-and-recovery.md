# Amazon RDS for PostgreSQL — operations, reliability and failure recovery

**Read when:** hardening a production workload, evaluating scale, handling outages or running negative integration tests.

## Service-specific pitfalls
IAM token expired/reused after new connection, `rds_iam` missing, security group port 5432 blocked, private subnet path, DNS/CA hostname mismatch, failover stale connections, pool amplification and too many DB sessions.

## Capacity, reliability and cost
Use measured pool size × replicas, RDS Proxy when connection churn justifies, Multi-AZ/recovery test, backups/PITR and max_connections headroom. IAM token is generated for NEW DB connection; don't reuse expired token for new connections.

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
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/database-authentication.html
