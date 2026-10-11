# Lambda handler implementation and event semantics

**Read when:** coding a Lambda handler, selecting trigger or dealing with invalid/inconsistent event envelopes.

## Handler and adapter structure

```python
import json
import os
import boto3

# Client can be reused by warm invocations; do not keep per-request mutable state.
s3 = boto3.client("s3")
BUCKET = os.environ["REPORT_BUCKET"]

def make_response(body: dict, status_code: int = 200) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

def handler(event: dict, context) -> dict:
    # Shape below is illustrative for HTTP proxy integration; inspect
    # actual API Gateway/Function URL event version before relying on it.
    report_id = (event.get("pathParameters") or {}).get("id")
    if not report_id:
        return make_response({"error": "missing report id"}, 400)
    key = f"reports/{report_id}.pdf"
    s3.head_object(Bucket=BUCKET, Key=key)
    return make_response({"status": "available"})
```

Real API code must authorize report owner before S3 access, catch and map expected SDK errors, and not reflect object key or internal exception details. API Gateway REST proxy payload v1, HTTP API payload v2 and Function URLs differ; confirm the actual event schema and status-response shape.

## Invocation differences

| Trigger | Failure and retry ownership | Design requirement |
|---|---|---|
| API Gateway sync | Requesting client / gateway | Return proper status; budget total latency; client retries can duplicate mutations |
| Direct Invoke RequestResponse | Caller | Sync errors surfaced to caller; caller decides retry |
| Async invocation | Lambda async retry/destination configuration | Handle duplicates, destination failures and max age |
| SQS event source mapping | Polling event-source integration | Batch-level or partial-batch retries; visibility, DLQ and ordering |
| S3/EventBridge events | Event source and invocation semantics | Duplicates and ordering vary; deduplicate business event |

## Idempotency boundary

A handler receiving the same business event twice must not charge twice, create duplicate shipments or overwrite a terminal workflow state. Place idempotency in a durable store (conditional write, unique DB key or Powertools idempotency when configured), not module globals.

## Test example

```python
def test_missing_id():
    from app import handler
    result = handler({"pathParameters": {}}, None)
    assert result["statusCode"] == 400
```

Mock or fake SDK calls for unit tests; integration-test IAM, actual trigger mapping and event payload in a sandbox. Assert status and response schema; capture negative payload, resource access denied and duplicate message behavior.

Official: https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html and https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html .
