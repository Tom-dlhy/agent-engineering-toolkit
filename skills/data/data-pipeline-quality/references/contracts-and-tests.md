# Data contracts and quality gates

**Read when:** defining ingestion contracts, dbt/GX tests, freshness
monitoring or deciding when to quarantine versus publish.

## Contract checklist
Record owner, row grain, version, lawful consumers, required fields/types,
unique business key, nullability, timezone, event/ingestion timestamp,
schema change policy, deletes, expected partitions, freshness SLO,
sensitive fields and retention. Schema-valid records can still be
**business-invalid**; reconcile against the right source.

| Check | Meaning | Potential false positive |
|---|---|---|
| Uniqueness | One row per business key/grain | NULL composite key semantics |
| Completeness | Expected partitions and source snapshot | Legitimately empty seasonal feed |
| Relationships | Foreign dimension resolves | Explicit unknown surrogate might be allowed |
| Valid range | Amount/status business rule | Refunds can be negative |
| Freshness | Validated data age | Max(event_time) not ingestion freshness |
| Reconciliation | Keys/sums agree at matching grain | Different duplicate/deletion policy |
| Distribution | Seasonal baseline/alerts | Random/static threshold |

## Version-sensitive frameworks
dbt standard generic tests include unique, not_null,
accepted_values and relationships; add domain SQL tests for
business invariants. Passing dbt tests doesn't imply metrics
are meaningful or all records were received.
Great Expectations **1.x** Checkpoints operate with Validation
Definitions. The older GX 0.18 Checkpoint/ExpectationSuite
examples may be incompatible; check pinned version before coding.

## Publish gate
Choose BLOCK, QUARANTINE, WARN or ALERT by consumer impact.
On block keep last known-good published state, quarantine
restricted samples with expiry, and avoid logging raw PII.
Alert must include dataset, source snapshot, owner and test
failure; warnings require human review and an expiry.

## Negative tests
Duplicate/key collision, NULL key, schema change, empty
partition, late record, source stale but successful DAG,
invalid amount and cross-tenant leakage. Re-run a prior
source snapshot and verify the same validated output.

Sources: https://docs.getdbt.com/docs/build/data-tests ,
https://docs.getdbt.com/docs/deploy/source-freshness ,
https://docs.greatexpectations.io/docs/reference/api/checkpoint_class/ .
