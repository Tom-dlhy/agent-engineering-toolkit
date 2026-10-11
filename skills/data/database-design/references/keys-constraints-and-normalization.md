# Database model: keys, referential integrity, normalization

**Read when:** creating transactional SQL tables, relationships,
business uniqueness and constraint-driven application invariants.

## Map invariant to mechanism
- PRIMARY KEY: stable row identity, natural or surrogate
  when defensible by expected changes/size/privacy.
- UNIQUE: business uniqueness across concurrent writers;
  PostgreSQL permits duplicate NULL by default unless
  NULLS NOT DISTINCT is supported/selected.
- FOREIGN KEY: referential integrity plus deliberate
  delete/update action. Cascade may delete unexpectedly.
- CHECK: row condition; SQL NULL result is not false,
  so add NOT NULL when missing value is invalid.
- Exclusion/range constraints for temporal overlap only
  after confirming actual Postgres version and operators.

~~~sql
-- Illustrative PostgreSQL schema, not full payment system.
CREATE TABLE customers (
  customer_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  external_ref text NOT NULL UNIQUE
);
CREATE TABLE invoices (
  invoice_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id bigint NOT NULL REFERENCES customers(customer_id),
  amount_minor bigint NOT NULL CHECK (amount_minor >= 0),
  status text NOT NULL CHECK (status IN ('draft','issued','paid'))
);
~~~

Actual invoices need currency/rounding and audit semantics.
Never use this toy state model to perform real payments.

## Normalize first, denormalize for evidence
Separate repeated business entities and their mutable
dependencies to avoid update anomalies. 3NF is a
useful default, not mandatory form for every workload.
JSONB can hold variable attributes but JSON documents
aren't automatic substitutes for FK/unique constraints.
Denormalization needs sync/refresh ownership and
negative tests for stale replicas.

## Test contract
Duplicate keys in concurrent inserts, null in composite
keys, invalid state, orphaned FK, simultaneous create,
delete with dependent rows, unsafe cascading, unexpected
public exposure of surrogate IDs and tenant boundaries.

Sources: https://www.postgresql.org/docs/current/ddl-constraints.html ,
https://www.postgresql.org/docs/current/datatype-json.html .
