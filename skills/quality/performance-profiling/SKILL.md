---
name: performance-profiling
domain: quality
version: "0.2.0"
description: >-
  Use when diagnosing measured latency, throughput, memory, CPU, event-loop,
  frontend responsiveness, database or network performance bottlenecks.
  Do not optimize speculative hot spots or substitute microbenchmarks for
  realistic end-to-end workload tests.
---

# Performance profiling — measurement before optimization

## Workload-first plan
1. Define user task and service objective: throughput, p50/p95/p99 latency,
   error rate, saturation, CPU/RSS/heap, bandwidth or mobile interaction.
   Fix environment, dataset, concurrency and representative request sizes.
2. Collect a baseline with telemetry including error/timeout/queue time;
   measure **completed** traffic, not only offered load.
3. Decompose critical path using tracing and suitable profilers: HTTP/DB,
   serialization, CPU, memory growth, client bundle/render, network waits.
4. Form a falsifiable bottleneck hypothesis and make the smallest correct
   change. Compare before/after under matched load with warmup and repetitions.
5. Verify correctness, accessibility, isolation/security and tail latency;
   no wins from dropping expensive requests or hiding errors.
6. Define performance regression budget only when stable, measurable and
   relevant to actual SLO. Record uncertainty and cost tradeoffs.

## Selection table
| Signal | Start with | Caveat |
|---|---|---|
| Slow Python CPU | cProfile/py-spy and traces | Sampling/observer overhead |
| Growing Python memory | tracemalloc for Python allocations, RSS | Native extensions not fully covered |
| API p99 increase | Span time, pool waits, queue age | Mean hides tail |
| DB slow | Query count, explain plan, lock contention | More workers can overload DB |
| Browser interaction | Browser trace, Web Vitals | Synthetic desktop isn't field/mobile |
| Capacity under bursts | k6/Locust staged scenarios | No unauthorized production load |

## Targeted references
- [Profilers and end-to-end decomposition](references/profilers-and-diagnostics.md) —
  **read when** localizing CPU, allocations, N+1, event-loop lag or frontend cost.
- [Load tests, SLO thresholds and reproducibility](references/load-testing-and-slos.md) —
  **read when** benchmarking throughput, concurrency, tail latency,
  saturation or defining regression thresholds.
- [Optimization decisions and validation](references/optimization-and-tradeoffs.md) —
  **read when** comparing cache, pool, batch, query, worker or code-level changes.

## Exit
Baseline, bottleneck evidence, intervention, controlled new measurement,
functional regression checks, limits, untested environments and rollback
plan where needed. Core systematic-debugging establishes failure cause;
observability-sre owns monitoring and incident alerts.
