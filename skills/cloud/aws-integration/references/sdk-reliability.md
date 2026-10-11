# AWS SDK integration, timeouts and reliability

**Read when:** writing boto3/botocore clients, retry/error-handling adapters or investigating unexpected throttling, latency, or credentials.

## SDK and credentials

Prefer the standard credential provider chain (identity from role, SSO/profile or workload federation). Set a region explicitly in application configuration rather than relying on the default from a developer workstation. Run `aws sts get-caller-identity` in the intended environment **only after authorization**, then verify account and role are correct. Avoid `AWS_ACCESS_KEY_ID` embedded in code, logs, tests, Dockerfiles or CI secrets when workload identities are available.

Python example (boto3/botocore — version-match the installed SDK):

```python
import boto3
from botocore.config import Config

config = Config(
    connect_timeout=3,
    read_timeout=12,
    retries={"mode": "standard", "max_attempts": 3},
    user_agent_extra="my-service/1.0",
)
s3 = boto3.session.Session(region_name="eu-west-3").client("s3", config=config)
```

Here `max_attempts` in the `Config` object refers to retries in the botocore configuration convention; validate effective settings using `client.meta.config.retries`, because `total_max_attempts` and environment-level max-attempt settings have different meanings. Use one explicit policy and avoid multiplying SDK retries by unbounded application retries.

## Distinguish failure categories

| Category | Example | Response |
|---|---|---|
| Authentication / authorization | ExpiredToken, AccessDenied | Inspect identity, trust, SCP, permission boundary, resource and key policies. Do not retry blindly. |
| Input or business failure | ValidationException, malformed ARN | Reject/fix caller input; do not retry. |
| Throttling / transient service fault | ThrottlingException, service 5xx | Bounded exponential backoff + jitter, respect operation-specific behavior. |
| Network / timeout | ConnectTimeoutError, ReadTimeoutError | Retry **only** if replay is safe; a timed-out write may have succeeded remotely. |
| Conflict / concurrent update | ConditionalCheckFailedException or service-specific conflict | Resolve consistency conflict; retry only with documented preconditions. |

A successful 2xx SDK response does not prove the downstream business workflow completed. For async systems, use durable state and explicit delivery/processing confirmation.

## Safe adapter example

```python
from typing import Protocol
from botocore.exceptions import ClientError

class ObjectReader(Protocol):
    def read(self, key: str) -> bytes: ...

class S3ObjectReader:
    def __init__(self, client, bucket: str):
        self.client, self.bucket = client, bucket

    def read(self, key: str) -> bytes:
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=key)
            return response["Body"].read()
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code")
            if code in ("NoSuchKey", "404", "NotFound"):
                raise FileNotFoundError(key) from exc
            # Preserve exception linkage for operational diagnosis.
            raise
```

For large objects, stream to bounded memory, validate size and content-type expectations, and close streaming bodies. Do not expose boto3 exceptions or object metadata directly to public API clients.

## Verification matrix

- Fake client unit tests: 200, 404, 403, 429/503, response parse failure, network timeout and retry classification.
- Integration tests in sandbox account: expected principal/region; resource scope; idempotent replays; throttle metrics; no credentials in logs.
- Trace: outbound attempt count, AWS request ID, service/operation, duration; redact keys, presigned URLs, PII and model content.
- Cost: validate SDK retry volume under degraded service; add meaningful alarms to operation error rate and throttling.

Official docs: https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html and https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html .
