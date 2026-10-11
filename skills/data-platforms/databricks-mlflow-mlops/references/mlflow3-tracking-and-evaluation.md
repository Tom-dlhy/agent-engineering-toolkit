# MLflow 3 experiment tracking, data lineage and task-specific evaluation

Read when: upgrading MLflow 2 to 3, comparing registered ML/GenAI models, recording inputs, prompts, runs and evaluation scores.

## Reproducibility contract
Snapshot model input feature definitions, observation timestamps, label horizons, row keys and train/validation/holdout windows. A model trained on post-observation data leaks target information even when registered correctly. Preserve dataset version/source query, code SHA, framework and Python versions, random seed, parameters, evaluation cohort and privacy-safe metrics. Don't upload raw sensitive training examples or tool traces into a shared experiment.

## Important MLflow 3 distinctions
- MLflow 3 introduces/uses LoggedModel identifiers as a model-first workflow in addition to experiment runs; registry and model IDs differ from MLflow 2 run-relative artifact paths.
- In suitable Databricks contexts, default registry URI is databricks-uc; register with exact catalog.schema.model and version.
- Older top-level mlflow.evaluate is deprecated: for ordinary ML use **mlflow.models.evaluate**; for GenAI use **mlflow.genai.evaluate**. Pin selected MLflow version before copying an example.
- MLflow 3 may read many MLflow 2 artifacts, but MLflow 2 may not fully understand newer objects. A migration needs compatibility testing and rollback.

## Experiment gate
1. Define a baseline and holdout dataset; separate model tuning from final evaluation.
2. For classification: target prevalence, recall/precision@K, calibration, group/time slices and confidence. For GenAI: grounding, abstention, tool safety, citation evidence, tokens/cost.
3. Record errors by severity; never allow an aggregate judge score to hide unauthorized access.
4. Verify signature schema/type, missing values and inference parity.
5. Mark the approved model version and promotion owner explicitly. MLflow run successfully logged != release.
6. Hold out redacted inputs; do not evaluate secretly on model training samples or change a gold set to make a new model look better.

## Failure example
A daily propensity score improves “accuracy” but target prevalence changed; it may worsen recall at operational contact budget. Compare same population/month and positive count, then inspect rank metrics and per-month variance. If data lineage is missing, label the result **incomparable**, not improved.

Sources: https://docs.databricks.com/aws/en/mlflow/mlflow-3-install and https://docs.databricks.com/aws/en/mlflow/model-registry-3 and https://docs.databricks.com/aws/en/mlflow/models
