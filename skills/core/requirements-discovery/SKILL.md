---
name: requirements-discovery
domain: core
version: "2.0.0"
description: >-
  Use when the user explicitly wants to clarify, pressure-test or scope an ambiguous product idea, feature or software specification before implementation. Do not interrogate users for routine well-specified edits or block urgent safe execution.
---

# requirements-discovery

## Role and boundaries
A short, opt-in requirements interview and adversarial clarification method. It is **not** architecture-decision (selecting technology), task-routing (selecting skills) or project management. Mode LIGHT: state assumptions and act. STANDARD: resolve critical unknowns in a concise exchange. DEEP: map roles, invariants, misuse, operations and acceptance scenarios. Never turn a simple request into a compulsory questionnaire.

## Routing decisions
1. Read the request and existing specification/repo context before asking anything. Separate stated facts, inferences and truly unknown decisions.
2. If implementation is already feasible and user asked for execution, proceed with explicitly labeled safe assumptions; do not demand a grill session.
3. If the user requested /grill-me, wants a product spec or a key decision could materially change the solution, enter discovery mode: ask a small ordered set of high-information questions, one at a time unless batching is expressly useful.
4. Challenge assumptions constructively: who has this problem, why now, how success is measured, what can go wrong, how to handle exceptional states, what is outside scope.
5. Stop when remaining questions have low decision impact. Produce a compact spec with open decisions and acceptance tests; do not invent agreement or claim user signoff.

## Selective expertise
- [Problem framing and question priority](references/problem-framing.md) — **read when** the idea, target user or scope is ambiguous, or competing assumptions need pressure-testing.
- [Acceptance examples and decision log](references/acceptance-and-decision-log.md) — **read when** translating an interview into an implementation-ready specification, risk register or handoff.

## Definition of done
State confirmed facts vs assumptions, scope/non-goals, two or more concrete acceptance examples where warranted, risks and unresolved blockers. Avoid aggressive or shaming tone. Never replace explicit user constraints with your own product preference.
