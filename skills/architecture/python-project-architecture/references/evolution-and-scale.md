# Evolution: POC → production → growth

**Read when:** a prototype becomes a real service, load grows, reliability requirements change or someone proposes microservices prematurely.

## POC / MVP / production are risk profiles

| Prototype shortcut | Can be fine for | Production risk/remedy |
|---|---|---|
| In-memory list/state | Single-user demo | Multi-worker state divergence; use durable store |
| SQLite local file | Standalone/small constrained app | Write concurrency/multi-host constraints; evaluate Postgres |
| Local background task | Tiny best-effort notification | Worker crash/redeployment loses task; queue for durable jobs |
| One globally created HTTP client | App lifetime if managed | Leaks if never closed; concurrency/timeout budgets |
| Retry all errors | Never safe default | Repeat POST/payment/tool side effects |
| Store raw prompts/logs | Synthetic dev evaluation | PII, secrets, retention, provider-policy and access risks |
| No auth | Disposable isolated mock | Must define trust/tenant boundaries before exposure |

## Scale dimension checklist
1. **Reliability:** RTO/RPO, idempotent mutations, DLQ/replay, migration/rollback, failure injection.
2. **Data:** connection pools × workers, lock contention, query plans, N+1, transaction scope, read/write patterns.
3. **Compute:** CPU-bound vs network-bound, long tails, memory per worker, async pool, thread/task limits.
4. **Integration:** API rate/TPM limits, per-tenant quotas, provider failover policy and latency budget.
5. **Security:** roles/tenant filtering on every data path, secrets rotation, SSRF protections, safe logging.
6. **Operations:** SLOs, traces, dashboard/actionable alerts, versioned schema and incident runbook.

## Do not choose by raw users
100k registered users with rare actions may be easier than 100 concurrent LLM calls with 90s tails. Model peak requests/sec, latency distribution and fan-out; benchmark on representative workloads. Evaluate vertical scale first, then replicas/queues/caching when identified bottlenecks justify them.

## Safe modularization
Before splitting services: explicit bounded context, contract ownership, durable event/outbox semantics, monitoring on both ends, deployment independence and team/on-call. Moving database transactions across network creates dual-write and consistency problems.

## Rollout checklist
Canary/shadow where appropriate, schema backward/forward compatibility, data migration test, feature flags for behavioral release, rollback and replay of failed jobs, real access-control and load tests.

Useful resources: https://12factor.net/ and https://martinfowler.com/bliki/MonolithFirst.html .
