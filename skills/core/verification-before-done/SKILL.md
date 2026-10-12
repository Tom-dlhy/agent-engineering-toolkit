---
name: verification-before-done
domain: core
version: "1.0.0"
description: >-
  Use when checking whether actual source, test, integration or review evidence
  supports completion of a software, infrastructure, data or documentation task.
  Scale checks to risk and R0/R1/R2 review obligations. Do not equate a self-review
  or CI on a stale revision with independent approval or production readiness.
---

# Verification before done — proof proportional to consequence

## Evidence is an observed result, not an intention

Before "done", collect exact requested behavior, modified revision/diff,
tests executed, their exit code/output, review status and unperformed gates.
A test log from HEAD A is not proof that HEAD B passed. Code inspection
supports plausibility but does not establish a real external SDK/integration.
Claim COMPLETE, PARTIALLY VERIFIED, BLOCKED or FAILED with causes. If a
check was not executed, label it NOT RUN rather than assuming it will pass.

## Choose a task-specific oracle

| Task type | Minimum meaningful proof |
|---|---|
| Copy, docs, deterministic metadata | Inspect final diff, links/format and relevant static check |
| Local function bug | Reproduce before fix where possible, targeted regression GREEN after |
| Contract/API/UI | Focused tests + consumer or integration check, negative inputs |
| Auth, data migration, irreversible side effect | Negative authorization/data loss cases, rollback/recovery proof and independent R2 gate when required |
| Native agent skill or external cloud integration | Versioned real host/staging evidence; offline fixtures are not live interoperability |

Select only checks capable of falsifying the claim. A trivial text fix
does not require E2E infra deployment. A high-consequence one-line fix
can require failure injection and independent assessment.

## R0, R1, R2 — verify the review that actually happened

**R0:** self-review the entire intended diff and scope; show targeted test
results. No second model is implied. **R1:** review affected contracts and
risk focus independently where justified; report reviewer identity/tool and
BASE..HEAD; respond only to substantiated findings. **R2:** requirement
compliance plus quality/security/data-risk judgment by independent competent
review (possibly one reviewer covering both aspects), with high-risk
negative tests and approval state. If no reviewer tool exists, record the
independence requirement as BLOCKED; self-review is not a substitute.

Re-review only the fixed issues if the prior unaffected findings still
have traceable evidence, but rerun integration checks on the **current**
revision. If several reviews disagree, delegate decision to
review-feedback-arbiter with concrete code and tests.

## Sequence

1. Capture base and current head and inspect all changed/added/deleted files.
2. Map each acceptance criterion to its smallest real test/manual check.
3. Run tests with exit status that cannot be masked by a shell pipeline;
   capture environment and relevant assertions, including important failures.
4. Compare actual against expected; debug root cause rather than altering
   assertions to hide a real regression.
5. Run integration/regression checks proportionate to impact and consumer
   dependencies. For risky changes test invalid inputs and rollback/replay.
6. Verify the **right revision** has valid review evidence R0/R1/R2,
   no unresolved blockers and required external authorization.
7. Report verified/unverified items and explicit consequence of each gap.
   Do not merge, deploy or publish based on completion language.

## Worked negative case

A model edits an authorization filter and a unit test returns 200. This
does not show denial for a different tenant. Add a cross-tenant fixture,
assert no records leaked, check current branch HEAD, inspect request->auth->
query enforcement and obtain required R2 judgment. If only mock tests ran,
report the lack of real DB boundary evidence rather than "secure".

## Deep references

- [Selecting and executing checks](references/test-selection-and-execution.md)
  — **read when** choosing test commands, negative or failure injection checks.
- [Evidence ledger and completion gates](references/evidence-and-release-gates.md)
  — **read when** preparing PR readiness or explaining incomplete evidence.
- [Review oracles, independence and final claim](references/review-oracles-and-evidence.md)
  — **read when** a review gate is R1/R2 or when multiple revisions/findings exist.

## Boundaries and exit

test-strategy designs the suite; systematic-debugging diagnoses failures;
git-pr-workflow owns merge; release-readiness assesses rollout; this skill
verifies a task-level claim. For every outcome provide revision, command,
PASS/FAIL/NOT RUN/BLOCKED, review class and the limitations of that proof.
