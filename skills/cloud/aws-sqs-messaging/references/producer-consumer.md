# SQS producer and consumer contract

**Read when:** authoring SQS send/receive/delete, choosing FIFO or designing message schemas and idempotent consumers.

## Producer

Message contract should carry `event_type`, `schema_version`, `event_id`, `correlation_id`, `occurred_at`, `entity_id` and a small non-secret payload. Validate size against service limits and keep large documents in S3 with a secured pointer.

```python
import json

def enqueue_job(sqs, queue_url: str, job_id: str, object_key: str) -> None:
    event = {
        "schema_version": 1,
        "event_type": "report.requested",
        "event_id": job_id,
        "object_key": object_key,
    }
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(event))
```

For FIFO queue URLs, include `MessageGroupId` (and `MessageDeduplicationId` unless documented content-based deduplication handles it). The group partitions ordering: a single group can serialise work and reduce throughput.

## Polling consumer

```python
def consume_one(sqs, queue_url: str, handle) -> int:
    result = sqs.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10
    )
    count = 0
    for msg in result.get("Messages", []):
        event = json.loads(msg["Body"])
        # handle must atomically deduplicate the business event ID and
        # persist the side effect before returning successfully.
        handle(event)
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
        count += 1
    return count
```

If `handle` fails, do not delete. The visibility timeout eventually exposes the message for another attempt. It is normal for the same message to be delivered multiple times (including before timeout in some cases); business operations must be idempotent.

## Deduplication strategies

- Database unique constraint on `event_id` plus transactionally recorded outcome.
- Conditional write/lock in durable KV store with TTL chosen for realistic retry/replay windows; only mark "processed" after side effect commits.
- Outbox for committing business state and enqueue intent together; a reconciler publishes pending events and marks delivered.
- For external non-idempotent APIs, use their idempotency key if supported; otherwise design compensation and human reconciliation.

**Anti-pattern:** in-memory `set()` of processed IDs — evaporates on restart and cannot coordinate scaled consumers.

## Observe and test

Track `ApproximateAgeOfOldestMessage`, message backlog, consumer error rate, retries, DLQ depth, successful business processing and invalid schema rejects. Simulate duplicate delivery and process crash at every boundary. Do not include PII or presigned tokens in message bodies.

Official: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html and https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html .
