---
name: fastapi-service
domain: backend
version: "2.1.0"
description: >-
  Use when implementing FastAPI HTTP, WebSocket or streaming endpoints,
  lifespan dependency injection, Pydantic contracts, auth, errors and ASGI deployment.
  Do not apply to unrelated scripts, SQL internals or cloud SDK-only tasks.
---

# FastAPI service — observable behavior and safe lifetimes

## Approach
1. Inspect FastAPI, Pydantic and Starlette versions and actual application conventions. The `lifespan` async context is preferred for shared startup/shutdown resources; do not mix legacy startup event assumptions.
2. Routes own HTTP/request parsing and public responses; application services own business invariants and authorization; adapters own DB/cloud/HTTP protocol mapping. Enforce object-level tenant authorization on reads **and** writes.
3. Keep shared HTTPX client/engine at application lifespan, DB **AsyncSession per request/task**, and no mutable request data in global clients.
4. Define Create / PATCH / Response / List DTOs; distinguish omitted vs null, apply response filters and safe exception mapping. A successful Pydantic parse isn't a security boundary or business decision.
5. Design timeouts, streaming cancellation, disconnect, input/body upload limits, HTTP status/caching, reverse proxy trust and background-job durability separately. Synchronous blocking code inside `async def` can stall event loop.
6. Test lifespan via TestClient context (or explicit ASGI lifespan manager), dependencies with overrides, request validation, 401/403/404/409/422/429/5xx and failure shutdown behavior.
7. Ship with trusted-proxy TLS, worker/pool/DB capacity, readiness vs liveness and graceful termination; never run schema migrations in each worker startup.

## Progressive reference access
- [Lifespan, DI, app composition](references/lifespan-and-di.md) — read when setting clients/DB or overrides.
- [DTOs and exception translation](references/schemas-and-errors.md) — read when implementing request/response/partial updates.
- [Request context, middleware and traces](references/middleware-and-request-context.md) — read when instrumenting and validating headers.
- [Testing, deploy and readiness](references/testing-and-deployment.md) — read when designing CI, worker or startup testing.
- [Security, auth, proxy and uploads](references/security-and-trust-boundaries.md) — read when exposing protected routes, CORS, rate limiting or untrusted files.
- [Streams, SSE/WebSockets and disconnect](references/streaming-and-backpressure.md) — read when implementing long-lived responses and cancellation.

## Exit
Real HTTP contract, authorization, resource lifetimes, negative integration
tests and deployment assumptions proven with limitations clearly labeled.
