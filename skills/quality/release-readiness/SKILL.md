---
name: release-readiness
domain: quality
version: "0.1.0"
description: >-
  Use when assessing a release candidate before production deployment, database migration or a high-impact product launch. Do not turn a harmless docs change into a release committee.
---

# release-readiness

## Readiness
Verify functional acceptance, build artifacts, CI results, runtime configuration, access permissions and feature flags. Check migrations, backups, rollback and dependency availability.
## Security and operations
Review secrets, monitoring, alerting, service limits, privacy/retention and user-facing error handling. Confirm support/runbook ownership and customer communication requirements where applicable.
## Controlled rollout
Prefer preview/staging checks, smoke tests, gradual promotion and post-release SLI monitoring for risky changes. Record exact tested artifact/version.
## Report
Produce concise GO / NO-GO / conditional decision with evidence, unverified checks and rollback trigger. No automatic deploy or merge.
