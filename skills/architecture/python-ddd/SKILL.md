---
name: python-ddd
domain: architecture
version: "0.1.0"
description: >-
  Use when modeling complex Python business rules, bounded contexts, aggregates, value objects or ports and adapters. Do not use for a trivial CRUD service where DDD would introduce needless ceremony.
---

# python-ddd

## Boundaries
Start from business language, invariants and bounded contexts; identify aggregate consistency boundaries. Keep domain entities, value objects and domain services framework-free. Application use cases orchestrate the domain; infrastructure implements persistence, messaging or cloud dependencies.

Dependencies point inward: HTTP handlers, SQLAlchemy models and boto3 clients must not leak into domain logic.

## Python pattern
~~~python
from typing import Protocol

class CustomerRepository(Protocol):
    def get(self, customer_id: str) -> "Customer | None": ...
    def save(self, customer: "Customer") -> None: ...

class RegisterCustomer:
    def __init__(self, customers: CustomerRepository) -> None:
        self.customers = customers

    def execute(self, customer: "Customer") -> None:
        customer.validate_invariants()
        self.customers.save(customer)
~~~

Use dependency injection at the composition root to bind infrastructure adapters to ports. Validate domain invariants in the domain, not in HTTP-only request parsing. Map between domain models, persistence models and transport DTOs explicitly.

## Anti-patterns and verification
Avoid "domain" classes that are ORM aliases, generic repository abstractions created preemptively, and remote calls hidden inside entities. Test business use cases against in-memory fakes; run adapter contract tests against actual SDK/database boundaries.

This improves portability but does not eliminate provider-specific behavior, data-format coupling or migration cost. Record deliberate tradeoffs.
