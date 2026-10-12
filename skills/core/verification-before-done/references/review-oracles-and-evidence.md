# Review oracles, reviewer independence and evidence ledger

**Read when:** R1 or R2 is needed, reviewer findings conflict, code changes after review, or completion must be justified to another engineer.

## Review evidence contract

A review claim must link requirements, exact BASE..HEAD, the reviewer
identity or tool, inspected paths/risks, findings, response and current
checks. "I reviewed it" from the implementer is R0, not independent R1.
A reviewer that read only the changed file cannot attest to caller
compatibility; a static SAST scan is not the entire security review.

~~~text
Revision / base / environment:
Acceptance IDs and observable outcomes:
Rigor LIGHT|STANDARD|DEEP:
Review R0|R1|R2:
Reviewer independence: self | separate actor | unavailable
Finding: ID, severity, file:line, preconditions and actual effect
Disposition: fixed | rejected with evidence | deferred | blocked
Checks: exact command, exit status, timestamp and relevant assertion
Not run: real cloud, real browser, rollback rehearsal, other gaps
Merge / deploy / destructive approval: explicit or absent
~~~

## A reliable review focuses on falsifiable defects

Review exact affected contracts, callers, privilege boundaries and
concurrent changes, not an automatic full repo restatement. For each
finding ask: can a legitimate or adversarial input reach this code,
what expectation fails, which existing guard prevents it (if any),
how severe is the real user-visible outcome, and what smallest test
would disprove the concern? R2 looks especially for authorization,
isolation, replay, partial failures, state transition recovery and
rollback. A clean report is valid when evidence supports it; do not
manufacture issues to justify an expensive subagent.

## Fix and re-review economics

One targeted fix pass is often enough when a reviewer exposes well-scoped
issues; re-run focused regressions and whole affected integration suite
on the new revision. Re-review the changed finding or its immediate
dependency if the fix changes semantics. If a fix widens trust boundaries,
escalate to a fresh broad risk review. No endless review/repair loop:
after a bounded number of rounds, classify outstanding issues and
escalate rather than paying for identical model opinions.

## Completion edge cases

* A review was green at SHA A, but new code was pushed at SHA B:
  previous review remains historical evidence, not approval of B.
* Two independent reviews both say "fine", but no negative auth test:
  completeness gap remains.
* CI is green, but destructive migration has no restore exercise:
  deployment readiness is blocked.
* Reviewer unavailable: inline author may still implement a local
  change, but must not claim external validation happened.
* Docs-only label fix: a good diff and link check can justify R0;
  demanding a reviewer would add cost with little benefit.
