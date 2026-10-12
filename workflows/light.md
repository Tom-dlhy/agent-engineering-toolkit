# LIGHT — focused change, real evidence, minimal overhead

## Entry

Use for reversible, localized work with a clear expected result and no
relevant shared interface, sensitive permission/data effect or migration.
A request can mention a complex domain but still be LIGHT if the actual
change is an isolated doc/UI detail. task-routing assesses impact, not
topic keywords. Never use LIGHT to bypass a known security or external
authorization gate.

## Procedure (usually inline, R0)

1. Confirm requested diff and current target file; don't interview
   the user or make a saved plan for already specified work.
2. Select zero or one specialized skill needed for actual task.
3. Implement directly, preserving unrelated user changes.
4. Run one focused falsifiable check: diff/link/format check for docs,
   unit regression for code, targeted browser observation if actually
   available for UI. Inspect negative path if the behavior requires it.
5. Self-review full intended diff for scope, secrets and accidental files.
6. Report verified outcome with exact check and any untested limitation.
   No automatic reviewer agent, worktree or PR ceremony.

## Escalate when

Uncovered shared interface, missing authorization, sensitive state,
destructive side effect, unexpected test failure or uncontrolled dependency.
Explain observed trigger and switch only the necessary axis:
e.g. LIGHT edit can escalate review to R2 if it touches authorization.

## Example

Correct a button label; inspect rendered output or component test and
diff. Do not make a detailed task graph or spawn reviewers. Do not call
the check "passed" unless it actually ran.
