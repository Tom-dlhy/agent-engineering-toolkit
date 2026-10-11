# Requirements discovery — testable handoff and decision register

**Read when:** writing a usable mini-spec, defining acceptance tests or recording unresolved architecture questions after discovery.

## Output contract
Produce a concise, reviewable artifact:
- **Problem / outcome:** observable behavior, not "make it modern".
- **Actors and trust:** authenticating role, privileges and forbidden operations.
- **Primary path:** triggering input → validation → processing → durable output.
- **Exceptions:** incomplete input, duplicates, conflict, third-party failure, timeout, denied access, retries and cancellation.
- **Non-goals:** explicit boundaries protecting scope and context.
- **Success signal:** what and how to measure, where actual data will come from.
- **Decisions:** resolved option, rejected alternatives, rationale and owner of pending choices.

## Acceptance example format
Given [state + actor + authorizations], when [specific action/input], then [observable response plus durable side effects], and [negative assertions].
Example:
Given a support ticket with no customer ID, when auto-triage runs, then it leaves ownership unchanged, sets "needs review" and records the reason without sending a customer notification.
Given the same ticket is retried, when the idempotency key is reused, then the log records a replay and the workflow does not create a second external side effect.

Avoid tests that merely check "LLM responds well". For probabilistic components, separate deterministic guarantees (schema, permissions, audit) from evaluated quality thresholds (e.g. class recall) defined from a representative dataset.

## Decision log
| ID | Question | Options | Impact | State | Owner |
|----|----------|---------|--------|-------|-------|
| D1 | Send output automatically? | Human review / auto-send under policy | External side effects | Open | Product owner |
| D2 | Where keep audit record? | Existing DB / central log | Compliance and tracing | Provisional | Engineering |

No fabricated approvals; distinguish "proposed" from "validated".

## Recommended implementation handoff
1. Map components/data contracts only after requirements are coherent.
2. Plan vertical slices with one complete user path per increment.
3. Generate tests for permissions, validation, failure, duplicate/replay and rollback.
4. Link open decisions to tasks; do not silently make irreversible choices.
5. If user explicitly wants an implementation instead of a spec, provide the smallest executable next step, not a mandatory documentation ritual.

Official background: https://www.atlassian.com/agile/project-management/user-stories and https://cucumber.io/docs/gherkin/reference/ .
