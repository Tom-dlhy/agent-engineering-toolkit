---
name: api-contract-design
domain: architecture
version: "0.2.0"
description: >-
  Use when designing public REST, GraphQL, webhook or event API contracts with
  client compatibility, pagination, idempotency, errors and security implications.
  Do not use for unshared internal function signatures or framework route syntax alone.
---

# API contract design — compatibility is observable behavior

## Contract-first method

1. Identify consumers, ownership, trust boundaries, data sensitivity, concurrency,
   reliability targets, and any **existing** published contract. Record expected
   HTTP/event behavior before picking framework or serializer.
2. Choose request/response shape and operations from business semantics, not
   a DB table dump. HTTP methods/status/cache/conditional requests follow
   RFC 9110, while selected error envelopes may use RFC 9457.
3. Specify required/optional/nullable fields independently. For PATCH,
   **missing** is not the same as explicit JSON null; define clearing behavior.
   Mutation calls need concurrency (ETag/If-Match or version) and replay policy.
4. Choose paging/filtering/sort with stable order; control tenant isolation,
   API resource limits and exposure of sensitive fields.
5. Define migration/compatibility against known consumers; additive changes
   are *often* compatible but can break strict schema/enum clients.
6. Select OpenAPI **version supported by actual toolchain** (OAS now has
   3.2.x specs; do not assume generators/validators support 3.2), GraphQL
   schema or AsyncAPI spec as appropriate. A valid schema is not runtime proof.
7. Test compatibility for real representations and negative cases, not only
   generated schema syntax; document sunset/deprecation and error/retry guidance.

## Choose selectively

- [HTTP contract design and RFC error semantics](references/http-contracts-and-errors.md)
  — **read when** choosing REST methods, HTTP statuses, Problem Details,
  idempotency, caching or concurrency preconditions.
- [Schema evolution, consumer contracts and pagination](references/versioning-and-consumer-compatibility.md)
  — **read when** changing a public API, fields, enums, paging,
  deprecation or generator versions.
- [GraphQL, webhook and async contract boundaries](references/graphql-and-async-contracts.md)
  — **read when** designing GraphQL schema, webhook signatures or a
  cross-service message schema/API.

## Ownership
fastapi-service handles Python implementation; event-driven-design handles
message delivery semantics; architecture-decision records major API style
choices; test-strategy owns broad suite design.

## Done
A versioned consumer-facing contract, authorization and data classification,
positive/negative and compatibility tests, rollback/deprecation plan, actual
supported specification/tool versions and unverified consumers named.
