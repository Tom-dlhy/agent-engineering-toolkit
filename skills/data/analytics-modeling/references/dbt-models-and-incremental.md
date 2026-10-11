# dbt model layers, tests and incremental contract

**Read when:** implementing staging/intermediate/marts in dbt
or selecting view/table/incremental materialization.

## Model responsibility
Source: raw ingestion snapshot with provenance.
Staging: clean/cast/rename source fields, minimal reusable
business interpretation.
Intermediate: join/reuse reusable business logic.
Mart: entity/fact/dimension grain serving analysts/BI.
The dbt official guide describes these layers; copying
all transforms into staging or making one large SQL query
hides testability and lineage.

## Incremental model (dbt pseudocode)
~~~sql
{{ config(materialized='incremental', unique_key='order_id') }}
select order_id, amount_minor, source_updated_at
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where source_updated_at >=
  (select coalesce(max(source_updated_at), '1900-01-01')
   from {{ this }})
{% endif %}
~~~

This is illustrative and incomplete: timestamp window misses
late arrivals older than max; source duplicate order_id may
break merge; deletes and corrections require policy. dbt's
unique_key is not necessarily DB unique constraint; validate
source/target uniqueness and null keys. dbt is_incremental()
only true for existing incremental table with no full-refresh.
A compatible full-refresh SQL path is required.

## Data tests and contract
Use not_null/unique/relationships and accepted_values for
useful guardrails; custom SQL for business invariant (e.g.
invoice line sum = invoice amount). Consider model contracts
and documented column/types where supported on actual
adapter version. Tests of source freshness and late-data
detection are separate from static build success.

## Review
Version dbt Core, adapter and warehouse; confirm incremental
strategy (merge, delete+insert, insert_overwrite, microbatch)
actually supported and whether it uses unique_key. Validate
delete propagation, backfill, full refresh and correction
arriving outside lookback under controlled fixture.

Sources: https://docs.getdbt.com/docs/build/incremental-models ,
https://docs.getdbt.com/docs/build/data-tests ,
https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview .
