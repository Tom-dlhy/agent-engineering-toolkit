---
name: aws-integration
domain: cloud
version: "0.1.0"
description: >-
  Use when designing or implementing AWS SDK integrations, IAM roles, S3, SQS, Lambda, ECS, Bedrock or related AWS services. Do not use for a GCP/Azure-only project.
---

# aws-integration

## Adapter design
Put boto3 or the appropriate AWS SDK in an infrastructure adapter; expose a narrow application-facing interface when business logic needs provider independence. Use IAM roles or workload identity rather than embedded long-lived credentials. Favor least-privilege policies scoped to actions/resources and minimize trust relationships.

## Reliability
Set request timeouts, bounded retries with exponential backoff and jitter, idempotency keys or deduplication where needed. Treat SQS as at-least-once, design for duplicates, handle visibility/dead-letter policies and inspect poison messages. For S3, configure bucket policies, encryption, public access settings and lifecycle intentionally. Never assume Bedrock model access, API availability or regions without checking documentation.

## Operations
Use structured redacted logs, tracing, cost tags, budgets and alarms. Prefer Terraform/OpenTofu plans reviewed before apply. Verify in local unit tests with mocked ports and in sandbox accounts with integration tests; do not access production automatically.
