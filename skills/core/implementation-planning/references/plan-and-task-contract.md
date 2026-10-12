# Implementation plan and task contract

**Read when:** producing a STANDARD or DEEP multi-step plan for an executor, especially a fresh agent with no conversation memory.

## Working document skeleton

Use the existing project's documentation placement; the following is a
*logical* format, not a mandated directory. Do not create a document for a
single harmless edit. A plan is only as authoritative as its linked, approved
requirements and verified repository revision.

~~~text
# Feature — Implementation plan
Goal: observable user change
Spec: real approved path, or "requirements captured below"
Repo/base: owner/repo @ inspected SHA
Authority: agreed scope / excluded scope / pending approvals
Constraints: exact versions, security policy, compatibility, test commands
Review focus: top uncovered failure modes, with task owners

Task 1 — minimal vertical slice
  Files: create/modify/test exact repository paths
  Produces: route POST /documents -> DocumentResponse
  Consumes: authenticated tenant context
  Dependencies: none
  Acceptance: unauthorized user -> 403 and zero writes
  Steps: failing test -> observe -> implementation -> targeted GREEN -> commit
  Expected: HTTP status, stable fields, storage state and exact test command
  Handoff: accepted signature + actual commit/test outcome

Task 2 — persistence
  Dependencies: Task 1 contract
  ...same contract...
~~~

## Design decisions and explicit values

The executor knows syntax for Python/TypeScript; they do not know whether
a DELETE is soft or hard, whether a datetime is UTC, or which tenant claim
is authoritative. Record these exact choices once in the global constraints
or producer interface, not repeatedly in every step. Pin details whose
guessing could cause incompatible code: filenames, function/class names,
request/response shapes, error statuses, migration direction, idempotency
keys, ordering and validation rules. Do not invent interface signatures
until actual project code and decisions have been inspected.

Write steps as observations instead of directives like "test thoroughly".
Example: "Run pytest tests/test_upload.py::test_cross_tenant_upload -q.
Expected: fails with 201 before fix; passes with 403 after fix, and no file
written." Distinguish a proposed expected failure from an observed one.
When TDD does not apply (docs-only edit, pure configuration, generated
contracts) state the strongest suitable alternate proof; never fake RED.

## Task size and handoff economics

A good task ends with a checkable artifact and a useful review decision.
Combining migration + API + UI into one task hides integration failures;
splitting "create directory", "add import", and "add header" into three
tasks buys no independent value. Prefer one cohesive slice including
needed scaffolding, a focused test and a commit. For long plans, define
a stable ID and a file-backed progress ledger so compacted contexts do
not restart already completed work.

Plan completeness is not a reason for overlong code examples. Include a
minimal code sample only when its exact bytes/interfaces are part of
the requirement or when a small example prevents a likely error.

## Executor acceptance contract

At task start: check HEAD, approved scope, dependent task artifacts and
the actual test command. At task completion: record changed paths, commit
range, test commands with real exit status, uncovered negative checks,
rulings/risks and any blocked permissions. If a task spans several commits,
review BASE..HEAD, never just HEAD~1. Confirm the accepted spec has not
changed since planning. When an external action is pending, stop at the
safe boundary and request authorization instead of representing it as done.

## Failure example

Bad plan: "Build upload backend; implement best practices; run tests."
It hides authorization, acceptable file types, storage transaction behavior
and what the UI expects. Improved plan identifies a source-controlled DTO,
tenant ownership invariant, max size and the staging/rollback rule, each
with one observable assertion. The difference is not extra verbosity; it
is removing decisions the implementer cannot safely invent.
