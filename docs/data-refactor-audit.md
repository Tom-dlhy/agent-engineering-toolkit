# Data category — SOTA-source-verified engineering review

Research date: **2026-10-11**. Charter: user-maintained *Agent
Engineering Toolkit — Charte de gouvernance et d'évolution, v2*.
Base: main after merges Core #13, Quality #14, Architecture #15,
Backend #16. Aim: practical, source-verified domain expertise with
**selective reference leaves**, one uniform contract and no tiers.

## Pre-refactor audit and candidate decision

| Skill | Original gap | Decision |
|---|---|---|
| data-pipeline-quality | 1 KB and no local leaves, vague idempotence/tests | EXTEND: contracts, backfills, Airflow, lineage/privacy |
| database-design | 1.2 KB, no constraint/RLS implementation | EXTEND: constraints, transaction/RLS, lifecycle |
| postgres-performance | 1 KB, no EXPLAIN safety or plans | EXTEND: safe plans, indexes/VACUUM, locks/capacity |
| schema-migrations | 1 KB, no operational migration procedure | EXTEND: expand-contract, backfills, tooling/rollback |
| analytics-modeling | Independent missing analytical grain/metric responsibility | CREATE: fact/dimension, dbt and historical metrics |
| lakehouse-engineering | Independent missing storage/table/warehouse responsibility | CREATE: Parquet/Iceberg, Snowflake and BigQuery |
| streaming-cdc-engineering | Independent missing log/stream state responsibility | CREATE: Debezium, Flink event-time, checkpoints/sinks |

**4 extended + 3 new Data skills = 7, across 22 deeply scoped
references**. Reuse/extend before create. This is not a maturity
ranking: each skills' content must meet the same quality obligations.

### Explicit boundaries
- analytics-modeling handles fact/dimension grain and semantic metrics;
  database-design handles transactional relation/constraints.
- lakehouse-engineering handles file/table format and analytic engine
  refresh/cost; data-pipeline-quality handles correctness/freshness
  and re-runnable data transformation.
- streaming-cdc-engineering handles change logs, WAL, event time,
  watermarks and checkpoint state. event-driven-design handles
  **business** event/outbox/saga protocols, not database row CDC.
- python-persistence owns SQLAlchemy sessions/ORM; schema-migrations
  owns multi-version database rollout; postgres-performance owns
  measured PostgreSQL plan and capacity.

## Verified official sources and conclusions

| Area | Primary source | Decision / limitation |
|---|---|---|
| PostgreSQL planner | https://www.postgresql.org/docs/current/sql-explain.html | EXPLAIN ANALYZE runs actual query; unsafe on DML without authorization |
| PostgreSQL RLS | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | RLS opt-in, owner/BYPASSRLS exception, test app role |
| PostgreSQL constraints | https://www.postgresql.org/docs/current/ddl-constraints.html | Unique/NULL/check behavior, DB-enforced concurrency invariants |
| PostgreSQL indexing | https://www.postgresql.org/docs/current/indexes.html | Choice by query/selectivity and write overhead, not universal index |
| Alembic autogenerate | https://alembic.sqlalchemy.org/en/latest/autogenerate.html | Candidate migrations, manual review required |
| Airflow 3.3 docs | https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html | Tasks retry and should be idempotent; no cross-executor local file assumption |
| dbt incremental | https://docs.getdbt.com/docs/build/incremental-models | unique_key governs matching, not actual uniqueness; late data/full refresh issues |
| dbt tests and layers | https://docs.getdbt.com/docs/build/data-tests and https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview | Quality checks and staging/intermediate/marts separation |
| Great Expectations 1.x | https://docs.greatexpectations.io/docs/reference/api/checkpoint_class/ | Version 1.x checkpoint API differs from older 0.18 docs |
| Kimball dimensional | https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/ | Grain, conformed dimensions, metric fanout and historical fact semantics |
| Iceberg | https://iceberg.apache.org/docs/nightly/evolution/ and https://iceberg.apache.org/spec/ | Schema field IDs, partition evolution and snapshot semantics, engine compatibility |
| Parquet | https://parquet.apache.org/docs/ | Columnar file format ≠ ACID table transaction format |
| Snowflake | https://docs.snowflake.com/en/user-guide/dynamic-tables/decision-guide | Declarative dynamic tables vs procedural streams/tasks; target lag isn't fixed schedule |
| Snowflake stream | https://docs.snowflake.com/en/user-guide/dynamic-tables/streams-on-dts | Incremental dynamic table stream observes net changes, not full audit history |
| BigQuery | https://docs.cloud.google.com/bigquery/docs/best-practices-costs | LIMIT alone won't necessarily reduce scanned bytes; use budgets |
| Debezium 3.7 | https://debezium.io/documentation/reference/stable/connectors/postgresql.html | WAL/slots, initial snapshots, replay, permission and lag hazards |
| Flink stable | https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/ | State checkpoint vs end-to-end sink delivery guarantees |
| Flink V2 | https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream-v2/watermark/ | V2 API marked experimental in current docs; don't uncritically adopt |

**SOTA** means up-to-date semantics, applicability to pinned installed
versions, tested failure modes and explicit uncertainty — **not**
assuming each latest version is universally deployable. Stack
Overflow/community bug reports can suggest reproduction, while
official specs/documentation and actual tests govern API claims.
The sources are informational, not remotely executable instructions.

## Executable evidence and protection

- 7 positive and 7 negative-neighbor lexical selection cases,
  plus two no-match cases in evals/data-routing.yaml.
- tests/test_data_expertise.py checks 116 skills, 7 Data, 22 real
  leaves, source annotations, selective loading, safe paths,
  profile boundaries and uniform no-maturity policy.
- tests/test_data_replay_contract.py runs deterministic pure
  Python replay/deduplication/tombstone/tenant corrections.
- tests/test_data_analytics_contract.py runs five SQLite in-memory
  semantic contract tests: fact grain, correct/incorrect SCD2 joins,
  overlap detection and weighted ratios. SQLite is a logic fixture,
  **not** Snowflake/BigQuery dialect or performance certification.
- examples/data-postgres/tests/test_postgres_contracts.py exercises
  **real disposable PostgreSQL 18** in CI, with an independent
  NOLOGIN app role for RLS, uniqueness, CHECK, rollback,
  expand-column compatibility and safe EXPLAIN. Requires an
  explicit ephemeral guard and synthetic credentials.
- Earlier toolkit, FastAPI and Node example CI must remain green.

## Explicit limitations and backlog

No live Snowflake/BigQuery costs, Flink cluster/checkpoint, Debezium
connector failover/WAL retention, Iceberg catalog multiwriter,
real dbt/GX execution, production load benchmarks, comprehensive
privacy/legal assessment or full real-agent Codex/Claude held-out
evaluation were performed. PostgreSQL fixture is synthetic and
does not prove high-volume online schema DDL lock behavior or
real client role topology. Keep these as concrete acceptance gaps
without arbitrary skill maturity tiers.

No third-party skill imports/executables or unapproved production
database mutations. PR remains Draft until user authorizes merge.
