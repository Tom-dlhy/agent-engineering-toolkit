# Business metrics, SCD dimensions and reconciliation

**Read when:** defining BI KPIs, historic dimension joins,
non-additive measures or cross-report disagreements.

## Metric as contract
Define name, owner, grain, source version, numerator,
denominator, date cohort/event window, filters/exclusions,
currency and timezone, invalid data policy, rounding and
change control. A "conversion rate" has no universal
meaning until conversion event, population and exposure
window are defined. Document semantic version/deprecation
for dashboards and API consumers.

## Aggregation rules
Additive amounts count over allowed dimensions at same
grain. Inventory balance is semi-additive over time;
a percentage/median/distinct users cannot generally
be summed across groups. Weighted aggregation depends
on underlying numerator/denominator, not average
of previously rounded ratios.

## SCD
Type 1 overwrites correction, appropriate when historical
version is intentionally irrelevant. Type 2 creates
effective-dated dimension versions for historic reporting.
Enforce one active current version per business key,
non-overlapping [valid_from, valid_to) ranges and
late arriving facts join to the appropriate effective row.
A naive join only by customer ID can duplicate facts
across multiple type-2 versions.

## QA
Two valid SCD2 versions; overlapping effective ranges
must fail. Late fact after a dimension correction;
historical reports remain reproducible or explicitly
restate according to business policy. Distinct user
metric across overlapping countries must not double
count. Totals reconcile source to mart at declared grain.

## Operational concern
Metrics change management, lineage and audit support
trust: keep definition/test outcomes with data release
and specify which dashboards need backfill on correction.
Do not claim semantic correctness because dbt tests all pass.

Sources:
https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/ ,
https://docs.getdbt.com/docs/build/data-tests .
