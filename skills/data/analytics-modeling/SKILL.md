---
name: analytics-modeling
domain: data
version: "0.1.0"
description: >-
  Use when building analytics marts, star schemas, dbt models,
  fact/dimension grain, slowly changing dimensions and consistent
  business metrics. Do not apply to OLTP key design, lakehouse
  storage format or generic DAG retry orchestration.
---

# Analytics modeling — grain before joins, metrics before charts

## Decision method
1. Define the business question and **grain**: what exactly constitutes
   one row of a fact, at what event time and under which source version?
2. Separate facts (measures at declared grain), conformed dimensions,
   bridge relationships and degenerate identifiers. Prevent fanout
   double counting before adding aggregates or BI measures.
3. Identify event time versus observation/load time, mutable dimensions,
   SCD type 1/2 treatment, surrogate keys and unknown/late dimensions.
4. Organize SQL/dbt layers (source → staging → intermediate → mart) by
   responsibility. Avoid arbitrary one-file-per-table transformations.
5. Define additive/nonadditive metrics, numerator/denominator, date
   window, timezone, nulls, populations and ownership once; distinct
   counts across dimensions often cannot be summed.
6. Implement incremental materializations only with tested unique key,
   late-arrival lookback, delete/correction semantics and a safe full
   refresh/reconciliation path. An incremental job going green doesn't
   prove historical accuracy.
7. Validate grain uniqueness, joins, reconciliation, time travel and
   metric invariants on fixtures with duplicates/late/corrected rows.

## Reference routing
- [Star schemas and grain discipline](references/facts-dimensions-and-grain.md) —
  **read when** selecting fact types, dimensional design and join safety.
- [dbt models, tests and incremental semantics](references/dbt-models-and-incremental.md) —
  **read when** building marts or incremental SQL transforms.
- [Metrics, historical dimensions and QA](references/metrics-scd-and-reconciliation.md) —
  **read when** implementing business metric contracts, SCD2 or BI semantic layers.

## Boundaries
database-design owns transactional relations and constraints;
data-pipeline-quality owns run-level data quality/freshness;
lakehouse-engineering owns columnar storage/warehouse efficiency.

## Exit
Grain/keys and metric specification, testable reconciliation,
documented late changes and measured warehouse costs.
