---
name: fastapi-service
domain: backend
version: "2.0.0"
description: >-
  Use when working on FastAPI HTTP endpoints, lifespan resources, DI, Pydantic request/response contracts, exception handlers and API testing/deployment. Do not use for a plain Python script or unrelated ML notebook.
---

# FastAPI — lifecycle, contracts and production HTTP

## Start with the existing app

Identify FastAPI/Pydantic versions, current ASGI server, routers, authentication, DB/HTTP clients, startup ownership, response model and error contract. Avoid rewriting an existing service to a template.

## Execution plan
1. Separate routing (HTTP validation/status) from application service (business rules) and infra (SQL/SDK/HTTP clients). Pick layered or feature-first folder organization according to python-project-architecture.
2. Use lifespan for shared connections and client disposal. Request DI constructs per-request dependencies; never share mutable AsyncSession across requests/tasks.
3. Define Create, PATCH/Update, Response, paginated List models; enforce explicit invariants, distinguish unset vs null. Never return ORM secrets.
4. Translate expected domain failures to stable public 404/409/422/503; distinguish upstream 429/4xx/5xx, and sanitize internal exception text.
5. Handle request IDs, metrics/traces and exceptions consistently, including 500s, stream behavior and trust boundaries.
6. Test unit, route contracts, startup/shutdown and real adapter integration. Operate with worker/pool/timeout budgets and graceful shutdown.

## Select only needed references
- [Lifespan, dependency injection and shared clients](references/lifespan-and-di.md) — read when wiring resources, settings and composition root.
- [Pydantic DTOs, PATCH semantics and error mapping](references/schemas-and-errors.md) — read when implementing Create/Update/Response/List or 4xx/5xx contracts.
- [Middleware and request context](references/middleware-and-request-context.md) — read when adding correlation IDs, request telemetry or security headers.
- [API tests and deployment readiness](references/testing-and-deployment.md) — read when validating overrides, lifespan tests, load/health or serving in production.

## Done
No leaked credentials or raw tracebacks, stable API contracts, explicit ownership, negative tests, auth/tenant checks, startup/shutdown and verified readiness semantics.
