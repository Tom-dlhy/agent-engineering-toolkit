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

## Four-phase causal process, scaled to actual failure

Based on the root-cause discipline of obra/superpowers, while respecting task-routing: a known typo does not need production-incident ceremony.

| Workflow | Method | Required proof |
|---|---|---|
| LIGHT | Reproduce known local defect and inspect first wrong value | Focused regression/direct observable check |
| STANDARD | Observe, isolate boundary, falsify hypothesis, repair, RED/GREEN | Evidence of first violated invariant plus nearby regression |
| DEEP | Trace across processes, git history, retries, concurrency, fault/replay paths | Correlated trace and recovery/invariant proof |

**Phase 1 — observe:** read the *entire* error and first causal frame; record request, input, expected and actual, environment and revision. A report is not reproduction. Establish whether failure is deterministic or intermittent.

**Phase 2 — isolate:** follow input -> transport -> validation -> domain -> persistence/provider -> output. For each boundary compare observed input/output until the first incorrect value. Check recent changes and known-good configurations. Do not change several layers simultaneously.

**Phase 3 — experiment:** state the leading hypothesis and an observation that would falsify it. Use a minimal disposable fixture, bisect, trace or controlled schedule. For intermittent cases preserve seed, timing, parallel test workers and shared state. Sleeping or rerunning until green does not prove a race fixed.

**Phase 4 — causal fix:** where possible make a meaningful behavioral test fail on old code for the intended assertion, then pass on the smallest fix. Run adjacent error and integration checks. For remote side effects, distinguish timeout from failed commit and check idempotency/reconciliation. If the failure remains unreproduced, provide a bounded instrumentation plan and uncertainty rather than a false conclusion.

Example: duplicate invoices after provider timeout. Wrong fix: retry earlier. Probe whether the provider committed before client timeout; simulate a remote commit followed by transport loss; require exactly one invoice after retry, and do not replay real payments in production.

Exit with observed symptom, causal boundary, disproved hypotheses, revision, real test commands and NOT RUN conditions.
