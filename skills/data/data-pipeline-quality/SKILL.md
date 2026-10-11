---
name: data-pipeline-quality
domain: data
version: "0.1.0"
description: >-
  Use when building batch or streaming ETL/ELT pipelines, ingestion validation, freshness monitoring and data contracts. Do not use for one-off notebook exploration with no production data contract.
---

# data-pipeline-quality

## Contract
Define source ownership, schema, nullability, uniqueness, timestamp semantics, expected latency and downstream consumers. Version schemas and define behavior for breaking changes.
## Idempotence
Design re-runs and backfills using stable keys, watermarking and partitioning. Store lineage, retry state and failed-record samples without leaking protected data.
## Quality
Validate completeness, referential integrity, distribution drift, duplicate rate and freshness as appropriate; distinguish operational SLA failures from legitimate business seasonality.
## Tests and operations
Use representative fixtures, schema tests, pipeline integration tests and safe backfill dry-runs. Instrument row counts, lag, latency, task failures and recovery runbooks.
