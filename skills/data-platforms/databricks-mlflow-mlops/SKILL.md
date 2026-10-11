---
name: databricks-mlflow-mlops
domain: data-platforms
version: "1.0.0"
description: >-
  Use when implementing Databricks MLflow 3 tracking, governed Unity Catalog Model Registry, model/agent evaluation, reproducible training, serving, tracing or drift monitoring. Do not use for Snowflake Model Registry, generic LLM inference APIs, Spark query tuning or Unity Gateway-only runtime policy.
---

# Databricks MLflow MLOps — reproducible evidence, registered versions and safe serving

## Mission

Control Databricks MLflow/ML model lifecycle from source and feature availability through training, evaluation, registry, serving, monitoring and rollback. The user owns deployment authority. A “best” notebook metric is not a release decision, and a registry version does not imply serving permission or model correctness.

## Compatibility gate

1. Inspect account cloud, workspace/metastore and grants, compute, exact MLflow/DBR versions and whether use case is classical ML or GenAI agent. Treat MLflow 2.x snippets as **versioned legacy**, not interchangeable with MLflow 3 APIs.
2. MLflow 3 defaults Unity Catalog registry URI to **databricks-uc** where supported; use fully qualified catalog.schema.model registration and explicit model version, never ambiguous "latest". Workspace Model Registry remains a legacy distinct configuration.
3. MLflow 3 uses LoggedModels/Model IDs in addition to runs; check signature, input example and reproducible packaging. For classic models use **mlflow.models.evaluate**; for GenAI apps use **mlflow.genai.evaluate** rather than deprecated top-level mlflow.evaluate.
4. Separate experiment and workspace access from the actual data/model/endpoint privileges. An evaluator must not gain full data warehouse access just to log trace metrics.

## End-to-end method

- Define population, target, observation/feature available-at timestamps, leakage embargo and train/validation/holdout split appropriate to business horizon.
- Pin code git SHA, dependencies/conda environment, seeds, hyperparameters, feature pipeline and input schema. MLflow run/LoggedModel should reference a reproducible source snapshot; do not log raw personal data into parameters or traces.
- Compare a baseline with confidence/segmented cohort metrics: rank, calibration, feature robustness or GenAI groundedness and tool misuse; guard safety failures independent of average score.
- Register in Unity Catalog with exact three-level name, immutable model version and typed signature. Prefer controlled aliases/deployment references and verify behavior in supported runtime rather than changing live model names.
- Validate offline versus serving outputs on identical schema, row keys, missing/null and representative size; online endpoints may have different latency/compute quotas and auth.
- Observe drift, label-maturation lag, error/fallback, inference costs, model/agent trace privacy; MLflow 3 production monitoring may be beta/region limited. A monitor configured without real sample/scorer verification is not proof of surveillance.
- Gate promotion on reviewed artifact, independent test, security/privacy owner and rollback to known-good version. Never deploy paid serving endpoint automatically.

## References

- [MLflow 3 experiments, evaluation and leakage](references/mlflow3-tracking-and-evaluation.md) — **read when** changing MLflow APIs or experiment lineage.
- [Unity Catalog Model Registry and controlled serving](references/uc-model-registry-and-serving.md) — **read when** publishing or invoking models and selecting aliases/versions.
- [Monitoring, tracing and staged rollouts](references/monitoring-tracing-and-rollout.md) — **read when** tracking regressions and online risk.

## Specialist boundaries and completion

databricks-unity-catalog owns securable model/grant definitions, databricks-ai-governance governs runtime model/agent traffic through Unity Gateway, ai/llm-evaluation owns provider-neutral evaluation methodology, databricks-spark-delta owns physical feature-engineering plans.

Return train/source manifest, MLflow version and artifact IDs if verified, UC registry identity, signature, held-out metrics with denominator, actual/UNRUN serving results, cost/approval and rollback. No invented run IDs, traces, trained models or endpoint state.
