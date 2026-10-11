# Warehouses — rightsize concurrency, credits and suspension safely

Read when: changing virtual warehouse size, autosuspend, cluster scaling, resource monitors or assigning Snowflake credits to a workload.

Separate CPU/memory size, overloaded query queue, suspend/resume provisioning, and billable credits. Increasing warehouse size may improve spilling or parallel scans; multi-cluster scale addresses different concurrency pressures and is edition/feature-dependent. Never assume a larger warehouse has lower credits per query. Resource monitors primarily address warehouse consumption, not every serverless/cloud service.

## Observe instead of assuming

Record workload class, query distribution and error rate; size and min/max clusters, auto-suspend and resume, time of day, active users, credits, data freshness and business p95. Snowflake bills warehouse runtime per second with a minimum charge after starting; turning off auto-suspend may cost more, while aggressive suspend/resume can also create minimum-billing churn. Official docs suggest tuning based on observed workload gaps, not hardcoding 60 seconds universally.

Read-only aggregate example:

~~~sql
SELECT WAREHOUSE_NAME, DATE_TRUNC('day', START_TIME) AS USAGE_DAY,
       SUM(CREDITS_USED) AS WAREHOUSE_CREDITS
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD(day, -14, CURRENT_TIMESTAMP())
GROUP BY 1,2
ORDER BY 2 DESC, 1;
~~~

View availability/latency and credit subcategories need verification. This does **not** represent whole account cost: Snowpipe, Dynamic Tables, Cortex, storage and other serverless features may add charges. Credit to currency requires account contract/region.

## Attribution and safe trials

Warehouse-level credit totals differ from per-query marginal attribution on a shared concurrent warehouse. Avoid a simplistic duration × warehouse size formula for shared sessions. For proposed changes, keep comparable load and run time; compare time, total credits, queueing and collateral regression, not just one query's peak speed. Set bounded budget, rollout owner, off-hours or disposable warehouse and rollback.

~~~text
HYPOTHESIS: spill is primary driver, one-size increase might reduce p95
PRECHECK: representative operator / concurrency / memory metrics
CHANGE: sandbox warehouse size for fixed runs, not production by default
SUCCESS: same SQL result, p95 under target and credits within cap
FAILURE: latency unchanged, spend excessive, other workloads suffer
STOP: rollback and choose SQL/data-layout approach
~~~

Sources: https://docs.snowflake.com/en/user-guide/warehouses-considerations and https://docs.snowflake.com/en/user-guide/cost-controlling-controls and https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history
