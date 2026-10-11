# Time-aware model evaluation, reproducibility and operational monitoring

Read when: assessing Snowflake ML score quality over time, promoting a registry version, explaining drift or running retraining safely.

## Evaluation population and anti-leakage

Write a versioned dataset manifest: prediction grain, eligibility, observation months, target horizon, label maturity, available features, dedupe, cohort and missingness. Split by time with an embargo appropriate to forecast horizon when overlap would leak outcomes. Keep final holdout untouched during hyperparameter/feature experimentation.

For acquisition propensity or moving probability scores, ranking metrics like recall@top 30%, precision@K, lift and stability per monthly cohort can be more decision-aligned than accuracy. Define denominators and target prevalence. Keep a trivial baseline, compare paired scoring populations, and inspect subgroup/temporal variability. A positive average delta is not evidence of sustained uplift if one month collapses.

## Separate three layers of evidence

1. **ML quality:** accuracy/ranking/calibration under labeled holdout, with confidence/variance.
2. **Operational fitness:** inference completeness, latency, failures, cost, feature freshness, model version lineage, score distribution.
3. **Business impact:** incremental conversions/action value from a properly designed experiment or credible quasi-experiment; offline recall alone does not prove value.

Do not silently compare one model trained on 2024 data with another evaluated on an updated label definition. Store label creation SQL and relevant source snapshot/version. Drift may be genuine behavior change, pipeline break, missing source or schema mismatch: detect which before retraining.

## Registry and monitoring lifecycle

Record immutable model version, source revision, training environment, seed and hyperparameter search, exact training/test windows, input signature, feature query version, metrics by segment/month and permission owner. Define who can log models, who can promote/deploy and who can access inference. Snowflake ML Observability supports performance/drift monitoring, but availability and signal maturity vary; verify edition/region/API at use time and don't treat “monitor enabled” as actual working alert coverage.

Trigger-based decision table:
- Prediction distribution shift with stable sources → review drift and target maturity.
- Large NULL/missing jump in feature input → stop scoring/reconcile pipeline before retraining.
- Recall@K degradation on matured labels across multiple months → investigate data, domain shift, calibration/threshold and candidate retraining.
- New registry version has signature mismatch → block deployment.
- New model has p95 latency/cost outside budget → rollback or rearchitect inference.

## Incident/recovery example

A new LightGBM version scores 0 rows on one monthly partition. Do **not** claim model drift. Reconcile score input rows and keys, inspect feature transform cutoffs and model version/signature, verify inference errors, compare previous pinned model on same input and restore the last known-good scoring job if authorized. Record partial publication, fix cause and rerun negative fixture.

## Deliverables

Provide dated evaluation report with exact cohorts/denominators, training and scoring manifest, registry version, metric variability, production feature SLI, failed cases, cost and human promotion/rollback authority. Any test not executed is marked UNRUN and any missing model access is stated.

Sources: https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview and https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/inference-overview and https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering
