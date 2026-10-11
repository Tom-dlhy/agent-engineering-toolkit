# Google Cloud Pub/Sub — operations and recovery verification

**Read when:** selecting production capacity, cost, rollback, monitoring or integration failure behavior.

## Service-specific engineering
At-least-once redelivery is default; exactly-once delivery feature has explicit supported constraints (pull and region), not all push/external effects. Ack deadline extensions, duplicate/retry, ordering keys, DLQ permissions, backpressure and subscriber shutdown.

## Identity and resilience constraints
Use workload service account; publisher and subscriber grant separate IAM. Push to private Cloud Run requires authenticated OIDC invoker identity. Publisher `roles/pubsub.publisher` on topic; consumer `roles/pubsub.subscriber` on subscription. Push service-account token creator/invoker grants distinct; no project Editor role.

Measure p95/p99 latency, error/queue backlog, resource limits, regional availability, quota project and relevant billable units. A successful local SDK call is not proof of end-to-end authorization, service-to-service JWT identity or failover. For mutations, treat post-send network timeout as **unknown remote outcome** and reconcile before retry; use per-service preconditions/deduplication features where documented.

## Required negative and integration tests
1. Wrong project/region and revoked service-account grant cause deterministic denial.
2. Expired/incorrect identity and wrong resource produce safe error mapping, no credentials in logs.
3. Duplicate/reordered input, timeout after remote commit and cancellation preserve application invariant.
4. Provider regional quota/throttle and network fault trigger bounded retries or fail-closed result.
5. Production claim requires authorized sandbox check of actual IAM, configuration, SDK version and rollback procedure.

## Official docs
- https://docs.cloud.google.com/pubsub/docs/overview
- https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery
