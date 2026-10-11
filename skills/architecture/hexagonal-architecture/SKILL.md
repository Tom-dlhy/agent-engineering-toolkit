---
name: hexagonal-architecture
domain: architecture
version: "0.1.0"
description: >-
  Use when isolating core business rules from HTTP frameworks, cloud providers, storage drivers or messaging libraries using ports and adapters. Do not use to wrap every basic utility in an interface.
---

# hexagonal-architecture

## Ports
Define use-case input/output and behavior-oriented interfaces at the application boundary. Ports should be expressed in domain vocabulary (e.g. `send_invoice`) rather than vendor SDK types (`put_object`).
## Adapters
Implement small concrete adapters for SQL, cloud SDKs, REST and queues. Convert transport/persistence DTOs at adapters. Wire dependencies at one composition root. Keep migrations and provider-specific error mapping here, not inside the domain.
## Tests
Domain/application tests use fakes implementing ports. Run adapter contract tests against representative real infrastructure; fake-only tests cannot prove network semantics.
## Decision gate
List which external systems are reasonably expected to change or need simulation. If a simple module achieves sufficient separation, prefer it over a complex architecture framework.
