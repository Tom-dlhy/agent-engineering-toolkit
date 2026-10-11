# Modular monolith: public APIs, private internals and import rules

**Read when:** dividing a growing codebase into business modules,
defining public interfaces or enforcing architectural boundaries.

## Boundary is a business capability

~~~text
app/
  platform/          # config, telemetry and cross-cutting runtime
  modules/
    orders/
      public.py      # published commands/queries/data contracts
      domain.py      # rules and invariants
      persistence.py # private table/repository
    billing/
      public.py
      domain.py
      persistence.py
  main.py            # dependency composition
~~~

This tree is illustrative and may be Python-specific, but module
ownership applies to Java/TypeScript and other stacks too.
A module may expose a direct function/application service;
it need not introduce a Protocol unless consumers need stable
independent behavior or test substitutes.

## Dependency rules

- orders may import billing.public when a synchronous business
  result is required, not billing.persistence or billing.domain.
- Private ORM/table entities never travel as a published API.
- Avoid cycles A→B→A; move shared *business* concepts to the
  actual owning module rather than a dumping-ground utils folder.
- Infra/telemetry platform modules may be shared, but cross-
  module transactions and authorization still need explicit owner.
- Avoid making generic global services that can mutate every table.

## Enforcement

Use language-appropriate import graph rules: Python AST/import-linter,
Java package restrictions (ArchUnit), TS ESLint boundaries/dependency
analysis. Tests should deliberately add a prohibited import in a
sandbox fixture and prove that the checker fails; a diagram
alone cannot enforce architecture.

## Architectural tests

Allowed Orders → Billing public, forbidden Orders → Billing
persistence, cycle check, module public contract smoke and
consumer negative authorization. A package layout is useful
only if these rules reflect actual code.

Sources:
https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles and
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html .
