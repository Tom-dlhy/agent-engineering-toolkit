---
name: technology-tradeoffs
domain: architecture
version: "0.2.0"
description: >-
  Use when comparing concrete libraries, frameworks, databases, cloud services
  or build-versus-buy options against cost, maintainability, operations and
  compatibility constraints. Do not treat popularity, benchmark snippets
  or a preferred stack as objective proof.
---

# Technology trade-offs — independent evidence over hype

## Evaluation workflow
1. Capture target runtime/environment, stakeholders, hard constraints,
   data classification/residency, license and existing stack.
2. Describe **specific use case and load shape**, not bare "number of users".
   Evaluate engineering effort, failure/recovery, observability and owner.
3. Compare stay-with-existing/buy/build and at least one practical
   alternative; isolate knock-out constraints from weighted preferences.
4. Verify current versions/API/toolchain compatibility, security advisories,
   license/maintenance status and cloud regional availability from **official
   docs or actual code**. Use Stack Overflow for reproducible edge cases,
   never as sole current authority.
5. Run a *timeboxed proof* on highest uncertainty: actual deployment,
   representative query, SDK integration, test and lifecycle complexity;
   avoid incomparable vendor benchmark claims.
6. Show total cost of ownership: build vs runtime bills, egress,
   support, skills, vendor lock-in and migration complexity. Do not
   hallucinate current pricing, scale thresholds or feature entitlements.
7. Recommend default and second-best with disqualifiers, evidence
   dates, rollback/switch triggers and residual uncertainties.

## Targeted references
- [Comparison matrix and evidence quality](references/selection-matrix-and-evidence.md)
  — **read when** evaluating two or more technologies, weightings,
  missing information and conflicts of interest.
- [Proof-of-concept and benchmark methodology](references/spikes-benchmarks-and-tco.md)
  — **read when** designing a trial, cost model or capacity
  comparison with actual data.
- [Portability, lock-in and migration](references/lock-in-and-reversibility.md)
  — **read when** choosing a managed provider, evaluating
  multi-cloud abstractions or exit plans.

## Boundaries
architecture-decision records broader system decisions;
stack-advisor offers a high-level initial stack recommendation;
database-selection owns concrete data-store fit; ui-library-selection
owns UI component library tradeoffs.

## Exit
Criteria, dated sources, measured vs assumed claims, alternatives,
TCO, migration/reversal conditions and recommendation scope recorded.
