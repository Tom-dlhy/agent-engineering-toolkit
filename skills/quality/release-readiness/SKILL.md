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
