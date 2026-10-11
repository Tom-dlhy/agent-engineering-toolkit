---
name: architecture-decision
domain: architecture
version: "0.2.0"
description: >-
  Use when deciding a significant software architecture style, service boundary,
  persistence strategy or hard-to-reverse technical design under explicit
  requirements and competing options. Do not write an ADR for a trivial reversible edit.
---

# Architecture decisions — trade-offs with falsifiable assumptions

## Decisions in sequence
1. Characterize the problem and forces: business workflow, correctness,
   privacy, team ownership, expected change, SLO/latency, cost, data
   consistency, region, deployment/rollback and existing architecture.
2. Separate **hard constraints** from weighted preferences and assumptions.
   Determine what can be learned cheaply by spike/benchmark versus guesswork.
3. Consider status quo/simplest viable design and at least one credible
   alternative. Compare options with traceable evidence and failure modes.
4. Reject premature complexity: microservices for a tiny team, CQRS
   for one CRUD, abstract repositories that add no testable boundary.
   Patterns are options with costs, not quality badges.
5. Record ADR: problem/context, chosen option, explicit rejected alternatives,
   consequences and measurable revisit triggers. An ADR captures why a
   decision made sense *then*, not immutable law.
6. Verify the highest-impact unknown with representative workloads,
   executable tests or a bounded technical spike before high-risk commitment.
7. Route implementation to the concrete specialist without copying its
   domain implementation guide into this ADR skill.

## Targeted references
- [Architecture decision record and evidence](references/adr-and-evidence.md) —
  **read when** creating ADRs, comparing alternatives or making
  assumptions testable.
- [Style selection and distributed-system trade-offs](references/style-selection-and-tradeoffs.md)
  — **read when** weighing layered, modular monolith, microservices,
  web-queue-worker or event-driven style.
- [Architectural quality attributes and validation](references/quality-attributes-and-fitness.md)
  — **read when** mapping security, reliability, latency, scaling,
  recovery or evolution into measurable architecture checks.

## Boundaries
technology-tradeoffs owns **concrete products/libraries** and weighted
evidence, while architecture-decision captures the consequential systemic
decision. python-project-architecture owns Python-specific project layout.
Do not invent throughput or cost forecasts from user counts.

## Exit
Decision, context, assumptions, measured unknowns, rejected choices,
reversibility, migration plan, consequences, and an explicit review trigger.
