---
name: python-http-clients
domain: backend
version: "2.1.0"
description: >-
  Use when building outbound HTTPX synchronous/async adapters with typed
  payloads, deadlines, retries, rate limits, auth and transport contract tests.
  Do not substitute for FastAPI inbound routes or SDK-native LLM/cloud semantics.
---

# Outbound Python HTTP — success, unknown outcome and failure

## Method
1. Confirm target upstream contract/tenant, approved **fixed** hosts, API auth and sensitivity; do not allow caller-supplied URL to bypass SSRF controls.
2. Use shared `httpx.AsyncClient` (or synchronous Client when stack is sync) with scoped ownership, connect/read/write/pool timeout, size and pool limits. Close on shutdown.
3. Differentiate `TimeoutException`, `RequestError`, `HTTPStatusError` and 2xx response schema validation. Catch specific statuses **before** generic unexpected errors.
4. Validate both inbound invocation and upstream response; distinguish malformed JSON vs invalid schema and don't leak raw partner responses or tokens into logs.
5. Retry only eligible transient failures under **total deadline**, with Retry-After and jitter/backpressure. A timeout after a POST may hide a committed side effect: use stable idempotency keys or provider reconciliation, not blind retry.
6. Pass sanitized correlation/trace context; don't use correlation ID as security identity. Handle redirects and authenticated cross-host behavior deliberately.
7. Test with HTTPX `MockTransport` and synthetic 429/500/timeouts/invalid payload plus a separately authorized provider contract check.

## References
- [Typed reusable HTTPX adapter](references/httpx-typed-client.md) — read when writing AsyncClient/Pydantic client.
- [Retries, deadlines and idempotency](references/retries-and-idempotency.md) — read when handling transient errors.
- [MockTransport negative contracts](references/contract-tests.md) — read when testing mapping and cancellation.
- [Authentication, SSRF and payload limits](references/security-and-transport-boundaries.md) — read when dealing with OAuth/mTLS, redirects and user input.
- [Total budgets, retry-after and circuit breaker](references/deadlines-and-backpressure.md) — read when balancing SLO, 429 and concurrency.

## Boundaries
api-contract-design governs published wire contract; python-observability
owns logging/tracing; event-driven-design owns durable event reliability.

## Exit
Client lifecycle, approved destination, precise error taxonomy, bounded
network behavior, idempotence, negative tests and observed gaps documented.
