# Dependency graph and interface preflight

**Read when:** multiple tasks share files, interfaces, schemas, migrations, APIs or stateful resources, or when choosing parallel execution.

## Build the actual dependency graph

For each candidate task identify consumed and produced interfaces, file
ownership and side effects. Draw an edge A -> B when B reads a schema, type,
database column, endpoint, fixture or state established by A. An absent
edge needs evidence of independence, not wishful thinking. Acyclic groups
can be scheduled in topological order; cycles mean the proposed task
boundaries are wrong or an interface needs extracting first.

~~~text
A: define UploadMetadata API schema (produces type + contract tests)
B: persist records with tenant ownership (consumes type A)
C: UI integration (consumes type A and endpoint contract B)
D: documentation (consumes public behavior C)

Edges: A -> B, A -> C, B -> C, C -> D
Safe concurrency: investigate storage failure modes while A is designed;
unsafe concurrency: implement B and C with divergent invented response types.
~~~

## Preflight checklist as executable questions

1. Are all target files and caller paths observed on the inspected commit?
2. Do producer/consumer signatures match exactly, including defaults, nulls,
   async semantics, error shapes, content types and transport serialization?
3. Is any global resource shared (test DB, migration number, registry,
   generated file, port, lockfile, CI config, cloud account)?
4. Which tasks change an irreversible state or perform external writes?
5. Can an implementation be verified without other unfinished tasks?
6. Will the negative test actually fail on the current baseline, or is it
   redundant with an existing guarantee?
7. Can the branch be reverted in isolation? If not, who owns recovery?

Record one short finding per intersecting pair, including "no conflict"
when examined. Avoid a huge O(N²) table when tasks have no shared interfaces;
state "no shared interfaces observed" and cite the file ownership map.
Only execute in parallel after interface contracts are frozen and write
workspaces are isolated. Parallel *investigation* is cheaper and safer than
parallel *edits* to shared modules.

## Conflict case: migration and application code

A database migration renames a column. An API task assumes the new name;
a background worker still expects the old field. The graph is not simply
"migration first"; deployment compatibility matters. Plan an additive
schema, dual-read/write period or coordinated deploy, a restore path, and
contract tests for both versions if the system runs mixed releases. Record
which side owns the transition and when old compatibility can be removed.

## Change control and rulings

A plan mismatch discovered during implementation should become a narrowly
scoped ruling: exact conflict, observed file/interface, decision, impact
and verification to rerun. If it changes scope, public data policy,
destructive behavior or production permissions, return for approval.
A ruling ledger is an audit trail, not permission to override the user.
Never silently rewrite task acceptance criteria to make tests pass.
