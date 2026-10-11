---
name: python-http-clients
domain: backend
version: "2.0.0"
description: >-
  Use for outbound Python HTTPX requests, async reusable clients, partner API adapters, retry/idempotency policies, auth headers, network errors and response validation. Do not use for unrelated FastAPI incoming request handling or SDK-native cloud calls.
---

# Python outbound HTTP — typed, bounded and observable

## Implementation checklist
1. Identify upstream API contract, authentication, allowed base host, rate limit, data classification and method safety; never accept arbitrary user-provided upstream URLs.
2. Share one async client per application process/lifespan (with pool/timeout limits); close on shutdown. Don't instantiate an AsyncClient for every request.
3. Distinguish connection/read/write/pool timeouts, RequestError, HTTPStatusError and JSON/Pydantic validation. Translate to precise application failures, not blanket 503.
4. Validate request/response DTOs and status-specific success/error envelopes; don't send secrets in query params or logs.
5. Retry only suitable transient failures within a total deadline. A timed-out POST might have succeeded. Use idempotency keys or reconciliation.
6. Test transport failures and mapping with HTTPX MockTransport; sandbox integration validates upstream contract and authorization.

## Deep references
- [HTTPX lifecycle and typed adapter](references/httpx-typed-client.md) — read when writing or reviewing actual reusable AsyncClient code and Pydantic response validation.
- [Retries, deadlines, idempotency, rate limits](references/retries-and-idempotency.md) — read when handling 429/5xx/timeouts or choosing circuit breakers/concurrency.
- [Transport tests and provider errors](references/contract-tests.md) — read when building mock transport tests or classifying partner responses.

## Boundaries
Use modern-python for language/tooling; python-observability for trace/log conventions; fastapi-service for inbound HTTP and lifespan wiring.

## Exit
Methods/statuses differentiated, lifecycle owned, retries bounded, failures mapped, secret-safe logs, unit+integration tests with negative outcomes.
