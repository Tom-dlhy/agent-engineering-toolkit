# MLflow Model Registry in Unity Catalog — versioned serving with compatibility tests

Read when: logging/registering models in Unity Catalog, using aliases/versions, selecting real-time vs batch inference or migrating Workspace Registry.

## Model registration is not serving
Determine actual MLflow/DBR version, feature set, Workspace vs UC registry, owning catalog/schema and model privileges, environment lock, signature and serialized artifacts. UC models use three-part names and versioned artifacts. Avoid mutable unspecified “latest” in a production scoring job; record exact model version or a tightly controlled alias with traceable rollback.

Illustrative MLflow 3 registration pattern (no provider request performed):
~~~python
import mlflow
# Requires an already created, authorized MLflow 3 LoggedModel and UC grants.
# mlflow.set_registry_uri("databricks-uc")
# mlflow.register_model("models:/<logged_model_id>", "dev_catalog.ml.risk_score")
# Verify current MLflow version docs and exact model ID source before use.
~~~
The commented command is not a runnable model deployment. Do not invent model_id, version, stage names or privilege readiness. MLflow 2 run-based URI syntax is not automatically a drop-in replacement in every new model-first path.

## Serving decision
- Batch scoring: scheduled Spark/SQL workload and UC data permissions; validate entity-to-score row mapping and processing volume.
- Online endpoint: actual model-serving support, endpoint access tokens, rate, cold start, latency, scaling and billing; compatibility with feature retrieval.
- External inference: application-owned API contract, data residency and provider approval.
- GenAI/agents: MLflow versions and tracing; runtime service policies delegated to Unity Gateway.

## Promotion gate
~~~text
IMMUTABLE TRAINING + MODEL VERSION
 -> SIGNATURE / TYPE / FEATURE ORDER TESTS
 -> REPRESENTATIVE BATCH/ONLINE PARITY
 -> ROLE DENIAL / PII / INPUT VALIDATION
 -> COST + LATENCY + BUSINESS HOLDOUT
 -> OWNER AUTHORIZATION
 -> SERVE WITH VERSION/ALIAS AUDIT
 -> MONITOR + ROLLBACK
~~~

A successful registry registration is not proof the serving endpoint exists; a model endpoint responding 200 isn't proof every output is correct. Preserve previous model and reversible client routing. Don't infer that aliases/stages behave identically between Workspace and UC registries.

Sources: https://docs.databricks.com/aws/en/mlflow/models and https://docs.databricks.com/aws/en/mlflow/model-registry-3 and https://docs.databricks.com/aws/en/mlflow/mlflow-3-install
