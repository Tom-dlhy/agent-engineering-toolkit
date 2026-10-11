---
name: snowflake-snowpark-ml
domain: data-platforms
version: "1.0.0"
description: >-
  Use when building, training, versioning, deploying or diagnosing Snowpark Python and Snowflake ML workflows, including LightGBM/XGBoost, Model Registry, inference, feature views and drift monitoring. Do not use for generic local sklearn training, unrelated model quality scoring or Cortex LLM Agents.
---

# Snowflake Snowpark ML — reproducible features to governed inference

## Mission

Make a Snowflake-native ML workload reproducible and operationally safe: point-in-time data validity, deterministic feature and target definitions, version-pinned training environment, meaningful evaluation and traceable model inference. Distinguish **Snowpark DataFrame execution**, Snowflake ML modeling, external Python training, Model Registry, feature store and serving. A model logged in the registry is not automatically approved or deployed.

## Intake and feature/target contract

1. Inspect actual Snowflake edition/region, role and compute permissions, dataset volumes, warehouse execution, training environment and installed snowflake-ml-python/Snowpark/Python version. Pin dependencies; current APIs and extras change.
2. Define prediction task, entity key, observation timestamp, future target horizon, population/opt-in and leakage boundary. For rolling historical scoring, split by **time**, hold out meaningful periods and use point-in-time joins, not random split across future information.
3. Distinguish feature computation timestamp and availability timestamp from event time. Audit features whose timestamps, future aggregates or post-outcome updates could leak target information.
4. Establish baseline and ranking metrics (e.g. recall@top-K, precision@K, PR-AUC where appropriate), stability per period, calibration, fairness/privacy where material and representative unseen cohorts. Do not claim that model metrics alone show business value.

## Train, log and deploy

- Implement reusable Snowpark transformations or versioned SQL feature tables. Push appropriate operations to Snowflake; avoid uncontrolled collect/to_pandas on large or sensitive tables.
- Train on a **pinned** environment, preserve seed/config, data snapshot/query IDs, feature list/order, hyperparameters and train/validation partitions. Optuna or HPO must not repeatedly evaluate on final holdout.
- Registry contract: log a supported model with explicit version and sample_input_data or signatures when required. LightGBM sklearn wrapper and native Booster expose potentially different target methods; validate predict vs predict_proba availability.
- Validate signature schema, dtype, NULL/order behavior, representative offline versus in-Snowflake inference, row-to-entity joins and scoring reproducibility. Avoid magic concatenation of input columns without a stored feature contract.
- Decide serving mode: batch warehouse inference, supported REST/container serving, feature store and latency/cost constraints from **real** workload and availability, not presumed universal endpoints.
- Promotion needs artifact immutability, metadata, current scoring behavior, rollback version and a human-governed release gate. Drift monitoring needs prediction distribution, feature shift, target maturation delay and actual outcome feedback.

## References

- [Feature/label time semantics and Snowpark execution](references/feature-time-and-snowpark.md) — **read when** building point-in-time scoring bases and nonleaky features.
- [Train/log/registry compatibility and inference contracts](references/model-registry-and-inference.md) — **read when** using LightGBM, snowflake-ml-python, versions and production scoring.
- [Evaluation, experiment lineage, promotion and drift](references/evaluation-lineage-and-operations.md) — **read when** comparing models over time or planning registry promotion/monitoring.

## Handoffs

data/analytics-modeling owns metric grain; data/data-pipeline-quality owns generic data tests; ai/llm-evaluation covers generative agent/prompt evaluation; data/lakehouse-engineering owns storage format. Here: **Snowpark ML and registry-specific lifecycle**. Snowflake Cortex Agents/Analyst/Search belong to snowflake-cortex-ai. No production registry overwrite or inference service deployment without authorization.

## Finish

Return dataset/temporal split manifest, feature/target contract, training configuration, algorithm and metrics with cohorts, model signature and version, security/compute plan, comparison versus baseline and safe rollback. No fabricated registry version or claims about training actually run.
