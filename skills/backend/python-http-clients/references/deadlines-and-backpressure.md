# HTTP retries, end-to-end deadlines and backpressure

**Read when:** deciding request timeout, Retry-After, concurrency
limits, circuit breaker or handling a remote unknown outcome.

## Budget propagation

Let the application deadline cover queue wait, pool wait, connect,
read, schema parse, potential retry wait and retry attempts.
Per-phase HTTPX timeouts are *not* the same as a total deadline.
A request with 4 retries × 5 seconds can already violate a
6-second SLO before considering backoff.

## Decision table

| Failure | Retry? | Guard |
|---|---|---|
| Connect timeout before send | Often for safe/idempotent request | Overall budget and bounded attempts |
| Read timeout after POST | Outcome unknown | Stable server idempotency or reconcile |
| HTTP 429 | Possibly | Honor valid Retry-After + quota ceiling |
| HTTP 503/transient 5xx | Possibly | Jitter, max attempts, circuit health |
| HTTP 401/403 | Not blindly | Refresh once only when documented; permission review |
| HTTP 400/422 schema | No until payload changes | Input/data fix |
| 2xx invalid response model | Contract failure | Alert; no blind mutation replay |

## Retry-After
RFC 9110 allows HTTP date or delta-seconds. Parse defensively,
reject negative/implausible values, apply capped jitter and
remaining budget. Preserve upstream rate information without
reflecting secret response headers. Don't let thousands of
workers synchronize on the same retry point.

## Backpressure
Bound concurrent outbound requests with a semaphore or queue,
matching local pool and provider RPM/TPM. A circuit breaker
can avoid repeated known failures but requires half-open
probe, isolation by upstream/tenant and stable state policy.
It does not replace explicit timeout or true availability checks.

## Test uncertain commits
Inject POST performs effect then connection drops. Confirm
retry preserves idempotency key or reconciles with provider.
Inject two simultaneous retries and verify one durable effect.
Model separate partner live API tests when authorized.

Sources: https://www.python-httpx.org/advanced/timeouts/ ,
https://www.python-httpx.org/advanced/resource-limits/ and
https://www.rfc-editor.org/rfc/rfc9110.html .
