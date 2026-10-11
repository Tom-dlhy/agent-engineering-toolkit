---
name: aws-sqs-messaging
domain: cloud
version: "2.0.0"
description: >-
  Use when implementing or troubleshooting Amazon SQS standard/FIFO queues, producer-consumer workflows, visibility timeouts, retries, DLQs, Lambda event source mappings or message deduplication. Do not use for unrelated websocket messaging.
---

# aws-sqs-messaging

## Scope

SQS provides durable queueing with **at-least-once** behavior for standard queues. FIFO reduces ordering and duplication problems within documented boundaries but is not a blanket guarantee of exactly-once downstream side effects.

## Choose queue semantics first

- Standard: maximize throughput; tolerate duplicates/out-of-order processing; use idempotency keys.
- FIFO: when per-message-group ordering is essential; define group cardinality and deduplication keys, and understand throughput/ordering constraints.
- Queue consumer: polling worker for explicit control; Lambda event source mapping for managed scaling with batch retry behavior.

## Procedure

1. Specify event schema, stable message ID/business idempotency key and ownership.
2. Select standard/FIFO, visibility timeout, long polling/batch size, retention, DLQ redrive and maximum receives according to processing budget.
3. Make processing idempotent using durable claims or uniqueness; deletion must happen **after** durable success.
4. Expose backlog age, approximate message counts, failed processing and DLQ handling.
5. Test duplicates, crash after side effect but before delete, poison messages, slow handlers and concurrency.

## Deep references

- [Producer/consumer contracts](references/producer-consumer.md) — open for boto3 send/receive/delete, idempotency and FIFO semantics.
- [Lambda batches, DLQ and failure recovery](references/lambda-and-recovery.md) — open for Lambda event mapping, partial batch failures, visibility and redrive.

## Exit

Queue delivery semantics, retry budget, failure policy, backpressure and replay procedures are explicit. Never claim exactly-once business execution without durable application-side controls.
