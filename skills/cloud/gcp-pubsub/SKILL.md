---
name: gcp-pubsub
domain: cloud
version: "0.1.0"
description: >-
  Use when implementing GCP Pub/Sub topics, subscriptions, publisher batching, ack deadlines, ordering and push/pull delivery. Do not use for AWS SQS or Azure Service Bus settlement and streaming Flink state internals.
---

# Google Cloud Pub/Sub

## Decision and connection procedure
1. Identify GCP organization/project, resource ID, region, API enablement, runtime and whether this is a data-plane read/write or IAM/infra operation.
2. Authenticate using ADC and a per-workload identity; local developer ADC ≠ gcloud CLI login. Use workload service account; publisher and subscriber grant separate IAM. Push to private Cloud Run requires authenticated OIDC invoker identity.
3. Apply **service-specific IAM** and, where relevant, database or application authorization. Publisher `roles/pubsub.publisher` on topic; consumer `roles/pubsub.subscriber` on subscription. Push service-account token creator/invoker grants distinct; no project Editor role.
4. Choose API/SDK client with explicit deadlines, replay/idempotency semantics, bounds and cleanup. At-least-once redelivery is default; exactly-once delivery feature has explicit supported constraints (pull and region), not all push/external effects. Ack deadline extensions, duplicate/retry, ordering keys, DLQ permissions, backpressure and subscriber shutdown.
5. Verify behavior in mocks/emulator then an explicitly authorized sandbox project; never create/delete resources or modify IAM without approval.

## Deep references only when needed
- [Identity, connection and API examples](references/connection-and-permissions.md) — **read when** connecting to Google Cloud Pub/Sub, IAM failures or SDK invocation.
- [Operational limits, security and recovery](references/operations-and-recovery.md) — **read when** deploying, scaling, securing or diagnosing this service.

## Boundaries
gcp-integration coordinates cross-service ADC and projects; data skills own DB/warehouse modeling; terraform-iac owns infrastructure apply.

## Exit
Project/region/identity and IAM actions verified, scoped connection, replay policy, negative tests, and unsupported live assumptions listed.
