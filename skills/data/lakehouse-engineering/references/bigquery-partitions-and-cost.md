# BigQuery partition, cluster and on-demand query cost

**Read when:** designing BigQuery physical layout, optimizer
pruning, query bytes, reservations or bill controls.

## Query price depends on model
On-demand BigQuery queries charge by data processed;
capacity/reservation billing follows slots/commitments.
Storage has its own billing/retention model. Query LIMIT
does **not** generally reduce bytes scanned from a
non-clustered table. Use dry runs/maximum_bytes_billed
and actual estimates where supported to protect budgets.

## Partition vs cluster
Partition by commonly filtered time/ingestion/range
when it allows pruning and useful retention. A qualifying
filter enables planner to skip other partitions. Too
many tiny partitions increase metadata/ops overhead,
so consider clustering by high-cardinality filter
columns instead or alongside partition. Cluster
column *order* matters for block pruning; estimates
for clustered bytes can be upper bound before execution.

## Example SQL (illustrative)
~~~sql
CREATE TABLE mydataset.events
PARTITION BY DATE(event_at)
CLUSTER BY customer_id, event_type
AS SELECT event_at, customer_id, event_type
FROM mydataset.staging_events;
~~~
This creates/replaces storage at cost and isn't a
drop-in production migration; check dataset location,
permissions, table creation syntax and safe destination.
Use read-only dry run/EXPLAIN-style plan before materialization.
Avoid date-suffixed sharded tables where native partition
is supported and a better fit.

## Test and operate
Inspect INFORMATION_SCHEMA job history/table storage,
actual bytes billed and bytes scanned, p95 latency,
partition pruning on real filters, clustering effects,
cost guard failures and background streaming buffer.
Measure region, quotas and reserved capacity; pricing
can change over time and is not a constant from memory.

Sources: https://docs.cloud.google.com/bigquery/docs/best-practices-costs ,
https://docs.cloud.google.com/bigquery/docs/partitioned-tables ,
https://docs.cloud.google.com/bigquery/docs/clustered-tables .
