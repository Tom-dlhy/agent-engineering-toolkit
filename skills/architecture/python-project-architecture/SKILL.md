---
name: python-project-architecture
domain: architecture
version: "2.0.0"
description: >-
  Use when choosing or refactoring an entire Python application's package structure, module ownership, layered versus feature-first layout or architecture by project scale and constraints. Do not force DDD/hexagonal patterns onto simple scripts or small CRUD tasks.
---

# Python project architecture — choose complexity deliberately

## Decision algorithm
1. Inventory domain rules, number of independent features/teams, integrations, expected change rate, deployment/runtime and operational constraints. Preserve existing coherent structure.
2. Pick the **simplest architecture that enforces important boundaries**: single module/script, feature-based package, layers, modular monolith, or DDD/hexagonal bounded contexts.
3. Separate three concerns even in small services: transport/API validation, business/application decisions and side-effecting adapters. Do not create an interface for every file.
4. For change across multiple providers or many invariants, define ports around *capabilities*, not vendor SDK shapes. Own transactions and unit of work in the application boundary.
5. Choose sync vs async and request vs background queues by actual latency, throughput and durability requirements; don't equate user count with architecture type.
6. Define a migration path and tests for structure changes. Do not perform a multi-service rewrite without architectural evidence.

## Targeted deep routing
- [Architecture selection by complexity and scale](references/architecture-decisions.md) — read when deciding lightweight, layered, modular monolith or DDD/hexagonal.
- [Concrete Python application trees and dependency boundaries](references/project-layouts-and-composition.md) — read when scaffolding, organizing modules or wiring routes/services/repositories.
- [Architecture evolution and operational scaling](references/evolution-and-scale.md) — read when app grows, teams split, performance changes or a POC must be hardened.

## Related
python-ddd owns aggregates/bounded contexts; hexagonal-architecture owns abstract port/adapters; fastapi-service owns HTTP mechanics; python-persistence owns session/unit of work.

## Definition of done
A chosen architecture with rejected alternatives, dependency direction, enforceable tests, explicit runtime/resource ownership and no unjustified folder proliferation.
