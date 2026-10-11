# DDD contexts, aggregate invariants and integration mapping

**Read when:** service/modules use the same business word
differently, ownership is unclear or invariants cross
transaction and external-system boundaries.

## Bounded context ≠ table / microservice

Example: Customer in Identity may mean verified user identity,
while Customer in Billing means payable account. Sharing a
single "Customer" ORM model across both creates semantic
coupling. Map integration via published language or a specific
anti-corruption translation layer, not by forcing one universal
entity through every module.

## Tactical boundary by invariant

One aggregate encapsulates state that must change atomically.
For example, Order confirm requires at least one valid line,
allowed status and version; storing order and each line as
independent aggregates may require extra consistency work.
Not every nested object is an entity; immutable value objects
may capture Money, Address, Period or Quantity invariants.

## Integration modes

| Context relation | Option | Cost |
|---|---|---|
| Same team, same deploy | Public in-process application use case | Coupled deployment |
| Legacy semantics mismatch | Anti-corruption layer translator | Translation/version maintenance |
| Independently owned consumers | Versioned business event | Eventual consistency and replay |
| Immediate shared invariant | One transaction within one store | Reduced independent ownership |

The anti-corruption layer is especially useful when an
unmodifiable legacy domain has different semantics. It
can add latency and operational cost, and may be transitional.

## Race and invariants

A domain check before persistence is not sufficient to
enforce uniqueness under concurrency. Add DB constraint/
version precondition, transaction isolation and negative
integration tests; fakes cannot prove DB isolation.

## Source of domain behavior

Business experts and real workflows, not just API endpoints
or ORM tables. For a CRUD with no complicated domain
lifecycle, a service layer can be enough; no aggregate root
class is mandated.

## Verification

Explicit glossary and context map, state-transition rules,
failed transitions, stale version, concurrent modification,
integration translation, and rejected mismatched schemas.

Sources:
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/acl.html and
https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices .
