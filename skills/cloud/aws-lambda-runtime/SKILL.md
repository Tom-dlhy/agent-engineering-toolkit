---
name: aws-lambda-runtime
domain: cloud
version: "2.0.0"
description: >-
  Use when building, deploying or debugging AWS Lambda functions, event triggers, packaging, cold starts, concurrency, IAM execution roles or failure handling. Do not use for long-running ECS-only services or ordinary Python scripts.
---

# aws-lambda-runtime

## Scope and selection

Use AWS Lambda for event-driven work with suitable latency, time, CPU/memory and deployment constraints. For long-running processes, sustained high-throughput web services or specialized runtime requirements, evaluate ECS, Kubernetes or other compute instead. Confirm current Lambda quota and runtime support in the target region.

## Project reconnaissance

1. Record trigger (API Gateway, function URL, SQS, EventBridge, S3), event schema and response contract.
2. Check runtime version, memory/timeout, architecture, package size, VPC/network, reserved/provisioned concurrency, execution role, layers and environment settings.
3. Confirm caller permissions and whether invocation is synchronous, async or event-source polled. Retry and DLQ behaviors vary by trigger.
4. Define error classes, idempotency key, external I/O timeouts and observability before writing handler.

## Implementation rules

Initialize AWS SDK clients and reusable immutable config outside handlers. Do **not** cache tenant-scoped sensitive mutable data across invocations. Make side effects idempotent under duplicate events and retry after unknown outcome. Put business logic in testable functions; treat the handler as transport adapter.

## Read only relevant deep material

- [Handler implementation and trigger semantics](references/handlers-and-events.md) — when authoring handlers, integrating API/SQS triggers or reasoning about event shape.
- [Concurrency, packaging and production](references/performance-and-operations.md) — when deploying, tuning cold starts, networking, timeouts, reserved concurrency or incidents.

Activate `aws-sqs-messaging` only if SQS semantics matter, `aws-iam-security` for policy/trust work and `aws-bedrock` for Bedrock model inference.

## Definition of done

Representative event fixtures pass; duplicate and timeout cases tested; permissions and environment captured; CPU/memory/concurrency are intentional; logs/metrics do not expose payload secrets; deployment changes require approval.
