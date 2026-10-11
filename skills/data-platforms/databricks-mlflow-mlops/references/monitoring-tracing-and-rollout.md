# Databricks MLflow monitoring — trace privacy, drift and controlled rollback

Read when: evaluating production ML/agent behavior or determining whether a newly registered model can replace an endpoint version.

## Three independent monitoring layers
- **Quality:** labeled holdout/per-month performance, calibration and counterfactual failures; for GenAI evaluate groundedness, harmful actions, abstention and multi-turn stability.
- **Operations:** request latency p50/p95, failure/refusal rate, input signature mismatches, rate limit, queue, model version, DBUs/tokens and feature freshness.
- **Business:** incremental decision value measured in an approved experiment, not inferred from offline model accuracy.

MLflow 3 includes online tracing and production monitoring/scorers; check exact regional and account status (production monitoring was documented Beta in Sep 2026). A configured monitoring job is not equivalent to a tested alert. Traces can contain prompts, retrieved docs, user identifiers or secrets: redact, sample and restrict access at collection.

## Drift diagnosis
Feature shift may be actual customer change, missing source column, out-of-order ingestion, new cohort mix or inference signature mismatch. Compare input key coverage, null rate, feature availability and data contract before retraining. Label horizon delay means today's predictions cannot be scored against tomorrow's ground truth.

## Canary/promotion rubric
1. Define stable baseline version, traffic allocation, duration and rollback policy.
2. Validate representative and forbidden inputs; verify service identity and feature permissions.
3. Observe cost, p95 and serious error counts; a single high-severity tenant leak blocks regardless of average score.
4. Assess confidence on matched cohorts; if insufficient sample size, report inconclusive.
5. Roll back route/alias under approved operator if quality/safety degrades; retain trace and data lineage for analysis.
6. Keep monitoring after promotion and refresh checks on schema/model changes.

## Negative cases
Malformed schema, missing feature, stale label, changed version/alias, prompt injection in retrieved tool data, wrong tenant output, rate/credit overage and no-traffic monitoring blind spot. Record executed vs simulated evidence.

Sources: https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/production-monitoring and https://docs.databricks.com/aws/en/mlflow/model-registry-3 and https://docs.databricks.com/aws/en/mlflow/mlflow-3-install
