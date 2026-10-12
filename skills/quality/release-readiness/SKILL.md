---
name: release-readiness
domain: quality
version: "0.2.0"
description: >-
  Use when evaluating a production release candidate, migration, high-impact
  launch, cutover or rollback plan against operational and security evidence.
  Do not force a release committee for docs-only changes or deploy based on
  a green CI status alone.
---

# Release readiness — artifact identity, go/no-go and recovery

## Release decision
1. Identify **exact** source SHA, built artifact digest, environment/region,
   consumers, compatibility constraints and ownership. Do not interchange
   testing on PR head with deployment of a rebuilt artifact.
2. Establish user acceptance evidence, API/data schema compatibility,
   security/supply-chain review, auth/secrets, capacity and observability.
3. Plan migrations, backups, forward-only/rollback limitations, data repair
   and dependent service/feature flags. Code rollback cannot always
   reverse customer-visible actions or destructive schema/data changes.
4. Run authorized staging/preview smoke, negative behavior and
   integration tests relevant to risk; record failed, skipped or blocked.
5. Choose deployment mode (simple, canary, rolling, blue/green) for the
   actual platform and SLO; define stop triggers and on-call/communications.
6. Decide GO, CONDITIONAL GO or NO-GO with evidence and explicit
   outstanding blockers. Do **not** merge/deploy without user authorization.

## Targeted references
- [Release gates, provenance and approval](references/release-gates-and-evidence.md) —
  **read when** preparing a release checklist, linking CI to artifact
  identity, required approvals or assessing operational readiness.
- [Migration, rollback and data safety](references/migrations-and-recovery.md) —
  **read when** changing schema, persistent state, integrations,
  secrets or designing rollback/roll-forward.
- [Progressive delivery and post-release checks](references/progressive-rollout-and-operations.md) —
  **read when** planning canary/rolling/blue-green, monitoring,
  traffic cutover or incident response.

## Boundary
verification-before-done assesses completion evidence of an individual task;
git-pr-workflow handles branch/PR interactions; release-readiness assesses
the full deployable artifact and operational consequences. A passing CI
is necessary if policy requires it but never grants deployment permission.

## Release as an observable state transition

Borrow the stage/check/rollback structure of GitHub's rollout-plan
methodology while preserving the independent GO/NO-GO authority gate.

| Risk | Process |
|---|---|
| LIGHT | No deployable behavior changed: skip release committee; check docs/metadata |
| STANDARD | Artifact pinned, staging smoke, readiness signals, simple rollback |
| DEEP | Approval owners, data migration compatibility, canary/blue-green, stop thresholds, reconciliation and incident handoff |

**1. Identify candidate:** source SHA, immutable artifact digest,
deployment environment and runtime/schema versions, rollback owner,
health baseline and consumer compatibility. Do not rebuild silently
after testing and then promote an unverified digest.

**2. Preflight:** dependency health, capacity, feature flags,
configuration/secrets, DB migration order, monitoring availability
and backup/restore evidence. A completed backup is not proof
restore succeeds; rehearse in a disposable environment if risk warrants.

**3. Rollout:** choose measurable canary increments and hold periods based
on deployment-specific SLOs. Compare current and baseline window on
error budget, latency percentiles, queue lag and business outcomes;
don't invent universal safe percentages. Define stop conditions and
who may decide rollback.

**4. Validate and close:** verify users can complete the critical
journey and that async tasks/data invariants hold after rollout.
Separate DEPLOYED from HEALTHY from RESOLVED. A code rollback cannot undo
published notifications or destructive schema changes; plan roll-forward
and reconciliation alternatives. Incident-commander owns emergency
coordination when actual impact occurs.

**Handoff example:** a safe database rename often requires additive
column, dual-read/write, data backfill, measured consistency, then
retirement after clients migrate. A single deploy "rename now, roll back
on fail" can be impossible. Keep NO-GO until transitions and restore
are proven or risk is explicitly accepted by the authorized owner.

Report GO/CONDITIONAL GO/NO-GO based on actually executed evidence,
separate unapproved production actions from tested staging.
