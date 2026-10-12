# STANDARD — incremental feature delivery with proportionate review

## Entry

Use for recoverable multi-file features, ordinary refactors, known API
changes and integrations without high-consequence irreversible effects.
Start inline unless isolation, new context or meaningful independence
justify delegation. Review is R0 with reliable tests, or R1 when
coupled interfaces, novel behavior or uncertainty merit fresh judgment.

## Procedure

1. Inspect repo, constraints, baseline tests, callers and relevant
   existing skills. Avoid a long discovery interview for a clear request.
2. Use implementation-planning for a **short** 2–6-task plan only if the
   change actually needs decomposition. Each task specifies outcome,
   owned files, consumed/produced interfaces, acceptance and negative check.
3. Execute tasks in dependency order with small testable commits;
   inline is default. Use an actual optional subagent only if the
   expected benefit exceeds context startup and review cost.
4. Select R0/R1 based on impact: a deterministic cross-file rename
   can remain R0; an unfamiliar API/UI contract may get targeted R1.
5. Run focused tests per task and affected integration tests on
   combined current HEAD, including one relevant invalid/error path.
6. Respond to substantiated review findings with smallest fixes,
   bounded re-review when needed and current-revision tests.
7. Open PR if requested/required, report checks, limitations and pending
   merge authority. Never infer merge approval from green CI.

## Escalate / de-escalate

Escalate to DEEP when real security boundary, data-loss/replay,
migration/rollback or high impact appears. A routine "production"
word in a description is insufficient by itself. If supposed
complexity turns out to be a local mechanical edit, return to
LIGHT-like execution while retaining necessary safeguards.

## Example

Add one public form endpoint and UI state. Freeze the request/response
contract, implement with contract tests, run integrated happy and
invalid payload cases; add targeted R1 if an unfamiliar consumer is
affected. Don't hire two fresh reviewers to inspect one field rename.
