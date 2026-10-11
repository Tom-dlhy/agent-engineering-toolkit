---
name: performance-profiling
domain: quality
version: "0.1.0"
description: >-
  Use when diagnosing application performance, slow endpoints, frontend responsiveness or excess memory/CPU. Do not optimize without a measured bottleneck.
---

# performance-profiling

## Reproduce
Define representative load, device, dataset and baseline (p50/p95, throughput, CPU, memory, frontend interaction or bundle weight). Inspect traces/profiles, query plans and external call timing.
## Hypothesis
Pick a bottleneck and test a small change. Consider N+1 queries, overfetching, cold starts, serialization, blocking work, excessive client bundles and rerenders.
## Guardrail
Keep correctness, accessible behavior and security invariant while optimizing. Avoid trading away consistency for a synthetic benchmark.
## Evidence
Repeat measurement under comparable conditions, record gains and regressions, and add performance budgets or regression tests only when stable.
