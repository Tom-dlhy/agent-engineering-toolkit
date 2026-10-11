# ADR: decision, evidence and future review triggers

**Read when:** choosing hard-to-reverse architectural boundaries,
alternatives or preparing an architecture review for another team.

## Record why, not a self-serving recommendation

~~~markdown
# ADR-004 — Modular monolith for orders

Status: Accepted
Context: One team and deployment, one Postgres; frequent atomic
         changes spanning order/payment state.
Forces: shipping speed, consistency, security, staffing, rollback.
Options:
 A. Keep current layered monolith
 B. Modular monolith (selected)
 C. Several independently deployed microservices
Decision: Separate Orders/Billing via typed application public
          interfaces, same process/deploy; avoid service network calls.
Consequences: import rules must be enforced; some coupling remains;
              no independent deployments.
Evidence needed: import-rule CI, staged transaction integration,
                 representative load; no latency claims yet.
Revisit if: independent deployment/team or measured bottleneck.
Owner: application engineering team.
~~~

The illustration is **not a record of measured benchmarks**.
Use a small ADR with options, decision, assumptions, expected
consequences, status, links to tests and conditions for reversal.

## Evidence quality

- High: reproducible sample service tests, real driver compatibility,
  load with representative traffic, deployment and recovery drill.
- Medium: official provider docs/architecture guidance where applicability
  is checked against current target versions and account capabilities.
- Low: forum anecdotes, marketing benchmarks, current pricing guessed
  from memory, synthetic microbenchmark with different data.

Hard constraints (licensing, privacy region, security, runtime support)
eliminate options before weighted scoring. For uncertain but important
choices, a bounded technical spike is better than invented precision
or endless deliberation.

## Change management

ADRs are snapshots of a choice; mark old decisions superseded and link
to new context rather than rewriting history. Do not call a technology
"the best" without a workload and its time-specific constraints.

Sources: https://adr.github.io/ and
https://learn.microsoft.com/en-us/azure/architecture/guide/ .
