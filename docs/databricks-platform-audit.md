# Databricks platform specialists — governance v2 and source audit

**Review date: 2026-10-12.** User explicitly authorized Databricks implementation following Snowflake PR #29. This is a newly authored platform-specific extension, **not** a third-party skills import. The external governance charter v2 remains outside this repository.

## Reuse / extend / create decision

| New skill | Independent job | Boundary and already owned mechanics | Verdict |
|---|---|---|---|
| databricks-spark-delta | Real Spark plan/shuffle/skew, Delta transaction, liquid clustering and measured compute costs | lakehouse-engineering chooses formats, analytics-modeling chooses fact grain | CREATE |
| databricks-lakeflow-pipelines | Auto Loader schema/state, Lakeflow flows, AUTO CDC, SCD, expectations and replay | data-pipeline-quality owns general contracts; streaming-cdc-engineering owns source Debezium/Kafka/Flink | CREATE |
| databricks-unity-catalog | UC securables, managed/external storage, governed-tag ABAC, workspace bindings, lineage and sharing | AWS/Azure/GCP cloud IAM handles cloud identities; privacy persona decides legal processing | CREATE |
| databricks-mlflow-mlops | MLflow 3 experiment/model/trace lifecycle, UC Model Registry, controlled serving | llm-evaluation owns model-agnostic rubrics; ai-governance owns runtime gateway | CREATE |
| databricks-automation-bundles | Bundles YAML, CLI/target/version compatibility, state migration and CI/CD | cloud/terraform covers external infra; quality/release-readiness owns general approval | CREATE |
| databricks-ai-governance | Unity Gateway model and agent/MCP runtime access, traffic, guardrails and spend | unity-catalog owns assets; mlflow-mlops owns model registry; agent-tool-safety owns universal trust rules | CREATE |

**REJECT separate micro-skills:** databricks-autoloader, databricks-autocdc, databricks-aqe, databricks-liquid-clustering, databricks-mlflow3-eval, databricks-abac and databricks-direct-deploy: all are appropriately owned by **one** deep reference each under the six primary skills. No monolithic databricks-expert and no duplication of Spark source capture or business metric modeling.

## Current official product/API distinctions

1. **Spark/Delta:** Adaptive Query Execution can coalesce partitions, change join strategy and address skew, subject to Spark plan/runtime. Liquid clustering is recommended for new eligible Delta tables, is incompatible with partitioning/ZORDER on the same table, and has DBR version requirements. Managed tables may use predictive optimization. Official: https://docs.databricks.com/aws/en/optimizations/aqe ; https://docs.databricks.com/aws/en/delta/clustering ; https://docs.databricks.com/aws/en/delta/optimize .
2. **Lakeflow:** Auto Loader provides durable file processing/checkpoint semantics for Delta writes, not business-key uniqueness across different files; changed checkpoint path restarts an independent stream. Schema evolution can stop a stream on addition and requires policy/restart. Lakeflow AUTO CDC succeeds APPLY CHANGES for new workloads, supporting SCD1/SCD2. Official: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/faq ; https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema ; https://docs.databricks.com/aws/en/ldp/cdc ; https://docs.databricks.com/aws/en/ldp/best-practices .
3. **Unity Catalog:** grants/ownership, governed-tag ABAC, table row/column policies and workspace bindings are complementary, not a single interchangeable access checkbox. Databricks recommends ABAC for broad tag-governed enforcement; requires supported compute (including serverless or suitable DBR 16.4+ mode). Official: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/ ; https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/requirements .
4. **MLflow 3:** defaults to UC registry URI in supported Databricks contexts. LoggedModels/Model IDs and model-level metadata extend previous run-based patterns; traditional model evaluation is via mlflow.models.evaluate and GenAI via mlflow.genai.evaluate. Production GenAI monitoring was labeled Beta in relevant Sept 2026 documentation. Official: https://docs.databricks.com/aws/en/mlflow/mlflow-3-install ; https://docs.databricks.com/aws/en/mlflow/model-registry-3 ; https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/production-monitoring .
5. **Bundles:** Databricks Asset Bundles renamed Declarative Automation Bundles on 2026-03-16; CLI bundle command remains. Direct deployment engine GA from CLI 1.3.0 for new bundles; existing state requires deliberate migration. Official: https://docs.databricks.com/aws/en/dev-tools/bundles/ ; https://docs.databricks.com/aws/en/release-notes/dev-tools/bundles .
6. **Unity Gateway:** current enterprise AI runtime gateway for model/provider services, agents, MCP tools, skills and governance. Endpoint AI Gateway docs are **legacy**. Gateway-level model access does not authorize individual tool side effects. Official: https://docs.databricks.com/aws/en/ai-gateway/ ; https://docs.databricks.com/aws/en/unity-gateway ; https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints .

## Documentation and catalog architecture

- Reuse existing **data-platforms** domain created for Snowflake, no new category.
- Six SKILL.md decision cores with three deep references each, progressive disclosure; no skill body is mandatory in installation profiles.
- Anticipated catalog after PR: **177 skills, 14 domains, 415 reference leaves, 20 unchanged profiles**.
- New source/safety docs, negative routing cases and *offline* deterministic CDC contract tests.
- No Databricks workspace, Delta table, MLflow experiment, cluster, provider key, paid API, SQL DDL or production job accessed or changed.
- No benchmark of real Spark/runtime behavior and no claim of verified Unity Gateway/UC enforcement: these require account-authorized integration and human review.

## Required non-collision tests

| Query intent | Owner | Must not hijack |
|---|---|---|
| PySpark SQL shuffle and Delta liquid clustering | databricks-spark-delta | generic PostgreSQL and Snowflake query profile |
| Lakeflow Auto Loader + CDC SCD2 | databricks-lakeflow-pipelines | source Debezium/Flink |
| UC governed tags / ABAC / workspace bindings | databricks-unity-catalog | AWS IAM trust policies |
| MLflow 3 models in Unity Catalog | databricks-mlflow-mlops | Snowflake Snowpark Model Registry |
| databricks.yml bundles and CI/CD | databricks-automation-bundles | generic Terraform module selection |
| Unity Gateway model routing and MCP policy | databricks-ai-governance | Bedrock Converse / Cortex Agents |
| Vuetify data table, React UI, generic dbt metrics | existing owners | any Databricks specialist |

## Safety and readiness

Never execute production VACUUM, Delta protocol upgrade, cloud IAM/UC grant, CDC checkpoint reset, historical backfill, bundle deploy/destroy/state migrate, public data share, model serving creation or paid Gateway LLM call without explicit approval. Test all negative tenant/role cases with actual authorized accounts before certifying security. Code examples in this PR are proposed or simulated; behavioral scenarios in evals/databricks-routing.yaml are **unexecuted**. Future Databricks implementation evidence should report DBR/CLI/MLflow version, cloud, workspace/region/identity, observed outputs, DBUs, effective privileges, rollback and failure cases rather than infer compatibility.

Next platforms BigQuery/Fabric/Redshift remain separately governed proposals, not automatic new skills.
