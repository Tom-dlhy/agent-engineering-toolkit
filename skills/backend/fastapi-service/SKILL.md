---
name: fastapi-service
domain: backend
version: "0.1.0"
description: >-
  Use when implementing or reviewing a Python FastAPI HTTP service and its tests. Do not use for unrelated Python batch jobs or when another backend framework has already been chosen.
---

# fastapi-service

## Implementation checklist
Separate routing, request/response schemas, use cases and infrastructure. Validate boundaries with Pydantic; use dependencies for session/auth/resources rather than mutable globals. Return stable, documented status codes and error contracts. Design idempotent retry-safe mutations when clients can repeat requests.

Use correct async semantics: avoid blocking sync I/O inside async handlers; choose sync handlers or async drivers deliberately. Set explicit timeouts and bounded concurrency for external calls. Never leak exception details, secrets or stack traces to clients.

## Testing and operations
Test validation, error mapping, authentication/authorization, service orchestration and actual DB behavior separately. Include at least one integration path through the HTTP boundary. Add health/readiness checks only with meaningful guarantees, structured logging with redaction, configuration validation and documented startup commands.

## Exit
OpenAPI shape, error cases, deterministic tests and deploy/runtime assumptions are documented.
