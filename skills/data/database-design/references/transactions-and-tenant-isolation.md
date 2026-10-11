# SQL transactions, concurrency and PostgreSQL row security

**Read when:** business invariants span concurrent writers, tenant
access must be isolated or isolation anomalies matter.

## Correctness under concurrency
READ COMMITTED may observe changed results across statements.
REPEATABLE READ and SERIALIZABLE have PostgreSQL-specific
semantics; SERIALIZABLE can abort with serialization failure
requiring safe bounded transaction-level retry. If payment
already sent, retrying SQL isn't the same as undoing charge.
Guard lost updates with version-conditional UPDATE row count,
short SELECT FOR UPDATE where appropriate, or unique constraint.
A Python pre-check can't prevent a concurrent insert.

## RLS caveats
PostgreSQL RLS **must be enabled**. Once enabled and absent
allow policy, normal access defaults deny, but owners generally
bypass unless FORCE ROW LEVEL SECURITY; superusers/BYPASSRLS
roles bypass. TRUNCATE/REFERENCES aren't ordinary row-policy
operations. Test with actual **least-privileged app DB role**,
not migrations/owner.

~~~sql
-- Example requires tenant_id text, trusted per-transaction
-- SET LOCAL app.tenant_id, role review and real policy testing.
ALTER TABLE tenant_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_orders FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_access ON tenant_orders
 USING (tenant_id = current_setting('app.tenant_id', true))
 WITH CHECK (tenant_id = current_setting('app.tenant_id', true));
~~~

If application can inject SQL to set a different tenant
claim this design isn't isolated. Check connection pool
state reset and role separation.

## Negative tests
Tenant B cannot select/update/delete A; missing tenant
context denies; INSERT WITH CHECK rejects wrong tenant;
app role lacks BYPASSRLS; stale update conflicts;
two unique insert races only commit one; transaction
rollback restores expected state.

Sources: https://www.postgresql.org/docs/current/ddl-rowsecurity.html ,
https://www.postgresql.org/docs/current/transaction-iso.html .
