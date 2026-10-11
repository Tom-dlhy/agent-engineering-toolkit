# Evolve a monolith incrementally; extract only when justified

**Read when:** planning a module refactor, strangler transition,
independent service deploy or distributed data split.

## A safe migration sequence

1. Observe actual dependencies/callers and business workflows.
2. Introduce narrow public module interface (no mass scaffolding).
3. Redirect call sites incrementally, with regression tests.
4. Establish data owner, migration responsibility and read access.
5. Enforce import tests, remove old direct table coupling.
6. Only if warranted: isolate API/protocol, network deployment,
   service data and asynchronous consistency model.
7. Run dual-version compatibility, rollback, load, failure,
   authorization and tracing tests before cutover.

An **anti-corruption layer** may translate a legacy domain
model into the new bounded context; it's not a mandatory
general-purpose service or a license to ignore semantic drift.
AWS notes such a layer adds latency/operations and should be
retired when migration completes.

## Extract decision criteria

- Independent domain team owns its deploy and on-call.
- Measured workload needs separately scaled compute/DB.
- Release coupling slows distinct product domains.
- Isolation/security requirements justify extra boundaries.
- Database transaction coupling can be removed without
  violating core invariants.

Without those, modular monolith may remain optimal for years.

## Extraction costs

Contracts and schema compatibility, more network failures,
distributed traces, retry/idempotency, data ownership
migration, migrations, elevated cloud running cost,
operational staffing and rollback complexity.

## Proof

Measure change-coupling, import violations and p95/p99 for
critical workflows before/after; test real client compatibility
and recovery during partial cutover. An architecture drawing
is a proposal, not measured evidence.

Sources:
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/acl.html ,
https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices .
