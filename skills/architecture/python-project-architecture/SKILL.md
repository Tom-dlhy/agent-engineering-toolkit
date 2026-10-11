---
name: python-project-architecture
domain: architecture
version: "2.1.0"
description: >-
  Use when selecting or restructuring a Python application package layout,
  layered versus feature-first modules, deployment boundaries and
  evolutionary architecture under actual requirements. Do not force
  DDD, microservices or a src layout on a tiny script.
---

# Python project architecture — choose by boundaries and deployment

## Decision algorithm
1. Inventory codebase and Python/runtime/deploy constraints, user journeys,
   data ownership, team capabilities, changes, concurrency and testing.
2. Select simplest appropriate **project organization** (script/library,
   feature-first, small layers, modular monolith, DDD/hexagonal when justified).
   It is not the job of this skill to choose every vendor SDK/framework.
3. Assign transport validation, business rules, persistence/network adapters
   and application composition to clear owners; don't equate directory names
   with actually enforced imports.
4. Choose request vs queue and sync vs async according to blocking drivers,
   latency and recovery; async doesn't accelerate CPU-bound code.
5. Wire shared clients/DB engines at lifespan; keep AsyncSession/request
   state per task and never open DB transaction across a slow LLM call.
6. Plan package/test/deploy conventions already present; no speculative
   rewrite of a functioning app or arbitrary interfaces just for purity.
7. Validate import boundaries and representative runnable feature
   before declaring refactor complete.

## Targeted references
- [Architecture style choice by complexity](references/architecture-decisions.md)
  — **read when** choosing layered, modular monolith or DDD/hexagonal.
- [Concrete Python package layout and composition](references/project-layouts-and-composition.md)
  — **read when** scaffolding files, DI or enforcing service/adapters.
- [Incremental scale and production evolution](references/evolution-and-scale.md)
  — **read when** turning POC into production, scaling workloads or
  contemplating network-deployed services.

## Distinct ownership
architecture-decision captures major system ADR;
technology-tradeoffs compares concrete products;
python-ddd models domain; hexagonal-architecture defines ports;
fastapi-service implements HTTP endpoints; python-persistence owns DB.

## Exit
One maintainable layout, explicit dependencies/resource lifecycles,
supported alternatives, tests and an evolution path without
imaginary user-count architecture thresholds.
