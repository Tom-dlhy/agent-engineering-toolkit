---
name: systematic-debugging
domain: core
version: "0.2.0"
description: >-
  Use when diagnosing unexplained failing tests, runtime exceptions, flaky behavior,
  regressions or production defects. Do not impose a full investigation for a known,
  isolated typo or claim an unobserved root cause is proven.
---

# Systematic debugging — evidence before repair

## Execution

1. **Describe** exact observed vs expected behavior, environment, revision, error and repeatability. Distinguish report, trace and hypothesis.
2. **Reproduce safely** with minimal test/fixture and controlled environment; never mutate customer data to reproduce.
3. **Localize** first violated invariant, inspecting recent diff and data flow across components, database, provider and worker.
4. **Falsify** one leading hypothesis with smallest disproof experiment. Controlled binary isolation, bisect and trace sampling beat shotgun edits.
5. **Fix the actual cause** at the owning boundary; avoid exception suppression, magical sleeps or retries without idempotency.
6. **Regress**: run red-then-green test and adjacent negative cases; inspect diff, report remaining uncertainty and escalate when security or data are at stake.

| Symptom | First action | Avoid |
|---|---|---|
| Deterministic failure | Focused test and first incorrect value | Changing several layers |
| Flaky test | Reproduce with seed, scheduling and shared resource checks | Declaring fixed after one retry |
| Production-only 503 | Safe traces, version/config comparison, staging replay | Speculative deploy |
| No reproduction | Record gap and add bounded safe instrumentation | Inventing a root cause |

## References

- [Reproduction and fault isolation](references/reproduction-and-isolation.md) — **read when** the failure spans layers or cannot be reliably reproduced.
- [Causal fix and regression checks](references/root-cause-and-regressions.md) — **read when** a candidate cause has been found or a fix needs proof.

`task-routing` selects workflow; `verification-before-done` audits completion; `performance-profiling` owns deep performance measurements. Domain skill explains specific API semantics.

## Completion

Observed symptom, confirmed or provisional cause, disproof experiment, fix,
regression result, untested scenarios and risk. Never fabricate tests or root cause.
