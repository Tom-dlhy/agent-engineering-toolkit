# Release acceptance — immutable artifact and decision evidence

**Read when:** preparing a production release candidate, building a
GO/NO-GO checklist or reconciling CI with the actual deployable artifact.

## An actual release has an identity

Record repository + source SHA, CI run, builder/toolchain version, immutable
binary/container digest, schema migration revision, environment/region and
change scope. A CI check on one SHA does **not** certify a rebuilt artifact
from a later SHA; a green PR status isn't release permission.

| Gate | Required proof by relevance |
|---|---|
| User behavior | Executed acceptance and relevant negative tests |
| Runtime | Artifact boot, health/readiness, config and dependency access |
| Security | Secret rotation/permissions and reviewed reachable findings |
| Supply chain | Pinned dependencies, build artifact/digest/provenance |
| Data | Backward-compatible schema, backup and replay/rollback |
| Capacity | Load/quotas within SLO under representative conditions |
| Operations | Observability, alert owner, support/incident runbook |
| Release authority | Approved reviewers, change window if applicable |

A nonapplicable control needs a documented rationale. A required check that
cannot be executed is BLOCKED, not secretly passed. NIST SSDF SP 800-218
1.1 supplies a secure-development life-cycle framework; its 1.2 revision
had an initial public draft in late 2025, so do not treat draft text as
a stable final requirement without checking.

## Decision states

**GO** when necessary evidence exists and authority approves.
**CONDITIONAL GO** only when the risk owner explicitly accepts
well-defined nonblocking gaps and a fallback exists.
**NO-GO** on failed critical acceptance, missing authorization, unknown
data-loss risk or impossible rollback for high-impact change.

## Report

Current tested and deployable SHA/digest, environment, evidence table,
open issues, GO rationale, rollout strategy, rollback stop criteria,
assigned operator and explicit *no deployment* if user only requested review.

Official: https://csrc.nist.gov/pubs/sp/800/218/final and
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets .
