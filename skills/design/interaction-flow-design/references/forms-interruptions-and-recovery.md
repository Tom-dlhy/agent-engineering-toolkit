# Form steps, interruption and user recovery

Read when: designing a wizard, onboarding sequence, confirmation, unsaved changes flow, timeout or resumable draft behavior.

## Choose steps by real dependencies
Keep one page when content fits and users benefit from overview. Use a wizard when sequencing reduces cognitive load or certain information is conditionally required, not just to create engagement. Show progress as **meaningful phases**, not invented percent completion. Provide back/skip when semantics permit and announce conditional step changes.

## Persistence and rollback
Specify whether drafts persist on client, server or not at all; consent, expiry, privacy and concurrency are product decisions. Revalidate on submission; never treat a disabled client button as authorization. Avoid duplicate side-effect requests with user feedback and backend idempotency where needed. A payment being pending is not "completed".

Example synthetic multi-step onboarding:
```text
Start -> identity -> preferences -> review -> submit
  identity invalid -> inline correction
  lost network -> keep safe local inputs, retry without duplication
  token expired -> re-authenticate, restore permitted state
  user cancels -> confirm only if meaningful irreversible loss
```
Check focus after navigating steps, error summary location, browser back, deep links, screen-reader headings and zoom. Reuse existing Form/Dialog/Progress APIs; do not implement a custom focus trap when provider owns one.

## Acceptance
Happy route, one incorrect value, server conflict, unavailable service, back to earlier step and resumability policy. Mark test participant findings separately from developer simulations.

References: https://design-system.service.gov.uk/patterns/ and https://www.w3.org/WAI/tutorials/forms/
