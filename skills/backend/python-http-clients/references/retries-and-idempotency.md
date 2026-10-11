# Outbound HTTP reliability: deadlines, retries, idempotency and protection

**Read when:** deciding whether to retry partner API calls, honoring 429 or managing timeout/partial network failure.

## Classify failure, then decide

| Failure | Default | Important nuance |
|---|---|---|
| DNS/connect/transient transport | Bounded retry for replay-safe operation | Check total deadline and provider expectations |
| Read timeout after POST | Unknown outcome | POST may have committed; never blindly repeat without key |
| 400/401/403/404 | No retry | 404 may be a business resource miss |
| 409/412 | Conflict resolution | Optimistic concurrency/version |
| 429 | Rate limit/backoff | Respect supported Retry-After, per-user/per-tenant budgets |
| 500/502/503/504 | Possible retry | Only if operation is replay-safe and budget allows |
| JSON/schema invalid | Normally no retry | Raise protocol change, alert; avoid hammering |
| Cancellation | Propagate promptly | Don't transform into success or retry |

## Deadline budget

Total user-facing deadline = app processing + DNS/connect + read + backoff + validation + downstream. Four attempts each with 30s timeouts may produce catastrophic p99. Limit total attempts and elapsed time; exponential backoff with **jitter** prevents synchronization. Do not nest SDK retry loops with a second unbounded retry mechanism. Retry only when the *whole operation* remains safe under ambiguity.

## Idempotent non-GET operations

Prefer a client-generated stable idempotency key supported by upstream, kept across retries and stored with request state. A random new key per retry defeats deduplication. If upstream has no idempotency support, implement a durable saga/reconciliation workflow and surface uncertain outcomes to operator. Never retry payments, email sends or order creation indiscriminately.

## Capacity safeguards

Use HTTPX connection pool plus app semaphore/backpressure, provider-specific 429 handling, bounded queues for asynchronous operations. A circuit breaker can reduce calls to persistently failed provider but requires an accurate failure classification, half-open probes and observability; do not add a new library unless justified.

## Negative cases

Timeout after remote commit, duplicate POST, retry storm during 503, Retry-After (seconds and HTTP-date formats), partial success and cancellation during backoff. Verify no duplicate external side effects and a bounded latency impact.

Official: https://www.python-httpx.org/advanced/transports/ and https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429 and https://www.rfc-editor.org/rfc/rfc9110.html .
