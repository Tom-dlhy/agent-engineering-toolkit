# S3 objects, presigned URLs and uploads

**Read when:** creating object APIs, upload/download endpoints or browser-to-S3 flows.

## Recommended storage contract

Persist metadata separately: `owner_id`, `object_key`, `status`, `expected_size`, `media_type`, checksum, creation/expiration and retention policy. Never trust a browser-supplied S3 key without checking ownership in the application database. Prefer unpredictable IDs (UUID/ULID) and a prefix per tenant; prefixes alone are **not** a substitute for authorization.

## SDK example: server-side upload

```python
import boto3
from botocore.config import Config

s3 = boto3.client("s3", region_name="eu-west-3", config=Config(
    connect_timeout=3, read_timeout=30,
    retries={"mode": "standard", "max_attempts": 3},
))

def store_report(bucket: str, key: str, content: bytes) -> None:
    if len(content) > 5_000_000:
        raise ValueError("unexpected report size")
    s3.put_object(
        Bucket=bucket, Key=key, Body=content,
        ContentType="application/pdf",
        Metadata={"kind": "generated-report"},
    )
```

S3 encrypts newly uploaded objects at rest by default with SSE-S3 for general purpose buckets; regulated deployments may require SSE-KMS with proper key policy. Do not claim this example enforces regulatory compliance.

## Presigned GET (download)

```python
def signed_download(bucket: str, key: str) -> str:
    # Caller authorization must be checked BEFORE this function.
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=300,
    )
```

A presigned URL is a **bearer token**: anyone holding it can use it while valid. Expiry may happen earlier than specified if the credentials used to sign expire. Do not log or send it to analytics/referrer destinations.

## Browser direct-upload pattern

1. Authenticated API checks who may upload, allocates unique key and a pending record.
2. Prefer presigned **POST policy** to constrain uploaded key, content type and declared length; or PUT with specifically signed headers where requirements fit.
3. Browser uploads directly to S3, not through app server. Bucket CORS must allow intended origin and method; CORS does **not** authenticate users.
4. API checks object with `head_object`, size and selected metadata; where security matters, verify actual bytes/content/checksum and run malware inspection asynchronously before publication.
5. Mark object ready only after successful validation; reconcile or expire abandoned uploads.

Presigned PUT with a fixed key can overwrite an existing object; prevent accidental replacement via unique keys, versioning and supported conditional operations where appropriate. Never assume presigned PUT offers the same upload-content constraints as a signed POST policy.

## Large uploads

Use multipart upload when object size and network reliability justify it. Track upload ID, individual part ETags/checksums, abort incomplete transfers, and implement retry on individual parts. Upload completion is a separate operation; abandoned uploads may incur storage costs. Lifecycle rules can abort incomplete multipart uploads.

## Tests

Authorized owner vs another owner, expired URL, wrong Content-Type, oversized actual object, duplicate key, missing object, network retry, abort/reconciliation and SSE-KMS deny.

Official: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html and https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html .
