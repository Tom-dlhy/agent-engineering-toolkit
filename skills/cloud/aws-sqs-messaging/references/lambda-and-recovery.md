# SQS → Lambda event source mapping and recoverability

**Read when:** configuring SQS triggers for Lambda, partial batch failures, visibility timeouts or DLQ replay.

## Failure behavior

With normal batch processing, if one record fails and the invocation fails, successfully processed records can be retried as part of the entire batch. Implement an idempotent handler. For partial batch behavior, configure the event source mapping with `FunctionResponseTypes=["ReportBatchItemFailures"]`, then return failed `messageId` values.

```python
def handler(event, context):
    failures = []
    for record in event["Records"]:
        try:
            process_event(record["body"])  # durable, idempotent processing
        except Exception:
            failures.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": failures}
```

Do not swallow a failure and report success. If the handler raises rather than returning the partial batch list, the whole batch can be retried.

### FIFO-specific rule

In FIFO processing, after the first failure, stop processing that group/batch according to AWS ordering guidance and include **all failed and unprocessed** record IDs in `batchItemFailures` to preserve ordering. The simple example above is for independent standard-queue messages, not a universal FIFO implementation.

## Timeouts and redrive

- Lambda timeout must fit within the SQS visibility timeout; AWS recommends a larger visibility timeout (often six times function timeout for SQS triggers; account for batch window) to tolerate throttling/retries. Verify current official guidance and configuration.
- DLQ `maxReceiveCount` must allow meaningful transient retries without silently exhausting retention; set alarming and ownership for DLQ triage.
- Match message retention to outage tolerance; beware oldest-message backlog alarms and in-flight limits.
- If downstream database throughput is bounded, restrict event source max concurrency/batch sizes appropriately, rather than allowing retry storms.

## Recovery runbook

1. Identify queue, message version and principal; inspect DLQ **without exposing sensitive payloads**.
2. Classify transient dependency failure vs permanent schema/business failure.
3. Fix root cause and test replay in staging with sample payloads.
4. Replay with documented idempotency handling and business side effect verification.
5. Confirm DLQ age/depth declines and no duplicate business records were created.

## Test matrix

Process first record successfully and second fails; throw exception vs return list; duplicate events; FIFO first-record failure; poison message; timeout; queue permission denied; DLQ redrive and backlog alarms.

Official: https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html and https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html .
