# Total cost, exit risk, and executable technology spikes

Read when: choosing a complete stack from competing deployable options, estimating hosting cost, or proposing a technology migration.

## Cost of ownership is not a list of free tiers
Model active and idle compute, request bursts, storage/data growth, read/write operations, data transfer/egress, CI minutes, logs/traces, monitoring, backups/snapshots, authentication users/messages, paid UI license where relevant, support contracts and engineering incident time. Separate **provider price estimate** from **measured billing** and **human effort assumptions**.

~~~yaml
assumptions:
  month: explicit date, region, plan
  workload: requests, concurrency, payload bytes, job duration, DB writes
  ops: incidents, backup size, recovery drill
  labor: person-days to build, test, upgrade and monitor
per_option:
  direct_recurring_cost: estimate_or_observed
  onboarding_and_migration: bounded_estimate
  lock_in_exit_cost: documented_risk
  unknown_provider_limits: [quota, idle behavior]
~~~
Never invent current provider prices, free tier caps or fixed high traffic threshold; fetch official current sources at execution time. Consider free tiers as conditional pricing, not assured capacity.

## Highest-uncertainty proof
A small bounded spike should prove what might break: SSR+auth+DB edge adapter on actual runtime, concurrent updates and rollbacks on DB, third-party webhook idempotency, build size/latency in realistic region, and restore after an intentionally simulated failure. Measurements must state fixture, tool, region, tier and limitations. Synthetic microbenchmarks do not prove production capacity.

## Migration/rollback discipline
- Identify old/new source of truth, schema/data transforms, stable identifiers and object permissions.
- Validate backup restore **before** irreversible data moves.
- Stage dual-read or shadow verification only where realistic; dual writes create reconciliation complexity.
- Plan DNS/session cutover and rollback window with owner and reversibility; do not assume data rollback after live user writes.
- Keep explicit review triggers: p95 exceeds accepted SLO, ops cost rises above budget, provider deprecates adapter, accessibility regression or security finding.

## ADR short form
Decision/context; alternatives (including stay-put); hard constraints and expected outcomes; evidence URL/date; measured/assumed scores; total cost; rejected reasons; risks/owner; verification/rollback; revisit criterion. `architecture/architecture-decision` owns formal ADR template when cross-domain significance warrants it.

Sources: https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/ops_priorities_eval_tradeoffs.html and https://docs.cloud.google.com/architecture/framework and https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework
