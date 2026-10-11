---
name: modular-monolith
domain: architecture
version: "0.1.0"
description: >-
  Use when organizing a growing codebase into bounded modules with clear ownership, transactions and contracts before adopting microservices. Do not use for a tiny app with no modularity pressure.
---

# modular-monolith

## Boundaries
Map business capabilities and ownership. Each module owns its domain, application interface, data-access layer and tests. Expose narrow, documented public APIs; avoid other modules importing internal database models.
## Integration
Prefer in-process use-case calls for synchronous workflows and durable events/outbox where asynchronous delivery is needed. Explicitly define transaction boundaries, consistency and migration ownership.
## Enforcement
Add import-boundary or dependency tests, not just folders. Record coupling and measure changes crossing modules. Plan an extraction path only for modules with separate scaling/deployment requirements.
## Verification
Test module contracts, cross-module workflows and migration behavior. Avoid a single shared global service layer that bypasses boundaries.
