# Google Cloud Pub/Sub — ADC, permissions and SDK usage

**Read when:** implementing application connectivity or debugging 401/403, project mismatch, IAM or API errors.

## Establish identity safely
Local: ADC login with project, topic and subscription IDs; Pub/Sub emulator is useful for local synthetic contract tests but doesn't reproduce IAM/production quotas.
Production: Use workload service account; publisher and subscriber grant separate IAM. Push to private Cloud Run requires authenticated OIDC invoker identity.
Common identity checks: `gcloud auth list` is **CLI**, while application code uses ADC; run `gcloud auth application-default print-access-token` only for authorized diagnostics and never record the token. `google.auth.default()` can reveal selected project without revealing secret; verify intended project and quota project. Use workload federation for CI/external hosts rather than persistent key files.

## Real service client
google-cloud-pubsub `pubsub_v1.PublisherClient/SubscriberClient`. Required permissions: Publisher `roles/pubsub.publisher` on topic; consumer `roles/pubsub.subscriber` on subscription. Push service-account token creator/invoker grants distinct; no project Editor role.

~~~python
from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()
topic = publisher.topic_path(PROJECT_ID, TOPIC_ID)
future = publisher.publish(topic, b'{"event_id":"example"}', event_type="created")
message_id = future.result(timeout=10)  # bounded publish confirmation
~~~

Code is illustrative: identifiers are environment/project configuration, required package versions must be pinned, and network calls should only run on approved accounts. Do not print tokens, password, response payload containing PII or raw secrets.

## Fail-safe diagnosis
At-least-once redelivery is default; exactly-once delivery feature has explicit supported constraints (pull and region), not all push/external effects. Ack deadline extensions, duplicate/retry, ordering keys, DLQ permissions, backpressure and subscriber shutdown.
Differentiate permission denied from disabled API, wrong project/region, missing network path and expired identity. Never grant Owner/Editor to work around an unknown AccessDenied.

## Official docs
- https://docs.cloud.google.com/pubsub/docs/overview
- https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
