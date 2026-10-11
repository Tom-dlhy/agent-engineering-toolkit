# Delta physical layout — liquid clustering and predictive optimization

Read when: selecting data layout, maintenance schedule, cluster size, compute type and total cost for Delta analytic tables.

## Choose based on filter distribution and maintenance
For new eligible Delta tables, Databricks recommends **liquid clustering** over static partitioning and ZORDER. Check DBR support (Delta GA from DBR 15.4 LTS), table protocol and other readers. Liquid clustering and partitioning/ZORDER are not used together on the same table. Altering keys does not immediately re-layout all old files; incremental OPTIMIZE or appropriate FULL operation and runtime restrictions govern rewriting.

Predictive optimization on eligible UC-managed tables can automatically OPTIMIZE and perform housekeeping. Running separate scheduled OPTIMIZE over these tables may duplicate cost. External tables may require operator-managed maintenance.

## Before/after diagnostic matrix
| Strategy | When valuable | Hazard |
|---|---|---|
| No custom clustering | Small or uniformly scanned table | Maintenance outweighs gains |
| Liquid clustering | Changing filters/skew/high cardinality | Runtime compatibility, rewrite costs |
| Static partitioning | Legacy layout and proven pruning | Many small partitions and update cost |
| ZORDER | Existing non-liquid Delta strategy | Can't combine with liquid clustering |
| Predictive optimization | Supported UC-managed table | Verify what actually ran and bill |
| Larger compute / Photon | Execution dominates rather than file pruning | DBU price vs gain; feature compatibility |

## Safe measured experiment
~~~text
QUERY SET: sample of production patterns, with business expected output
TABLE: disposable copy under permitted workspace with exact DBR version
BASELINE: files, size, data skipping, p50/p95, task skew, DBU
CHANGE: select layout/OPTIMIZE only after expense and SLA review
EQUIVALENCE: key count, null semantics, aggregates and ACL
POST: same queries/concurrency, read latency + refresh/write credits
DECISION: cost-per-success and resource owner, revert if regressions
~~~

An OPTIMIZE that is faster for one dashboard but disrupts ingestion or costs more DBUs overall is not automatically desirable. Underlying storage, compute, job/serverless pricing and catalog effects must be measured rather than guessed.

Sources: https://docs.databricks.com/aws/en/delta/clustering and https://docs.databricks.com/aws/en/delta/optimize and https://docs.databricks.com/aws/en/sql/language-manual/delta-optimize
