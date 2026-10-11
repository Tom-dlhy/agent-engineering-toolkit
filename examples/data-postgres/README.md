# PostgreSQL 18 disposable integration tests

**Not a migration recipe for production.** Uses a synthetic database,
isolated randomized schema, a separate NOLOGIN role and RLS enabled.
The test explicitly refuses to execute without both an isolated
connection string and DATA_TEST_EPHEMERAL=1. Do not set that flag
against customer or production data. CI supplies disposable Postgres
18 service with synthetic username/password and psycopg.

~~~bash
# Only in authorized, disposable PostgreSQL:
DATA_TEST_EPHEMERAL=1 PG_DATA_TEST_DSN='postgresql://postgres:password@127.0.0.1:5432/data_ci' \
  python -m unittest discover -s examples/data-postgres/tests -v
~~~

Proves chosen Postgres constraints, RLS with nonowner role,
rollback, additive column compatibility and safe EXPLAIN;
not benchmark capacity, RLS correctness for all roles/policies,
real production role setup, snapshot restore, distributed
exactly-once or online migrations under live traffic.
Check server major version before porting SQL.

Official: https://www.postgresql.org/docs/current/ddl-rowsecurity.html ,
https://www.postgresql.org/docs/current/ddl-constraints.html .
