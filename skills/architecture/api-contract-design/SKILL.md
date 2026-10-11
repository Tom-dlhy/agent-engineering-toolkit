---
name: api-contract-design
domain: architecture
version: "0.1.0"
description: >-
  Use when designing REST, GraphQL or event API contracts that must remain stable across clients and services. Do not use for private one-off function boundaries.
---

# api-contract-design

## Contract-first
Define consumers, resources, commands, schema, authentication, authorization and meaningful error semantics. Make breaking changes visible with OpenAPI/JSON Schema or explicit event schemas.
## Compatibility
Prefer additive changes, stable identifiers, pagination and explicit nullability. Document deprecation, versioning, idempotency, rate limits and retry guidance. Avoid ambiguous 200 responses for domain failures.
## Security
Reject unrecognized sensitive fields where appropriate. Validate input at boundaries and return safe errors; do not expose internal exception strings.
## Verify
Run schema validation, generated-client smoke tests or contract tests with representative clients. Document compatibility impact before merging.
