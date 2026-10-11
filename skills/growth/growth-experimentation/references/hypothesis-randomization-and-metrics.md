# Hypotheses, randomization units and primary metric contracts

Read when: designing a controlled conversion/activation test or examining variant assignment before a growth rollout.

## Register choices before exposure
~~~yaml
question: Does clearer pricing help visitors finish inquiries?
hypothesis: Treatment reduces abandoned inquiries
population: eligible visitors to approved public route
control: current truthful explanation
treatment: approved clearer explanation
assignment_unit: stable eligible visitor subject to lawful identity use
allocation: {control: 0.5, treatment: 0.5}
primary_metric:
  outcome: inquiry_confirmed
  numerator: assigned eligible visitors with server-confirmed inquiry
  denominator: assigned eligible visitors within declared 7-day window
guardrail: submit_error_rate
minimum_detectable_effect: to-be-estimated from authorized baseline
power_and_method: declared before test
~~~
This fixture is **illustrative**, not a recommendation to deploy identifiers without lawful consent. A client CTA click is not a server-confirmed lead. A thousand repeated clicks from one user are not independent exposure units.

## Assignment invariants
- Assign before outcome; maintain stable variant for permitted user/account scope across reloads.
- Expose only when variant actually rendered; log exposure/assignment independently to detect missing visibility.
- Identify shared-account or social interactions: user-level randomization may be invalid with interference.
- Record filtering and bucketing IDs while minimizing personal information and protecting identifiers.
- Prevent crossovers and track when users move from anonymous to authenticated states; avoid silently re-randomizing.
- Coordinate existing feature flags and analytics; this skill does not install a new provider SDK.

## Traffic and power
Define baseline conversion rate, absolute vs relative MDE, acceptable false-positive risk, intended statistical power, feasible population and test window. When unavailable, don't invent sample sizes or announce a power calculation. For tiny samples, prefer descriptive/qualitative evidence and a staged rollout without causal uplift claims.

## Fail-safe
Experiment conflicts with existing provider-flag rules or legal consent? Defer release or narrow scope. Unexpected severe guardrail deterioration? Rollback via authorized release mechanism. This is test planning, not permission to deploy.

Official: https://docs.statsig.com/experiments/advanced-setup/sequential-testing and https://developers.google.com/analytics/devguides/collection/ga4/reference/recommended-events
