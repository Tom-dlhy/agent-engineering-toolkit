---
name: modular-monolith
domain: architecture
version: "0.2.0"
description: >-
  Use when structuring a growing single-deploy application into explicit
  business modules with private internals, public contracts, data ownership
  and enforceable dependency rules. Do not use for tiny scripts or assume
  every module should become a microservice.
---

# Modular monolith — strong modules without a network boundary

## Procedure
1. Identify business capabilities/change clusters and boundaries from
   domain vocabulary, ownership and actual dependency graph. Avoid
   a universal services/models/utilities folder.
2. Keep **one deploy** deliberately; a module is a consistency and
   ownership boundary, not automatically a separately deployable service.
3. Define each module's public application API, domain behavior,
   persistence/data ownership, allowed imports and dependency direction.
   No direct cross-module table/model imports for convenience.
4. Choose cross-module semantics per use case: direct in-process call
   for required synchronous result, local transaction for genuinely
   shared consistency, event/outbox only when async failure trade-offs
   justify it. Do not add a broker for every module interaction.
5. Enforce boundaries with automated import checks and module-level
   contract/integration tests; folder structure alone isn't isolation.
6. Track change coupling and scale bottlenecks. Extract a service only
   when ownership, deployment, load or isolation justifies the **new**
   network, distributed tracing and data migration complexity.
7. Preserve existing APIs with incremental module extraction
   (strangler-like approach) and rollback-friendly migration.

## Targeted references
- [Module boundaries and import enforcement](references/modules-and-dependency-rules.md)
  — **read when** designing module public interfaces, reorganizing
  folders or writing architecture boundary tests.
- [Cross-module data, transactions and events](references/cross-module-data-and-consistency.md)
  — **read when** modules share a DB, domain invariants, synchronous
  calls or eventually consistent projections.
- [Incremental evolution and service extraction](references/evolution-and-extraction.md)
  — **read when** planning gradual restructuring, testing coupling,
  deciding whether or how to extract microservices.

## Boundaries
python-project-architecture owns Python scaffolding;
python-ddd owns rich aggregates and contexts;
hexagonal-architecture owns implementation ports/adapters;
event-driven-design owns messaging/replay failure semantics.

## Exit
Public/private imports enforced, realistic business tests, ownership
and transaction map, migration path, measured extraction criteria.
