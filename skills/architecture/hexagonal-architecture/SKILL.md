---
name: hexagonal-architecture
domain: architecture
version: "2.0.0"
description: >-
  Use when isolating Python application logic from HTTP, SQL, LLM, cloud APIs and messaging through behavior-oriented ports/adapters. Do not create an interface wrapper around every stable utility or framework method.
---

# Ports and adapters — clear dependency direction

## Decisions
1. Identify business capability that must survive infrastructure replacement or be testable without side effects.
2. Define an inward-facing port using domain/application types, not vendor SDK shapes.
3. Build concrete adapters mapping external errors and data, with connection ownership at composition root/lifespan.
4. Test pure use cases with in-memory fakes and adapters with real sandbox/DB contracts. Don't mistake fake-only tests for infrastructure verification.
5. Keep a clear import direction enforced in review or static architecture tests; avoid circular dependencies and a universal ServiceLocator.

## References
- [Ports and adapters in Python](references/ports-and-composition.md) — read when defining Protocols, wiring DI and deciding what to abstract.
- [Adapter contracts and anti-pattern review](references/adapter-tests-and-boundaries.md) — read when testing cloud/HTTP/SQL adapters and avoiding excessive abstraction.

For overall project selection use python-project-architecture; python-ddd is optional for complex domains, not a required companion.
