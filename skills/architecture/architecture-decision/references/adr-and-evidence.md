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

## Falsifiable ADR and right-sized design handoff

**Read when:** architecture decisions impact multiple modules,
data ownership, deployment topology or long-lived interfaces.

### Decision framing

Write the problem, actual system constraints, hard/non-hard criteria,
workload that has been observed, status quo and credible alternatives.
Avoid implying that an unmeasured user count mandates microservices.
For complex topology compare consistency mode, tenant isolation,
network boundaries, release independence, observability, failure
recovery, operational cost, reversibility and skill needs.

### Evidence-led comparison

For each option state:
- invariant it guarantees and the mechanism that enforces it;
- failure mode introduced; who operates it;
- proof needed to distinguish from simpler alternative;
- rollback/transition effort and cost sensitivity;
- one measurable trigger for revisiting the choice.

Only score a weighted trade-off among options that pass hard
requirements. If an option violates mandatory data isolation, no
sum of lower latency and better maintainability should "win".

### Worked example

A small monolith has slow email notifications. Option A: keep module
and enqueue transactional outbox jobs. Option B: extract a separate
notification service. First measure how often notification blocks
request latency, and how deployment coupling hurts work. Verify
transaction/outbox recovery and duplicate delivery in a disposable
environment. Do not create a service and distributed trace system
unless evidence supports operational advantage.

### ADR output

Decision title / current SHA / affected modules / status quo /
alternatives / hard constraints / evidence and uncertainties /
chosen option / rejected reasons / invariants / negative tests /
producer-consumer interfaces / migration and rollback plan /
revisit trigger / owner approval.

Handoff concrete contracts to implementation-planning. The ADR
does not prove tests executed or authorize deployment. Deep designs
can include a diagram and test spike; for a local reversible rename
record the convention and skip ADR entirely.

Method inspiration:
https://github.com/github/awesome-copilot/tree/main/skills/agent-architecture
