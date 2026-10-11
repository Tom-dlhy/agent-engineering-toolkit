---
name: aws-integration
domain: cloud
version: "2.0.0"
description: >-
  Use when coordinating multiple AWS services or building resilient AWS SDK adapters, credential resolution, retries, errors and region-aware clients. Do not use instead of a specific AWS IAM, S3, SQS, Lambda, ECS or Bedrock specialist.
---

# aws-integration

## Responsibility and boundaries

This is the **AWS integration coordinator**, not an encyclopedia of every AWS service. Keep cross-service identity, SDK boundaries, failure semantics and observability here. For one service, activate its focused skill directly. Avoid loading every service reference.

## Inspect before implementation

1. Detect deployment runtime (local, Lambda, ECS, EC2, EKS), region and account boundaries, SDK and dependency versions, existing IAM role, config and instrumentation.
2. Identify which side effects must be idempotent and which AWS calls may be retried; distinguish read-only/idempotent and non-idempotent operations.
3. Use the SDK credential provider chain; never paste keys, store credentials in prompts or hardcode account identifiers.
4. Create clients at a controlled boundary; configure timeouts, bounded retries and structured error mapping. Do not create clients on every request without a reason.

## Specialist routing

| User request | Activate and read |
|---|---|
| Roles, trust, policy, resource permissions, AccessDenied | `aws-iam-security` |
| Buckets, upload/download, presigned URLs, encryption, lifecycle | `aws-s3-storage` |
| Queues, retries, DLQs, consumer delivery, FIFO | `aws-sqs-messaging` |
| Serverless handlers, triggers, concurrency, packaging | `aws-lambda-runtime` |
| Containers, task definition, Fargate, services, ALB | `aws-ecs-deployment` |
| Bedrock models, inference, tool calling, guardrails | `aws-bedrock` |
| Metrics, tracing, SLOs across providers | Existing `observability-sre` |
| Infrastructure resources/state | Existing `terraform-iac` |

Never activate all siblings merely because the task says "AWS". If the task only changes one service, load the corresponding specialist plus this skill **only if** shared SDK concerns arise.

## Targeted deep references

- [SDK configuration and reliability](references/sdk-reliability.md) — open for boto3/SDK adapters, retries, timeout tuning, errors, cancellation or credential chain.
- [Cross-service execution patterns](references/cross-service-patterns.md) — open for S3→SQS→Lambda, orchestration, compensating actions, correlation and consistency.

## Exit criteria

IAM minimum actions and resource ARNs enumerated; timeout/retry/idempotency policy justified; deployment environment and region verified; observability identifies request IDs and transient/permanent failures; destructive infrastructure operations require explicit approval.
