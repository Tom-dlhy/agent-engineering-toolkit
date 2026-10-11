---
name: architecture-decision
domain: architecture
version: "0.1.0"
description: >-
  Use when choosing architecture, a framework, service, database, component boundary or significant technical tradeoff. Do not use for reversible styling or trivial implementation choices.
---

# architecture-decision

## Decision workflow
1. State the actual problem, requirements, constraints and success criteria. Identify assumptions that need testing.
2. Propose at least two credible alternatives, including a simpler option and status quo when valid.
3. Compare maintainability, latency, security, team familiarity, operational cost, scale, lock-in and reversibility.
4. Select one option. Explain why others were rejected and what would change the decision.
5. Record an ADR with context, decision, consequences, migration path and review date or trigger.

## Portability
Differentiate business logic from infrastructure. Avoid creating abstraction layers around every provider without evidence that migration or independent tests matter. Provider-native services can be the right tradeoff.

## Done when
The decision is reviewable without re-reading the entire conversation, and constraints and risks are explicit.
