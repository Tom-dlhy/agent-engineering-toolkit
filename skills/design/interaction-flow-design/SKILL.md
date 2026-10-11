---
name: interaction-flow-design
domain: design
version: "1.0.0"
description: >-
  Use when designing an end-to-end user task flow, onboarding journey, multi-step form, error recovery, permission gate or interactive state machine before implementation. Do not use for simple animation timing, component API debugging or auditing an already implemented screen without flow design.
---

# Interaction flow design — make the task complete and recoverable

## Define the journey
1. Inspect real brief, actors, device, entry points, existing navigation and business invariants. Use `core/requirements-discovery` only for genuinely blocking missing requirements.
2. Define the user outcome, preconditions, happy path, alternate routes, irreversible actions, permissions, cancellations and resumability. Distinguish interface state from backend/business state.
3. Build the smallest useful task/state map: event, current state, guard, outcome, feedback, next state. Account for loading, retry, stale data, expired sessions, validation and conflicting requests.
4. Choose single-page vs wizard vs progressive disclosure based on cognitive load and validation dependencies. Provide a path backwards where safe; do not reset successfully completed work without reason.
5. Specify focus and keyboard changes, status/error announcements, prevention of duplicate action, cancellation of pending requests and graceful handoff across devices where relevant.
6. Reuse installed router, form, dialog, state and component primitives. This skill **designs behavior**, while `ui/<provider>` and `frontend/<framework>` own real implementation APIs.
7. Verify task completion with scenarios: success, invalid inputs, permission denial, offline/timeout, back/refresh/resume and interruptions. Separate simulated walkthroughs from actual observed usability tests.

## Deep branches
- [Task maps and guarded transition contracts](references/flow-state-contracts.md) — **read when** defining steps, states, guards, async transitions and cancellations.
- [Complex forms, interruptions and recovery](references/forms-interruptions-and-recovery.md) — **read when** designing wizards, optimistic confirmations, resumable drafts or failure recovery.
- [Flow validation and measurable acceptance](references/flow-evaluation.md) — **read when** preparing task-based scenarios, evaluating alternate paths or handing off to engineering.

## Boundaries
`information-architecture` owns navigation/taxonomy/findability across destinations. `interaction-motion` owns animations. `ux-audit` audits observable implementations. `accessibility-wcag` maps normative criteria. `frontend-design` owns visual expression. Never replace a provider's form/dialog with custom primitives just to represent a flow.

## Output
A legible flow with guards, states, error/recovery routes, component handoffs and observable completion criteria; report unverified assumptions.
