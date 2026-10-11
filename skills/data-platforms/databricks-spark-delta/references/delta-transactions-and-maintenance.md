# Delta transaction safety, schema/CDF and file retention

Read when: updating a Delta table, enabling change data feed, migrating schema/protocol, restoring a version or handling concurrency and VACUUM.

## Table format is a compatibility contract
Capture protocol reader/writer features, DBR versions of **all readers and writers**, table owner, Unity Catalog managed/external location, streaming consumers, time-travel expectation and privacy retention. Delta table features such as deletion vectors, column mapping or change data feed have specific compatibility and retention semantics. A new writer feature can render older readers unable to access data.

Concurrency and MERGE require deterministically unique source matches; deduplicate by business key and ordered version. Define deletes/tombstones, null update behavior and out-of-order corrections. Some Delta MERGE options and schema evolution depend on DBR/API version. Rehearse on disposable tables.

## Conceptual SQL inspection (no mutation)
~~~sql
DESCRIBE DETAIL dev_catalog.analytics.orders;
DESCRIBE HISTORY dev_catalog.analytics.orders;
-- Use the recorded schema, table features, versions and retention settings
-- to design and APPROVE a migration before any ALTER, MERGE or VACUUM.
~~~
These queries require an authorized workspace and grants; no such request was executed as part of this skill.

## Destructive operations and recovery
- OPTIMIZE rewrites files but should retain transactional reader correctness if supported; measure compute and concurrent write behavior.
- VACUUM removes files beyond retention; shortening retention can break long-running readers, streaming checkpoints, restore and time travel. Never blindly disable retention checks.
- RESTORE / history cannot recover files already physically vacuumed. A table history entry is not a backup.
- CDF requires carefully coordinated start version/timestamp and source retention; an expired version can require resnapshot, not silently restarting with a newer offset.
- External storage cleanup and Unity Catalog governance are separate from Delta log semantics.

## Negative cases
Test same-version duplicate keys, concurrent MERGE, schema type drift, delayed deletion, missing checkpoint, old client reader, corrupted/expired source version and permissions lost during restore. A correct query post-migration and an explicit rollback exercise are mandatory before calling the change production-ready.

Sources: https://docs.databricks.com/aws/en/delta/ and https://docs.databricks.com/aws/en/delta/history and https://docs.databricks.com/aws/en/delta/delta-change-data-feed
