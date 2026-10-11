# Experiment quality gates: SRM, early peeking and rollout decisions

Read when: reading A/B outcome reports, debugging sample ratio mismatch or deciding whether observed growth supports shipping a variant.

## Integrity before uplift
1. Confirm assignment unit, exposure trigger, dedupe logic, valid cohorts, time windows and event-to-outcome mapping.
2. Check **sample ratio mismatch** against expected allocation. SRM can indicate broken bucketing, excluded traffic, duplicate events, consent-related missingness or logging errors; investigate before interpreting treatment.
3. Check carryover/contamination, account clustering, delayed conversion, differential loss to follow-up, variant interaction and bot activity.
4. Use the preregistered primary outcome and guardrails; don't replace the metric with a nicer after-the-fact segment.
5. Report absolute/relative effect, units, interval/uncertainty, valid population and guardrail harms.

## Peeking and multiplicity
Traditional fixed-horizon tests are analyzed at planned endpoints. Peeking repeatedly and stopping at the first nominally small p-value increases false positives. When repeated monitoring is operationally required, choose a **sequential-valid design and framework configuration in advance**. Multiple variants/outcomes and post-hoc segmented looks need exploratory labels or multiplicity control; a significant p-value is not a guarantee of financial benefit.

## Illustrative fixture, not proof
~~~text
Control:   100 confirmed inquiries / 2000 eligible visitors = 5.0%
Treatment: 110 confirmed inquiries / 2000 eligible visitors = 5.5%
Point difference: +0.5 percentage points, +10% relative
~~~
These synthetic point estimates do **not** establish significance, causality if assignment corrupted, retained customer value or safe rollout. If treatment damages lead quality or accessibility, a numeric gain may be undesirable.

## Decision record
~~~text
Experiment ID and preregistered hypothesis:
Run dates, eligible population, assignment and exposure:
SRM result and instrumentation defects:
Primary estimate + uncertainty, planned analysis method:
Guardrails and harmed segments:
SHIP / ITERATE / STOP / INCONCLUSIVE:
Owner, next action, rollback and evidence gaps:
~~~
If no reliable baseline, no sufficient sample, or invalid exposure denominator exists, mark INCONCLUSIVE. Do not turn before/after page analytics into randomized evidence.

Official: https://docs.statsig.com/experiments/advanced-setup/sequential-testing and https://docs.statsig.com/experiments/interpreting-results/read-results
