# Optimization choices and regressions

**Read when:** selecting performance interventions after finding a measurable
limiting resource and evaluating what tradeoffs are justified.

| Proposal | Use when | Risks |
|---|---|---|
| SQL index | Frequently filtered selective query | Write overhead, lock/migration cost |
| Eager load/fix N+1 | Repeated DB trips dominate | Extra memory/large join |
| Connection reuse | Repeated network calls | Pool saturation, lifecycle leakage |
| Cache | Stable read, clear invalidation | Stale data and cross-tenant exposure |
| Batching | Supported upstream and amortized overhead | Head-of-line blocking, partial errors |
| Async I/O | True async, many concurrent calls | Blocking SDK, runaway tasks |
| More workers | CPU/resources independently scalable | DB, LLM quotas, RAM multiplication |
| Streaming | First-result latency matters | Disconnect, incomplete JSON, proxy buffering |
| Frontend splitting | Unused JS delays interaction | More chunks and network waterfall |

## Make a controlled change

1. Baseline version, scope and SLO.
2. Hypothesis: "90% p99 is outbound provider, not Python JSON formatting".
3. Implement smallest relevant fix with limit/invariant checks.
4. Repeat same workload and track useful completions, p95/p99, error,
   cost, CPU/memory and downstream saturation.
5. Test correctness, security isolation, cache invalidation, cancellation
   and failure/overload paths before retaining optimization.
6. Revert if gains are not reproducible or a serious regression occurs.

Amdahl's law reminds us that accelerating a tiny local operation rarely
fixes an end-to-end latency dominated by another stage. Adding Redis
because there are "lots of users" is not an evidence-based diagnosis.

Official: https://docs.python.org/3/library/profile.html ,
https://www.python-httpx.org/advanced/resource-limits/ ,
https://grafana.com/docs/k6/latest/using-k6/thresholds/ .
