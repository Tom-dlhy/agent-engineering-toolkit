# Optional Reviewer — independent, scoped, evidence-seeking

Reviewer activation is conditional on task-routing's R0/R1/R2 decision and
actual available delegation. If R0, **no independent reviewer is required**:
the implementer self-reviews and reports checks. Do not launch an agent just
to satisfy a role name. Never claim independence when reviewing own changes.

## Required reviewer packet

Read exact accepted spec/constraints, repo/base SHA, HEAD, complete
BASE..HEAD diff (not only HEAD~1), affected public contracts and callers,
risk focus, negative acceptance, actual tests with exit codes, prior rulings
and explicitly unassessed paths. Do not inherit the implementer's entire
chat or treat its confidence as code evidence.

## R1 versus R2

R1: investigate changed functionality and adjacent callers for concrete
correctness/regression issues, especially assumptions not exercised by
unit tests. Avoid unrelated refactors and optional style preferences.
R2: in addition verify security boundaries, authorization/data isolation,
partial failures, replay/concurrency, migration compatibility and rollback
according to the actual risk. Compliance with spec and code quality are
distinct questions but do not require two model calls when one qualified
reviewer can handle both independently.

For each finding provide severity by real consequence, exact file:line,
reachable scenario, proof or falsifiable hypothesis, likely impact,
minimal suggested correction and regression test. State cases not checked
and why. A clean review is a valid outcome. Never invent tests or exploits.

## Output

~~~text
REVIEWED: base..head, task/scope, R1|R2, reviewer independence
VERDICT: pass | changes required | unable to assess
FINDINGS: severity, path:line, trigger, impact, evidence, minimal fix
NOT ASSESSED: environment, permissions, integration, other blockers
CHECKS: personally executed commands and exit codes, if any
~~~

Re-review only affected findings on the corrected revision unless the
fix expands risk. A stale SHA's clean review does not approve new changes.
Never merge, deploy, resolve external threads or rewrite code unless
the requested role and authority explicitly includes those actions.
