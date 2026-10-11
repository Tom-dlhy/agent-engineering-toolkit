---
name: python-ddd
domain: architecture
version: "2.0.0"
description: >-
  Use when Python business complexity justifies bounded contexts, domain aggregates, value objects, consistency invariants or domain events. Do not impose entities, factories and repositories on a simple CRUD service.
---

# Python DDD — domain modeling only when justified

## Decide
1. Is domain language contested, are invariants complex or multiple teams share different meanings? If not, prefer layered/feature-first Python application.
2. Draw context map and aggregate ownership from actual business capabilities. Keep domain entities/value objects free of FastAPI, SQLAlchemy and HTTPX.
3. Enforce invariants in domain methods and DB constraints; application use case orchestrates transaction, auth and external ports.
4. Map transport DTO, domain types and ORM models at appropriate boundaries; don't create a useless generic mapper for trivial cases.
5. Test domain invariant failure and concurrent persistence; remember fake repository tests cannot prove database isolation.

## References
- [Bounded contexts, entities, value objects and invariants](references/domain-modeling.md) — read when modeling complex business behavior and consistency boundaries.
- [Use cases, ports, UoW and domain event publishing](references/application-and-events.md) — read when coordinating domain changes, DB transactions and external side effects.

For overall architecture choice use python-project-architecture; hexagonal-architecture owns ports/adapters principle, python-persistence owns DB session and outbox mechanism.
