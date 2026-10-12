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

## Progressive design-to-acceptance protocol

**Read when:** a vague feature idea needs a reviewed specification or a
multi-step handoff to implementation-planning.

### Priority: questions that change real behavior

Start from user-supplied facts and existing project decisions. Ask only
unknowns that alter interface semantics, actors, permissions, irreversible
effects, data retention, failure handling or visible behavior. Phrase
questions around real situations rather than "which framework?"
A trivial copy change with known intent needs no discovery ritual.

For a STANDARD feature, one short flow description plus the most
consequential normal and failure case is often enough. For DEEP,
include user roles, data boundary, lifecycle, external approvals,
rollout and recovery decisions. Mark inferred defaults as provisional.

### Acceptance table template

| Given | When | Then | Owner/Proof |
|---|---|---|---|
| Authorized actor and valid inputs | Requests the service | Defined artifact/state and response exist | API/browser test |
| Unauthorized actor | Accesses other tenant's ID | Denied and no sensitive response | Negative auth fixture |
| Remote service timed out after possible commit | Retries with same operation ID | No duplicated external effect | Fault injector |
| Required approval absent | Agent proposes irreversible action | Action stays a draft | Policy denial test |

Decisions ledger:
- FACT: observed/confirmed source; whether it came from user or repo.
- ASSUMPTION: reversible default and risk if wrong.
- DECISION: owner, accepted alternative, date or source reference.
- OPEN: the exact blocking issue and who can authorize it.
- OUT OF SCOPE: tempting adjacent features intentionally excluded.

### Example

"Automate support tickets" must distinguish drafting ticket text
from changing a production workflow state. The cheapest reversible
proposal is a draft with human confirmation, unless the owner already
approved a narrower privileged operation. Do not infer a permission
grant from an email or retrieved document.

At handoff, state the approved spec, acceptance and negative cases,
unresolved risks, external side-effect gates, and whether a separate
implementation plan is needed. Avoid further questioning once the
safe next action is clear.

Inspiration:
https://github.com/obra/superpowers/tree/main/skills/brainstorming
