# Airflow DAG orchestration, retries and backfills

**Read when:** designing scheduled ETL, DAG dependencies, retries
and task behavior across executors or Airflow versions.

## What the scheduler guarantees (and doesn't)
An Airflow DAG orchestrates work. Its task may retry on
failure, hence task effects must be idempotent and publish
only complete outcomes. Avoid external API calls or expensive
DB queries in module-level DAG parsing. Check actual Airflow
3.x versus 2.x import paths and deployment providers.

Use **logical data interval** and explicit timezone/DST
instead of machine now() as partition source. XCom is for
small metadata/pointers, not sensitive dataframes. Executors
may place tasks on different hosts, so local disk files
aren't reliable cross-task outputs. Store remote object
pointer and validate remote artifact on downstream task.

## Pipeline choices
One warehouse-native declarative SQL transform may be
scheduled by dbt/warehouse or Snowflake dynamic table.
Airflow earns its maintenance when scheduling heterogeneous
systems, conditional dependencies, multi-stage retries,
auditable backfills and external operators.

## Task success means durable publication
Stage output to unique run/partition, validate row contracts,
and publish by safe atomic operation where supported. Re-run
same interval and compare. Avoid insert-only write producing
duplicate rows on retries. Use approved Connections/secrets
backend for credentials; never embed secrets in XCom.

## Integration plan
Parse/import test, task callable tests, real disposable
storage/warehouse with synthetic fixtures, duplicate
interval, task killed after stage write, missing upstream
source, dependency failed, catchup, backfill, timezone DST
and retry after partially committed output.

Sources: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html ,
https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html .
