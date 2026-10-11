# Spark plan, AQE, skew and measured query optimization

Read when: a Databricks SQL/PySpark workload is slow, has uneven task duration, shuffle spilling or unexpected join amplification.

## Evidence first
Pin cloud, DBR, compute kind, Photon enabled/disabled, inputs and catalog, statement/job ID, p50/p95 and stable snapshot. Inspect Spark UI stage/operator metrics, query profile and executed **final adaptive plan**; static EXPLAIN is not evidence of runtime gain. Use the same source key and expected output population before/after.

Spark's Adaptive Query Execution can change sort-merge to broadcast joins, coalesce partitions, address skew and propagate empty relations. AQE optimization is not guaranteed for every query. Examine whether it was actually applied and the final physical plan.

## Failure decision table
| Observation | Hypothesis | Falsification check |
|---|---|---|
| Many tiny tasks | Overpartition/shuffle size | AQE coalescing and actual file/task sizes |
| One giant task | Key skew or unbalanced partitions | per-stage task histogram and hot key distribution |
| Join output explodes | Grain/cardinality mismatch | uniqueness by join key, expected fact row count |
| Shuffle spill | Wide aggregation, cardinality or memory | operator metrics and reduced projection experiment |
| Scan huge despite filters | Partition/data skipping missing | file stats, table layout and predicates |
| Plan fast, client slow | Result serialization/fetch | client time and result volume |
| Frequent executor OOM | Data distribution/caching or underprovisioning | heap/GC/driver vs executor metrics |

## Reversible Spark example
~~~python
# Read-only on an existing authorized Spark session.
plan = (
    spark.table("dev_catalog.analytics.orders")
    .where("order_date >= DATE '2026-01-01'")
    .groupBy("customer_id")
    .count()
)
plan.explain("formatted")  # plan only; not actual run or cost proof
~~~
Do not write hard-coded data repartitioning values into production without measuring actual shuffle. A broadcast hint can worsen executor memory; salting a join may multiply intermediate data and alter semantics. A DISTINCT added to hide fanout is a **data-correctness defect**, not a sound optimization.

## Test and cost protocol
Record snapshot ID, input rows, output key-level checksum, SQL semantics and role; change one plan/layout setting; compare multiple representative runs, spilled bytes, shuffle IO, runtime and DBU cost plus underlying cloud charges. Runtime and Photon availability gate the exact optimization. Retain rollback, release owner and alert.

Sources: https://docs.databricks.com/aws/en/optimizations/aqe and https://docs.databricks.com/aws/en/optimizations/
