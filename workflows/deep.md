# DEEP — risk-led implementation, controlled side effects and review gates

## Entry

Use when changes cross authorization, personal/sensitive data, persistent
migration, external privileged actions, high-consequence security,
distributed replay/concurrency, irreversible writes or difficult rollback.
DEEP describes **strength of proof**, not mandatory number of agents,
tools or pages of documentation.

## Procedure

1. Establish approved scope, target SHA, system trust boundaries, actual
   data/infra owners, prerequisites, rollback and external permissions.
   Mark missing approvals. A plan never authorizes destructive behavior.
2. Use implementation-planning to produce a versioned spec-linked
   dependency graph: interfaces, file ownership, negative acceptance,
   risk focus, recovery and test commands with expected observations.
3. Choose execution inline or subagent-driven via execution-orchestrator.
   Select parallel work only for independent investigations/isolated
   implementations with frozen interfaces and known integration owner.
   Do not fake reviewers or dispatches where tools are unavailable.
4. Run short meaningful verification cycles; preserve a file-backed
   progress/decision ledger when context loss is plausible. Review each
   important task's spec compliance and quality (possibly one competent
   reviewer for both) in proportion to risk.
5. Execute fault/invalid/replay/migration rollback tests in **authorized**
   disposable environments; distinguish mocked from live host evidence.
   Never touch real secrets or production records merely to prove a test.
6. Apply R2 independent risk review where required. Cover actual
   requirements, security/data correctness, concurrency and recovery;
   if independent tool unavailable mark gate BLOCKED, not "reviewed".
7. Integrate and run relevant full affected suite on exact combined HEAD;
   verify fresh CI, branch protection, outstanding findings and approval.
8. Hand off PR/branch outcome; merge/deploy/publish and destructive
   actions require explicit authority beyond source implementation.

## Review economics

Don't dispatch per-line reviewers or regenerate equivalent reviews when
the diff hasn't changed. Re-review the changed findings and affected
interfaces, and cap repetitive feedback rounds with risk-based arbitration.
Never reduce an essential safety gate merely to save tokens.

## Stop and recover

If remote side-effect outcome is unknown, reconcile/idempotency before
retrying. If migration rollback is unsafe, prefer a forward remediation
plan and staged acceptance. If a blocker cannot be tested safely,
record precise missing evidence and retain recovery artifacts.
No "production ready" label from structural checks or a clean mock CI.

## Example

A one-line tenant authorization predicate change may be DEEP/R2:
prove cross-tenant denial, old/new contract behavior and storage
isolation, then independent security review. It does not necessarily
need separate planning, implementation and two security subagents.
