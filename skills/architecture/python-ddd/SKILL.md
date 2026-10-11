---
name: python-ddd
domain: architecture
version: "2.1.0"
description: >-
  Use when Python domain complexity requires bounded contexts, aggregates,
  value objects, lifecycle invariants, business events and explicit
  consistency boundaries. Do not require DDD for a simple CRUD API.
---

# Python domain-driven design — consistency and language first

## Procedure
1. Establish ubiquitous language with domain experts and discover where
   business terms have different meanings (bounded contexts). Don't
   equate every package/table/REST resource with a bounded context.
2. Find invariants that must hold atomically; group entities into
   aggregates accordingly. Smaller aggregates reduce contention, but
   splitting an invariant across aggregates changes consistency needs.
3. Use meaningful immutable value objects and behavior methods; keep
   domain independent from FastAPI, Pydantic transport DTO, SQLAlchemy
   ORM and provider SDK details unless deliberately justified.
4. Place authorization/orchestration/unit-of-work in application boundary,
   transaction atomicity in infrastructure and domain rules in domain.
5. Domain events record meaningful facts, not ORM row changes. For
   external publishing use transactional outbox and idempotent consumers;
   don't imply events are exactly once.
6. Test business invalid transitions, boundaries and concurrency
   against actual database when persistence isolation matters.
7. For simple domains, prefer feature-first or layered service with
   fewer classes; DDD ceremonies are not mandatory.

## Targeted references
- [Bounded contexts, aggregates and value objects](references/domain-modeling.md)
  — **read when** identifying rich domain behavior or consistency units.
- [Application/use case UoW and domain events](references/application-and-events.md)
  — **read when** implementing domain transitions, repositories and
  reliable event boundaries.
- [Context maps, tactical patterns and evolution](references/context-mapping-and-consistency.md)
  — **read when** negotiating integration between contexts, defining
  translation layers and assessing aggregate/concurrency choices.

## Boundaries
python-project-architecture chooses project style;
modular-monolith defines module ownership;
hexagonal-architecture provides ports/adapters when needed;
python-persistence handles session/locking/DB details.

## Exit
Glossary/context map, invariants and consistency boundaries,
negative/concurrent tests, no leaking infrastructure into domain,
no unjustified aggregate/repository scaffolding.
