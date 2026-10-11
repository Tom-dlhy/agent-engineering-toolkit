---
name: hexagonal-architecture
domain: architecture
version: "2.1.0"
description: >-
  Use when separating domain/application behavior from HTTP, SQL, LLM,
  messaging or cloud infrastructure with ports and adapters in a Python
  application. Do not create an interface per utility or demand DDD.
---

# Hexagonal architecture — stable business ports

## Decide before refactor
1. Map one capability and its external collaborators, inputs/outputs and
   failure invariants. Does business logic change independently of DB/HTTP?
2. Define **behavior-oriented ports** in application/domain language,
   not interfaces reproducing every library method. Python Protocol,
   abstract interface or small concrete dependency may each be appropriate.
3. Keep dependency direction inward. Domain has no FastAPI, ORM, cloud
   SDK or HTTP exception; adapters translate shape/status/error semantics.
4. Application use case owns orchestration and transaction boundary;
   composition root/lifespan wires shared clients and request-scoped state.
5. Do not pass user/tenant context implicitly through global mutable
   adapter; apply authorization before side effects, including LLM tools.
6. Verify pure use case with fakes and adapters with real disposable
   contract tests. Mock-only green does not prove provider IAM/schema.
7. Prefer fewer clean boundaries over empty folders, "repository for every
   table", Service Locator or blanket middleware layers.

## Selective references
- [Python ports, Protocol and composition](references/ports-and-composition.md) —
  **read when** defining a real behavior contract and its adapters.
- [Boundary contract tests and anti-patterns](references/adapter-tests-and-boundaries.md)
  — **read when** verifying adapters, domain error translation and
  test doubles without distorting semantics.
- [When to adopt and enforcement strategies](references/adoption-and-boundary-enforcement.md)
  — **read when** deciding if ports are worth their complexity,
  enforcing imports or migrating a coupled codebase incrementally.

## Boundaries
python-project-architecture owns whole Python layouts;
python-ddd owns aggregate modeling; modular-monolith owns module
boundaries; this skill owns inward-facing ports/adapters only.

## Exit
Explicit dependency directions, minimal stable ports, transaction/resource
ownership, concrete validation of adapter error/feature paths, and
rejected unnecessary abstraction.
