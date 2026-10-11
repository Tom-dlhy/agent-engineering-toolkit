# Analytical grain, fact/dimension design and join integrity

**Read when:** building data marts, business fact tables,
conformed dimensions, BI joins or star schemas.

## Grain before table shape
Write an explicit sentence: "one row represents one invoice
line at issuance time" or "one row represents one account at
monthly observation date". Grain determines unique key and
valid aggregation. Facts can be transactional events,
periodic snapshots or accumulating lifecycle snapshots;
don't confuse these with OLTP normalized entities.

Dimensions carry descriptive context, often surrogate key,
possibly history. Conformed dimensions require genuinely
shared business definitions; similar column names don't
ensure identical meaning. Bridge tables for many-to-many
relationships need weighting or explicit rollup rules to
avoid multiplying measures.

## Fanout error example
Invoice 100 euros has two line records and three
customer-tag rows. Joining invoice -> lines -> tags
produces six result rows, and SUM(invoice.total) may
give 600. Fix grain before aggregation, preaggregate
by invoice, or use correctly weighted bridge. DISTINCT
on arbitrary columns is not a universal repair and
may undercount legitimate repeated values.

## Fact tests
- Primary grain uniqueness at declared keys.
- No missing dimension keys or explicit "unknown" policy.
- Total before/after join reconciles at stable source grain.
- Null/zero/refund and currency semantics valid.
- SCD historical join chooses dimension version valid
  at fact event time, not just latest dimension version.
- Cardinality negative fixture duplicates dimension keys
  and must trigger failure instead of inflating metric.

## Time and identity
UTC event timestamp vs local reporting date and timezone
are distinct. Document whether corrections alter historic
values and which source version was used in metric computation.
A daily cohort table using observation date cannot
automatically be interpreted as event transaction fact.

Sources:
https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/ ,
https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview .
