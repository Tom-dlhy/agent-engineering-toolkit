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

## Architecture selection as a falsifiable decision, not fashion

Draw on the distinction between discovery, architecture and implementation
in GitHub's agent-architecture guidance and the explicit design-to-plan
handoff from Superpowers.

| Mode | Design process | Artifact |
|---|---|---|
| LIGHT | No ADR for local reversible code style choice | Existing convention and one direct reason |
| STANDARD | Compare status quo with a credible alternative for important interfaces | Short ADR, constraints, trade-offs and testable spike |
| DEEP | Evaluate consistency, security, scale, failure/recovery and migration | ADR with evidence, failure model, transition plan and revisit trigger |

**Sequence:**
1. Discover actual nonfunctional expectations, topology, existing modules,
   consumers, latency budgets and ownership. Distinguish hard constraints
   from preferences and unverified volume estimates.
2. Map 2-3 credible designs **including the status quo**. Record each
   one's operational cost, coupling, observability, reversibility, data
   consistency, security and migration consequences. Do not choose
   a framework because of popularity alone.
3. Identify the *one unknown* that could reverse the decision; resolve
   cheaply by bounded spike, performance measurement, contract test,
   failure rehearsal or API proof before building abstractions.
4. Choose the simplest viable option satisfying hard gates; document
   why alternatives were rejected and which new evidence would trigger
   reconsideration.
5. Hand exact produced interfaces to implementation-planning and executor.
   ADR approval does not authorize production migration.

**Example:** deciding whether to extract notifications from a monolith.
Prefer module boundary + asynchronous outbox only if observed operational
needs justify it; a microservice introduces network failure, deployment and
eventual consistency. Run contract and recovery tests before deciding.
"Microservices scale better" is not a falsifiable local requirement.

If two reviewers disagree, ask what metric/input would change the decision,
not which diagram looks cleaner. Architecture decisions are contextual, not
permanent mandates.
