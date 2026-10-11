# Product content QA and outcome evidence

Read when: auditing UI language, planning copy experiments or verifying wording after implementation.

## Verify in real context
Compare text in the complete journey, not isolated spreadsheet cells. Assess: Does the user know what this is? Why is it needed? What happens if I act? How to recover? Does a status truthfully reflect backend state? Are links/buttons distinguishable without jargon?

```yaml
id: payment-save-error
trigger: server request failed before confirmed save
copy: "We couldn't save this payment method. Try again."
expected_action: retry (only when duplicate attempt is safe)
implementation_owner: selected UI provider's alert/form primitives
manual_review: product + legal reviewer when needed
observed_with_users: false
```
This synthetic example requires a real safe-retry contract before use in production.

## Evaluation without vanity metrics
For review ask a representative participant to predict the result of an action, find a recovery step, or complete the relevant task. Record participants, variant, task and completion definition. A preference poll ("which sounds nicer") is not equivalent to observed task understanding. If no test was conducted, label changes as hypothesis and run targeted review.

## Handoff and non-goals
`ux-audit` logs existing user-impact failures; `interaction-flow-design` owns task sequencing; `frontend-design` owns visual hierarchy; `growth/content-strategy` owns editorial programs. The copy skill does not publish marketing content, install analytics tooling or invent uplift.

Sources: https://design-system.service.gov.uk/components/error-message/ and https://www.w3.org/WAI/test-evaluate/
