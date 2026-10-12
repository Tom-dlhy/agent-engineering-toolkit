---
name: implementation-planning
domain: core
version: "1.0.0"
description: >-
  Use when translating an approved specification or nontrivial feature request into
  a dependency-aware, independently testable implementation plan with exact interfaces,
  acceptance checks and a reviewer handoff. Do not create a lengthy plan for a typo,
  replace requirements-discovery, or start code changes without requested authority.
---

# Implementation planning — executable contracts, not a ceremonial checklist

## Purpose, ownership and activation

Turn an agreed outcome into instructions that a competent engineer or a fresh-context
agent could implement without guessing the chosen interfaces. The plan is a **decision
record and an execution contract**, not a transcript or a license to do more work.
requirements-discovery owns unresolved product intent; architecture-decision owns hard
trade-offs; execution-orchestrator chooses how to execute; test-strategy owns test design.
Use this skill for nontrivial implementation decomposition even when no subagents exist.

Before writing, inspect **actual source**: project conventions, current branch/base,
interface callers, relevant tests, existing patterns, migration constraints, and
previous accepted decisions. Cite paths and observed contracts; mark guesses
explicitly. Never fabricate a file, command, existing API or test result.

## 1. Right-size the plan using task-routing

| Workflow | Plan expected | Stop adding detail when |
|---|---|---|
| LIGHT | No saved plan; at most intent, edit, one proof and a rollback note | One isolated reversible edit, no downstream interface change |
| STANDARD | Concise plan, usually 2–6 outcome-sized tasks; exact paths/interfaces and success tests where important | Another engineer could implement each task without guessing a consequential choice |
| DEEP | Versioned spec link, task dependency graph, contracts, fault/negative tests, recovery and approval points | High-impact uncertainty is resolved or explicitly blocked |

A sensitive three-line permission change can merit DEEP; twenty mechanical
independent text changes can remain STANDARD. Do not use line counts, agent counts,
keywords or the requested number of files as sole risk signals. Do not create
boilerplate for an already sufficiently specified single-step task.

## 2. Establish authority before sequence

Separate four classes: **binding** user requirements and non-goals; inspected code
facts with revision; **assumptions** that can be reversed safely; and decisions
requiring human authorization (production operations, irreversible/destructive
actions, widened data access, publication/merge). A plan cannot grant its own
authorization. If a missing value changes security or user-visible semantics,
identify the smallest blocking question; otherwise choose a conservative default
and label it. Reference an approved spec when one exists; do not invent its path.

Write one measurable outcome and acceptance scenarios: happy path, one meaningful
negative path, compatibility/regression behavior and proof environment. Distinguish
a user-level requirement from a chosen technical means so that implementation can
adapt without silently changing scope.

## 3. Map file ownership and interfaces before task numbering

Inventory files expected to change, ownership boundaries, shared public
interfaces, migrations and third-party side effects. For dependent tasks record
exact producer -> consumer contracts: names, signatures, input/output schema,
invariants and version compatibility. Identify a small vertical slice that can
run and be verified independently; fold empty setup/scaffolding into its
first useful deliverable. Split a task only when it has its own distinct
acceptance/review decision. Serialise shared interfaces unless an agreed
contract and isolated workspaces make concurrency safe.

For each task write:
- **Outcome & scope**: testable behavior, non-goals, permitted files and dependencies.
- **Precondition & interface**: exact upstream contract, environment and fixture.
- **Execution steps**: RED failure observation for behavioral changes when feasible,
  minimal change, GREEN verification, integration check, coherent commit.
- **Oracle**: command or human check, expected observation, negative and error cases,
  and what counts as a genuinely executed pass.
- **Review focus**: what could go wrong outside these tests, including a bypass
  or concurrency path when relevant.
- **Handoff**: what evidence next task/agent needs, and whether action requires approval.

Do not hard-code detailed sample code unless needed to pin an ambiguous interface;
if included, it must be syntactically sound and match the project language.

## 4. Pre-flight plan review (before execution)

Check every task against global constraints. For each shared API/file, match
the producing task to all consumers; check fixtures versus stated expected
outcomes; check ordering of migrations, indexes and rollback; check that
test commands will exercise the artifact just produced, not stale caches.
Record conflicts with resolution and downside if wrong. On DEEP plans,
include a **Review Focus** section naming the highest-impact failure classes
not covered by tests; turn the most critical into task-local acceptance tests.
Explicitly state where human decisions are pending; no silent scope widening.

## 5. Handoff and change control

Hand the executor the *spec*, *plan path*, *current base revision*, *constraints*,
*task table* and *first permitted action*. Never claim a delegated actor exists.
The executor may record a narrow engineering ruling if a plan step is wrong;
log the rationale, evidence and downstream impact before deviating. A change
to requirements or sensitive side effects returns to the owner for authorization.
The plan's task IDs and progress ledger enable resume after context compaction:
a completed task must be tied to actual commit(s) and test output.

## Example decision

For a feature introducing a tenant-owned document upload: task one defines
the Zod/request + ownership contract and negative authorization test; task two
stores metadata and bytes with compensating cleanup; task three wires UI.
The first two share an interface and must agree on exact types before parallel
work. Review focus includes stale upload tokens, orphaned blobs, content-type
spoofing and rollback after partial success. Contrast: a button-label typo
needs a direct edit and a relevant check, not these three tasks.

## Selective deep references

- [Plan specification and runnable task contract](references/plan-and-task-contract.md)
  — **read when** writing STANDARD or DEEP plans or handing tasks to fresh agents.
- [Dependency and interface preflight](references/dependencies-and-preflight.md)
  — **read when** tasks touch shared schemas, files, migrations or integration boundaries.
- [Review-focus and risk-driven negative tests](references/risk-and-review-focus.md)
  — **read when** planning DEEP work, production-sensitive paths or acceptance gaps.

## Exit evidence

Deliver a proportionate plan with exact spec provenance, owned paths, task
dependencies, acceptance oracle and unapproved actions separately identified.
Never mistake a written plan for a verified implementation or promise a
model/agent was dispatched. See task-routing for rigor selection and
verification-before-done for completion evidence.
