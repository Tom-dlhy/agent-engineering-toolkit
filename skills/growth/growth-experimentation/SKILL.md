---
name: growth-experimentation
domain: growth
version: "1.0.0"
description: >-
  Use when designing or evaluating acquisition, activation or conversion experiments, A/B tests, rollout hypotheses, guardrail metrics and event-based funnels. Do not use for mere landing page styling, arbitrary analytics SQL, generic unit tests or claiming statistical uplift without a valid experiment.
---

# Growth experimentation — decide before looking at results

## Experiment admission gate
1. State user problem, **intervention hypothesis**, observable behavioral outcome, target population, eligibility criteria, cost and potential harms. If intervention cannot be safely randomized, choose a clearly labeled observational alternative.
2. Audit the existing feature flag/experimentation and analytics stack first; reuse it rather than introducing another vendor/SDK. Verify installed version, event schema and permission/privacy practices.
3. Write primary metric **numerator/denominator/unit/window**, exposure event and assignment unit (user, organization, account, etc.). Coordinate the business meaning with `data/analytics-modeling` and instrument with the existing framework/provider. A CTA click is not a successful lead, payment or onboarding.
4. Predeclare control/treatment, randomization/stickiness, MDE or precision goal, power/sample horizon when appropriate, one primary outcome, guardrails and analysis method. Clustered accounts, seasonality, repeated visitors and network effects can invalidate naive independent-user assumptions.
5. Before interpretation check **sample ratio mismatch (SRM)**, missing/excluded exposures, duplicate events, assignment leakage, bots, consent effects and cross-variant contamination. No-positive-data does not imply no product impact.
6. Respect fixed-horizon tests or use a **pre-selected sequential-valid** method; repeatedly checking ordinary p-values and stopping at the first low value inflates false positives. Don't claim causal lift from a simple before/after.
7. Decide ship/iterate/stop with effect size and uncertainty, practical value, harms, cohort sensitivity, exposure quality and rollback plan. If sample is inadequate, report inconclusive rather than artificial significance.

## Deep branches
- [Hypothesis, randomization and metric contracts](references/hypothesis-randomization-and-metrics.md) — **read when** designing A/B assignment, identifying causal outcome and instrumenting exposures.
- [Analysis checks, SRM and decision quality](references/experiment-diagnostics-and-decisions.md) — **read when** interpreting real experiment results, checking SRM, peeking/false discovery or guardrails.
- [Consent-aware instrumentation and funnel evaluation](references/event-instrumentation-and-privacy.md) — **read when** implementing event schemas, consent-aware funnels and analytics QA via the installed provider.

## Ownership and guardrails
`design/landing-page-design` decides the page experience; this skill owns **test design and causal interpretation**. `data/analytics-modeling` owns mart/grain and metric definitions; `quality/test-strategy` owns software correctness; `lifecycle-retention` owns CRM send logic; `privacy/security` or legal reviewer owns lawful data collection. Do not quietly deploy experiments, change user cohorts, send messages or turn on tracking. Finish with a preregistered experiment plan or measured interpretation, testable event invariants, and evidence/uncertainty limits.
