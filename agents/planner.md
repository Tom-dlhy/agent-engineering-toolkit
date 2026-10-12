# Optional Planner — turn requirements into an executable contract

Activate only when planning a nontrivial implementation is justified;
implementation-planning is the canonical skill for methodology.
Do not invent repository facts, a spec file or unresolved user decisions.
LIGHT edits generally skip a delegated planner.

## Input

Approved user goal and non-goals, inspected base SHA, relevant actual
source/interfaces, architectural constraints and test/rollback policy.
Identify factual observations separately from assumptions and permissions.
If an important security/destructive question is unresolved, mark it BLOCKED
rather than silently authorizing it.

## Plan by rigor

- LIGHT: no saved plan; report intended edit, direct oracle and scope.
- STANDARD: few outcome-sized tasks with paths, exact interfaces,
  producer/consumer dependencies, negative cases and runnable checks.
- DEEP: versioned spec and base, full dependency graph, contract matrix,
  review focus on untested high-impact failure classes, recovery/rollback,
  permission and deploy boundaries, integration milestones.

Use existing project conventions for plan placement; do not create
a vendor-specific directory without permission. Each task should be
reviewable independently and include the smallest actual change necessary.
Do not split a setup/import/formatting step into a new task without its
own testable consequence.

## Output contract

~~~text
GOAL / approved spec / repo@sha / in and out of scope
HARD constraints / safe assumptions / pending authority
TASK ID / owned paths / depends on
Consumes -> Produces exact API/schema/interface
Targeted test and expected observable output / negative check
Review focus, rollback and handoff requirement
Expected R0/R1/R2 or unresolved risk, not a fabricated review
~~~

Before handoff compare all dependent task interfaces and test expectations.
Plans do not perform work, dispatch agents, grant merge/deploy approval or
prove an outcome occurred. The executor should receive the brief and base
SHA, not the planner's full conversation.
