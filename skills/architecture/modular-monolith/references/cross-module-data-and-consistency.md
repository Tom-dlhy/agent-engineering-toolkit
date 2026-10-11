# Cross-module workflows, data ownership and transactions

**Read when:** modules share a database or exchange state and
the chosen consistency, query and migration owner are unclear.

## Direct call or event?

| Need | Usually choose | Caveat |
|---|---|---|
| Immediate consistent read from another module | Published synchronous application query | Call graph/cycles need control |
| Atomic invariant in one database | Explicit application unit of work | Agree on boundary/lock ownership |
| Independent reporting projection | Async event/read model | Eventual consistency/reconciliation |
| Long external provider action | Durable job/status | Never hold DB lock during slow call |
| Many independent subscribers | Event publication | Outbox/inbox needed for failure guarantees |

One deploy does not automatically justify a broker between every
two modules. A single SQL database may support a well-defined
transaction spanning module code, but table ownership and
migration authority should stay explicit. Avoid hidden save()
commits inside repositories that prevent atomic use cases.

## Example: Order confirmation and billing

Application use case validates order, authorizes tenant,
coordinates billing reservation and order transition within
an authorized transaction when both are local to same store.
When billing is an external payment provider, remote effect
cannot be atomically committed with SQL: use persisted intent,
stable provider idempotency and reconciliation.

## Data boundary

If modules use same Postgres schema, enforce private table
imports and stable public API. Separate schemas can improve
ownership/privileges but do not alone prove independent
deployability. For replicated read projection, version the
event and allow lag/missing event repair.

## Tests

Atomic rollback, stale optimistic version, duplicate requests,
tenant ownership, schema migration while old/new code coexists,
and missed event replay. Identify data invariants requiring
synchronous strong consistency before proposing extraction.

Sources:
https://docs.sqlalchemy.org/en/20/orm/session_transaction.html and
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html .
