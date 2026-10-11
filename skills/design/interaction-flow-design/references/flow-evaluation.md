# Flow evaluation and acceptance evidence

Read when: converting a designed interaction flow into implementation acceptance cases, prototype walkthroughs or user-testing scenarios.

## Acceptance fixture
```yaml
user_job: Submit an application
entry: authenticated form start
happy: valid data -> review -> submit -> confirmed receipt
negative:
  - invalid required field -> explained correction
  - session expires -> safe reauthentication/recovery
  - network timeout -> clear retry without duplicating action
safety:
  - permissions validated on server
  - user not told success before confirmation
accessible:
  - headings and focus reveal new step
  - error correction keyboard usable
observed_in_browser: false
```
Specify expected user-observable outcomes, not merely component render tests. Instrument completion, error recovery and abandonment only when analytics have appropriate consent and observable event definitions. A unit test that proves state transitions does not establish that users understand the flow.

## Handoffs and non-goals
- Navigation between *product destinations*: `information-architecture`.
- Backend side effects and invariants: architecture/backend/security skills.
- Provider-specific Form/Stepper/Dialog: existing UI skill.
- Animation timing and transitions: `interaction-motion`.
- Review of implemented problems: `ux-audit`.

## Validation method
Run role-based walkthrough on realistic fixtures, then actual browser keyboard flows and representative user tests where possible. Document nonobserved scenarios separately. Minimize prompting burden for simple changes: a new text label does not need an entire state machine review.

References: https://www.w3.org/WAI/tutorials/forms/ and https://design-system.service.gov.uk/patterns/
