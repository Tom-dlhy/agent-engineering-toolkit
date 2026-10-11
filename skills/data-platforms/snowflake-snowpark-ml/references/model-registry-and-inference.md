# Snowflake ML Model Registry and LightGBM inference compatibility

Read when: logging, retrieving, predicting with or deploying a Snowflake ML model, including LightGBM and Snowpark registry methods.

## Version and model-type gate

Record Python version, Snowpark Python, snowflake-ml-python and framework versions, account features/edition, model type, signature schema, trained preprocessing, and target runtime (warehouse batch or container serving). Pin in a lock/env file; package release notes may alter optional extras, default signatures and inference method options.

Snowflake Model Registry manages versioned first-class model objects. Models may be logged from LightGBM sklearn wrapper (LGBMClassifier/LGBMRegressor) or native Booster, but **their available method names differ**. A classifier's predict_proba is not interchangeable with native Booster predict; check actual exported methods and expected probability/class outputs.

For LightGBM, current Snowflake docs require sample_input_data **or** explicit signatures at log time. Input feature order/names/types and nullable behavior must match downstream inference. The registry can infer placeholder feature names from arrays; store and check a real feature contract rather than assuming order by SELECT *.

## Example — illustrative API structure, not an executed deployment

~~~python
from snowflake.ml.registry import Registry

# session: preexisting authorized Snowpark Session
# model: pre-trained supported LightGBM model; samples: representative
# pandas/Snowpark frame with stable feature names/types and no labels
reg = Registry(session=session, database_name="DEV_DB", schema_name="ML_REG")
mv = reg.log_model(
    model=model,
    model_name="RISK_SCORE",
    version_name="V2026_10_TEST",
    sample_input_data=samples,
    comment="Sandbox evaluation only; not promoted",
)
# Check the methods available on mv for this model before invoking.
# E.g. mv.run(scoring_features, function_name="predict") where supported.
~~~

Do not run this in production or overwrite a model version without explicit approval. The snippet intentionally relies on existing safe session/model objects and requires pinning exact API at use time. Snowflake Registry objects may differ from model class wrappers and external MLflow registries. Keep train artifacts, training-data snapshot, model metrics and input schema as lineage metadata, with PII-safe handling.

## Inference options

| Path | Good for | Validate |
|---|---|---|
| Batch in Snowflake warehouse / SQL | Large periodically refreshed scores | Runtime support, deterministic joins, warehouse credits |
| Python Snowpark/pandas through ModelVersion | Offline/small validation and scheduled scoring | DataFrame type, schema and method name |
| Snowpark Container Services / REST serving | Online latency or specialized compute | Provisioning, model versions, endpoint authorization, cost |
| External application inference | Existing service + model portability | Data transfer, feature parity, signature/version pinning |

Ensure result row counts and entity mapping; a batch inference returning N rows that join incorrectly to input keys can create silent incorrect scores. Compare a sample scoring run in both environments under same model version and feature order; verify error outputs, nulls and concurrency.

## Production promotion gate

Training success → log immutable version → registry method/signature inspection → negative schema tests → batch score parity → business ranking/per-period validation → privacy/security review → approved promotion → monitoring/drift and rollback. Avoid a mutable “latest” model pointer without deployment record.

Sources: https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview and https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/lightgbm and https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-signature and https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/inference-overview
