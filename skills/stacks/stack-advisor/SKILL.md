---
name: stack-advisor
domain: stacks
version: "2.0.0"
description: >-
  Use when selecting or revising an end-to-end web/SaaS/API/data application technology stack with explicit constraints and connected architecture decisions. Do not use to replace an already suitable mandated stack, implement one framework's APIs or compare a single database/UI/cloud provider in isolation.
---

# Stack advisor — fit the system, not a fashionable inventory

## Decision gates
1. **Inspect first:** existing manifests/lockfiles, target framework versions, architecture, deployed infrastructure, team fluency and migration commitments. A working existing stack is the baseline; user-fixed constraints are not invitations to redesign.
2. Define jobs and measurable hard requirements: public SEO/SSR, stateful sessions, realtime/async work, database invariants, traffic/load shape (not just user counts), geography, regulatory/data classification, budget, ownership, operating capacity and restore objectives.
3. Identify **knock-out constraints** before weighted preferences: runtime incompatibility, prohibited residency, unavailable region, unsupported transactions, unacceptable auth model, team cannot operate it, license or vendor prohibitions. Never average a hard failure into a high overall score.
4. Compare **stay with current/minimum viable**, one genuinely credible alternative, and optional more complex variant only when justified. Don't fabricate fake precision in TCO, prices, benchmark throughput, popularity or rankings.
5. Check **interfaces between selected parts**, not a bag of individually popular packages: rendering/deployment runtime vs DB driver/socket, ORM migrations vs pooler, auth cookie/session vs edge/SSR, storage and signed URL semantics, queues and idempotency, CI/build output and observability.
6. Rank by declared priorities, evidence/confidence and reversibility. Record total cost at realistic workload assumptions (compute idle/burst, DB, egress, storage, observability, licenses, vendor support, migrations). Include development and operation labor.
7. Choose smallest sufficient coherent architecture. Demonstrate one **representative vertical slice** (login if needed → server authorization → write/transaction → background/asset → deploy → health/restore), run measurements or label the gap. Follow quality/release gates before production.
8. Record concise ADR: chosen stack, disqualifiers, rejected viable option(s), migration/rollback, assumptions and **revisit triggers**. Never change dependencies or infrastructure as an incidental result of recommending.

## Select only relevant deep expertise
- [Product constraints, knockout filters and weighted choices](references/requirements-and-decision-matrix.md) — **read when** comparing complete stack candidates and recording confidence/weights.
- [Cross-layer runtime, identity, data and deployment compatibility](references/cross-layer-compatibility.md) — **read when** integrating SSR/edge/serverless, database adapters, ORM, auth and cloud platform.
- [TCO, evolution, migration and executable proof](references/total-cost-migration-and-spikes.md) — **read when** making lifecycle cost claims, proposing migrations, designing a bounded spike or documenting ADR triggers.

## Routing ownership
`database-selection` owns the *data-store choice*; `ui-library-selection` the *UI kit*; `authentication-solution-selection` the *end-user authentication approach*; `cloud/cloud-provider-selection` the *cloud workload/provider fit*. `architecture/technology-tradeoffs` owns generic library/product comparison evidence and `architecture/architecture-decision` owns broader architectural style/ADR. After decisions, **activate only the selected** frontend/UI/cloud/backend skills, not every candidate.

## Stop condition
The recommendation is not the implementation. Provide dated evidence, assumptions vs measured claims, a viable fallback, testable acceptance and explicit authorization boundary. LIGHT requests need a focused answer; DEEP applies only with irreversible/security/production concerns.
