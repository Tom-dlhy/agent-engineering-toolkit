---
name: typescript-api
domain: backend
version: "0.2.0"
description: >-
  Use when implementing Node.js TypeScript REST APIs and services with
  runtime input validation, safe errors, dependencies, tests and deployment.
  Do not apply to Python services or framework-specific frontend rendering.
---

# TypeScript backend — strict types plus runtime proof

## Decision method
1. Inspect existing Node runtime/LTS, module format ESM/CommonJS,
   tsconfig, package-manager lock, server framework and deploy target.
   **Strict TypeScript types disappear at runtime**, so external inputs
   still require schema validation.
2. Choose HTTP adapter (native Node, Fastify, Express, NestJS or
   framework routes) based on existing stack and DI/validation requirements;
   avoid rewriting a working server for fashionable abstractions.
3. Keep route validation/status/public DTO separate from application
   logic and outbound DB/SDK adapters. AuthN ≠ authZ: enforce object/tenant
   rights in application paths, not just middleware.
4. Parse unknown inputs with supported runtime schema library (or JSON
   Schema/Ajv); define null/optional/PATCH semantics and safe errors.
   Fastify uses Ajv v8/JSON Schema Draft 7 by default; never compile
   user-supplied schema as application data.
5. Reuse HTTP/DB connections and guard timeouts/AbortSignal,
   cancellation, shutdown, rate limits and idempotency on mutations.
6. Scope AsyncLocalStorage per request and verify propagation,
   event-loop/blocking CPU and unhandled Promise rejection handling.
7. Execute typecheck, unit, contract/integration and malicious-input
   cases on pinned Node/runtime/platform. Choose deployment health and
   workers by measured workload, not user count.

## Reference router
- [TS Node project/toolchain and server choices](references/node-ts-project-choices.md) — read when choosing framework, ESM, Node runtime or package scripts.
- [Runtime validation, DTO and auth/error boundaries](references/runtime-schema-and-security.md) — read when writing Fastify/Express validators, handlers or scopes.
- [Async lifecycle, fetch/AbortSignal and context](references/node-async-operations.md) — read when handling outbound IO or graceful stop.
- [Tests, build, scaling and release](references/node-testing-and-deployment.md) — read when preparing Node CI, test runner or production worker capacity.

## Boundaries
api-contract-design owns public REST/GraphQL contract;
test-strategy owns full testing mix; dependency-supply-chain owns npm
package risks; this skill owns TypeScript/Node server mechanics.

## Completion
Supported runtime and lock, typecheck + runtime validation, secure
auth/status mapping, bounded resources, negative tests and release proof.
