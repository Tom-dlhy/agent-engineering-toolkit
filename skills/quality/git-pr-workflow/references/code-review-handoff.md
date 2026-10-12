# Code-review handoff and bounded feedback loop

**Read when:** an R1/R2 review is justified, PR feedback has arrived or a new commit invalidated old review evidence.

## Why the reviewer packet matters

A reviewer working from a fresh context should inspect the product,
not infer requirements from the implementer's confidence. Hand off only
necessary facts, preserving exact user constraints and negative acceptance.
Use BASE..HEAD rather than HEAD~1 (which misses multi-commit tasks);
avoid dumping unrelated history or copying secrets.

~~~text
REPO / HEAD / BASE / exact diff range
PURPOSE / approved spec or concise acceptance, explicit non-goals
FILES / key interfaces and affected consumers
REVIEW LEVEL / R1 or R2, why and what is outside scope
FOCUS / plausible untested failure modes
EVIDENCE / exact test command, environment and observed result
RISKS / security boundaries, migrations, concurrency, rollback
REVIEWER OUTPUT / severity, file:line, reachable input, impact, proof,
                  smallest safe fix, regression test, uncertainty
~~~

R1 targets the changed contract and its callers. R2 covers requirements
compliance and quality/security as independent *concerns*: it does not
mandate multiple redundant models when one qualified independent
reviewer can address both. A reviewer may legitimately return no issues.
Ask for explicit "not assessed" areas rather than inventing coverage.

## After feedback

For every finding capture ID, current line/revision, what behavior the
reviewer asserts, actual code/test reproduction, verdict
(ACCEPT/MODIFY/REJECT/DEFER/RESOLVED), and the smallest safe action.
Do not accept unsupported feedback merely because it came from an AI.
Fix load-bearing bugs first; include targeted regression checks.
A correction that touches a new trust boundary can require broader
R2 reassessment; otherwise re-review only modified findings.

Set an explicit small iteration budget. When repeated reviews give
the same unsubstantiated opinion, adjudicate against the spec,
tests and real impact rather than generating more reviews. If unresolved
critical/important findings remain, do not call the PR ready.
A stale review at SHA A is not approval for SHA B; verify combined
integration tests at current HEAD and record skipped checks.

## Adversarial example

Reviewer: "Use Promise.all on all these writes for performance."
Actual requirement: writes are ordered and operation B consumes A's ID.
Verdict: REJECT (shared state); demonstrate dependency with code and
a contract test. If parallelism is beneficial for truly independent
queries, revise suggestion to those calls and measure latency before
claiming an improvement.

## Handoff to git-pr-workflow

Document review decision and gates as PR comments or a concise ledger;
never silently mark required checks or human approvals complete.
Keeping a review packet as a file is useful for long plans, but
LIGHT edits do not need persistent process artifacts.
