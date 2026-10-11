---
name: typescript-api
domain: backend
version: "0.1.0"
description: >-
  Use when building Node.js and TypeScript APIs with runtime validation, service layers, dependency boundaries and production observability. Do not use for a Python-only backend.
---

# typescript-api

## Structure
Separate router/handler, validation, application service, domain and adapters. Keep TypeScript types from being mistaken for runtime validation: use schema parsers at untrusted inputs.
## Runtime
Define supported Node LTS version, reproducible dependencies and package-manager lockfile. Prefer typed error classes mapped centrally to safe HTTP responses. Set bounded external API timeouts, cancellation and idempotent retries.
## Security and operations
Implement authorization in application paths, not only routing. Use secure session/token handling, secret injection and redacted structured logs. Handle graceful shutdown, connection pooling and health/readiness semantics.
## Tests
Cover HTTP contracts, invalid payloads, auth boundaries and real adapters; run typecheck, lint, tests and production build.
