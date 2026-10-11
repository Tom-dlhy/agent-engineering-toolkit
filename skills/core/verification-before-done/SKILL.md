---
name: verification-before-done
domain: core
version: "0.2.0"
description: >-
  Use when assessing whether actual evidence supports completion of a coding,
  documentation, infrastructure, data or deployment-preparation task. Do not
  substitute code review or unrelated green CI for unexecuted behavior.
---

# Verification before done — evidence gate

## Check the claim, not just the command

1. Inspect user acceptance criteria and actual diff. Associate each claimed outcome
   with a check capable of falsifying it.
2. Run proportional tests safely in the *documented project environment*: focused
   test, unit/integration, typecheck, lint, build, contract, UI/AT, security,
   staging smoke or migration rehearsal as relevant and authorized.
3. Include negative paths relevant to changed semantics; don't declare all paths
   covered because a healthcheck passed.
4. Record exit codes and skipped cases. Use pipefail where supported; be careful
   with `pytest | tee` / `grep` hiding the actual command failure.
5. Recheck exact revision and CI run: prior green commit does not prove the new head.
6. Report verified, partially verified, blocked or failed without pretending a
   check ran or promising unspecified future execution.

## Evidence hierarchy

| Evidence | Supports | Doesn't support |
|---|---|---|
| Source/diff review | Structural plausibility | Runtime correctness |
| Unit/mock test | Named local behavior | Real cloud/IAM or DB isolation |
| Staging smoke | Named staging environment behavior | Production release |
| CI for commit A | Commit A check results | Commit B changes |
| Real device QA | Tested device/assistive path | All devices/usability |

## References

- [Selecting and executing checks](references/test-selection-and-execution.md) —
  **read when** deciding appropriate proof, dealing with failures or test commands.
- [Evidence ledger and completion gates](references/evidence-and-release-gates.md) —
  **read when** reviewing PR readiness, documenting limitations or handoff.

`test-strategy` designs suites; `systematic-debugging` diagnoses failures;
`release-readiness` governs overall deployment; this skill verifies **this claim**.

## Exit
Per outcome: check, environment/commit, PASS/FAIL/SKIPPED/BLOCKED, limitation.
No unauthorized deployment or merge from a green test alone.
