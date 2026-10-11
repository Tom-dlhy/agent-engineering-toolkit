# Lakeflow AUTO CDC, SCD and data quality expectations

Read when: applying CDC events or snapshot differences to Databricks streaming tables, handling SCD1/SCD2 or declaring row expectations.

## Choose an accurate change source
AUTO CDC reads a true CDC feed with stable keys and ordered sequence; AUTO CDC FROM SNAPSHOT compares successive consistent source snapshots. Do not infer deletes from absent records in a partial incremental export. AUTO CDC supersedes older APPLY CHANGES syntax for new work (legacy remains supported). Newer bitemporal features can be beta; check exact API before choosing.

## Define semantics explicitly
- KEYS: entity identity; uniqueness of source event identity vs target row;
- SEQUENCE BY: **source-order** field, not arrival/processing timestamp by convenience. Ties must be resolved or rejected;
- APPLY AS DELETE WHEN: source deletion vs logical false flag;
- SCD TYPE 1: latest surviving business state;
- SCD TYPE 2: preserved historical version ranges with effective times;
- IGNORE NULL UPDATES: absent field versus intentional clear-to-NULL, only if producer supports correct distinction;
- schema: type drift, missing fields, rescued data and publisher compatibility.

A SQL outline is illustrative; test against current Databricks SQL syntax and source type in a disposable catalog:

~~~sql
-- SANDBOX REVIEW ONLY: not a runnable production replacement.
-- CREATE OR REFRESH STREAMING TABLE target_table;
-- CREATE FLOW orders_cdc AS AUTO CDC INTO target_table
-- FROM STREAM(source_changes)
-- KEYS (order_id)
-- SEQUENCE BY event_sequence
-- APPLY AS DELETE WHEN is_deleted
-- STORED AS SCD TYPE 2;
~~~
Do not blindly use a column that can repeat as ordering. A legacy APPLY CHANGES flow should not be migrated without backfill/state and downstream history checks.

## Expectation decision
| Violation | Possible policy | Safety condition |
|---|---|---|
| Optional noncritical field missing | Warn/report | Data consumer accepts partial record |
| Corrupt payload | Quarantine/drop | Quarantine is durable and reconciled |
| Missing key/finance amount | Fail update | Owner approves blocked publish |
| Late event correction | Process deterministically | SCD version and valid time tests |
| Source not arriving | Freshness alert | Do not mark stale output green |

Databricks Lakeflow expectations evaluate row predicates and can produce WARN/DROP/FAIL behavior. They cannot by themselves prove relationships between tables or accounting totals; add pipeline-level reconciliation.

## Negative fixtures
Out-of-order CDC, duplicate same-key event, delete after insert, update after delete, partial record, null overwrite and checkpoint recovery. Verify row set and **history intervals** for SCD2, not just count. Always return actual vs expected results and mark unexecuted tests UNRUN.

Sources: https://docs.databricks.com/aws/en/ldp/cdc and https://docs.databricks.com/aws/en/ldp/best-practices and https://docs.databricks.com/aws/en/ldp/developer/ldp-sql-ref-apply-changes-into
