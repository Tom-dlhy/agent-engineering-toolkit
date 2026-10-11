# Task maps and state transition contracts

Read when: modeling multi-step experiences, async state, authorization guards or a user flow before writing UI code.

## Compact state table
For each transition record **current state | event | guard | next state | feedback | recovery**. Model client presentation separately from authoritative server outcomes. A "loading" screen is not equivalent to a persisted business action.
```text
DRAFT      | submit | inputs valid           | SUBMITTING | disable duplicate submit | edit
DRAFT      | submit | invalid                | DRAFT      | field+summary errors      | edit
SUBMITTING | ok     | server confirms        | COMPLETE   | confirmation + reference  | return
SUBMITTING | fail   | retry allowed          | DRAFT      | actionable message        | retry
SUBMITTING | reject | permission revoked     | BLOCKED    | explain access limits     | leave/request access
```
Do not persist sensitive drafts without authorization; server must check permissions independently. Ensure idempotency for money/booking/one-time side effects, and separate optimistic presentation from confirmed success.

## Walkthrough
Start at entry route -> prerequisites -> primary action -> meaningful feedback -> exit. Test Tab/Escape/back/refresh/timeout, short/long content and component unmount. If a dialog is used, route exact focus/portal code to the installed provider and `accessibility-wcag`; flow ownership here is **the choice to confirm, cancel and return**, not the dialog API.

## Guardrails
Don't create a state machine library for a simple two-state form. For complex flows, the table may justify a typed reducer/statechart after inspecting existing architecture; no automatic dependency addition. Distinguish permitted cancellation of UI loading from actual cancellation of server work.

Official interaction baseline: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ and https://design-system.service.gov.uk/patterns/
