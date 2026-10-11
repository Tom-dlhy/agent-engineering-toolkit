# Snowflake specialists — governance v2 decision and official-source audit

**Date:** 2026-10-12. **Base:** main after PR #28. **User request:** start the provider-specific Data & AI cloud platform series with Snowflake. Charte v2 maintained **outside** the repository. **Decision:** five independently useful Snowflake skills CREATE, existing cross-platform Data/AI/Cloud specialists REUSE/REFERENCE, no import, no changes to installation profiles.

## Scope: why five independent skills, not one monolith

| Proposed | Independent task trigger and delivered expertise | Adjacent owner kept intact | Governing verdict |
|---|---|---|---|
| snowflake-query-performance | A specific Snowflake SQL execution/warehouse/credit investigation | data/lakehouse-engineering cross-engine storage/format; cloud/finops-engineering provider portfolio spend | CREATE |
| snowflake-data-pipelines | Snowflake COPY/Snowpipe/Dynamic Tables/Streams/Tasks, retry/replay | data/data-pipeline-quality generic data contracts, data/streaming-cdc-engineering source WAL | CREATE |
| snowflake-snowpark-ml | Snowpark Python, temporal feature joins, Snowflake ML Model Registry, LightGBM and inference | ai/llm-evaluation generic model/prompt eval, data/analytics-modeling metric grain | CREATE |
| snowflake-cortex-ai | Cortex Agents/Analyst/Search/semantic views, tracing, query grounding and RBAC | ai/rag-engineering retrieval design, ai/agent-tool-safety generic tools, cloud/aws-bedrock native Bedrock APIs | CREATE |
| snowflake-security-governance | Snowflake RBAC, database/account roles, masking/row policies, shares and SQL audit | cloud IAM principal management, personas/privacy-compliance-lead legal purpose and processing review | CREATE |

**Rejected micro-skills:** snowflake-dynamic-tables alone (REFERENCE pipelines), snowflake-query-history alone (REFERENCE performance), snowflake-lightgbm alone (REFERENCE snowpark-ml), cortex-analyst-only (REFERENCE cortex-ai, avoid promoting a transition API as default), masking-policies-only (REFERENCE security). Reevaluate only when proven task demand and genuine independent expertise justify a split.

## Repository changes proposed

- New domain: data-platforms (platform SDK/SQL behavior, **not** a new general Cloud category).
- Five new task-specific SKILL.md cores with exactly three deep, locally indexed references each.
- Proposed post-PR inventory: **171 skills across 14 domains, 397 reference files, 20 unchanged profiles**. Snowflake skills are discoverable but not automatically installed or activated by general profiles.
- Reference leaves are substantial with SQL/Python examples, failure and recovery paths, and official links. No Snowflake connection, paid query, DDL or new third-party script is executed as part of this PR.
- Deterministic validation and negative routing scenarios are necessary but **not live Snowflake proof**.

## Official-source findings and scope qualifications

**SQL/performance**
- Micro-partitions/pruning and clustering are Snowflake physical concepts, not PostgreSQL B-tree indexing. Official: https://docs.snowflake.com/en/user-guide/tables-micro-partitions and https://docs.snowflake.com/en/user-guide/tables-clustering-keys
- Spilling to local/remote and Query History timing should be diagnosed with actual profiles before sizing changes. Official: https://docs.snowflake.com/en/user-guide/performance-query-warehouse-memory and https://docs.snowflake.com/en/sql-reference/account-usage/query_history
- Auto-suspend can reduce idle credits, but repeated resume minimum billing must be considered; account spend is broader than warehouse credits. Official: https://docs.snowflake.com/en/user-guide/warehouses-considerations and https://docs.snowflake.com/en/user-guide/cost-controlling-controls

**Pipelines**
- Dynamic Tables TARGET_LAG is a **best-effort freshness target**, not a cron interval or guaranteed SLO. Source: https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag
- Snowpipe is staged-file micro-batch ingestion. File-order is not guaranteed; load metadata is not an application business-key uniqueness constraint. Official: https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro
- Dynamic Tables support eligible SELECT-based declarative transformations. Streams/Tasks handle procedural MERGE/side effects, and target lag is best-effort freshness rather than fixed interval. Official: https://docs.snowflake.com/en/user-guide/dynamic-tables-limitations and https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag
- Heavy replay can reinitialize dynamic outputs or exceed stream retention; never auto-run CREATE OR REPLACE/DROP/large backfill. Official: https://docs.snowflake.com/en/user-guide/streams-intro

**ML**
- Model Registry is versioned and supports LightGBM, with version-specific inference method signatures and sample_input_data or explicit signatures for LightGBM logging. Official: https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview and https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/lightgbm
- Feature Store feature views and point-in-time training vary by edition and version; new append-only history capabilities have explicit version gates. Official: https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/feature-views and https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering
- Batch vs real-time serving depends on warehouse/container service and workload, not merely model registry existence. Official: https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/inference-overview

**Cortex GenAI**
- Snowflake 2026-08-28 recommends transition from Cortex Analyst to Cortex Agents while existing Analyst REST continues. Semantic views can carry over. Official: https://docs.snowflake.com/en/release-notes/2026/other/2026-08-28-cortex-analyst-transition-cortex-agents
- 2026-04-13 changed some Cortex Agent result blocks to system_execute_sql, requiring response parser updates. Official: https://docs.snowflake.com/en/release-notes/2026/other/2026-04-13-cortex-agents-agentic-analyst
- **Critical:** Cortex Search uses **owner's-rights**; service usage does not automatically create per-caller source-row filtering. Enforce document entitlement explicitly, review service grants and test unauthorized retrieval. Official: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview
- Agent evaluations and AI_OBSERVABILITY_EVENTS have feature/permission/billing and sensitive trace considerations. Official: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-evaluations and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-monitor

**Governance**
- Account roles/database roles and managed access schema grant authority differ. Future grants apply to new objects and can have schema/database precedence. Official: https://docs.snowflake.com/en/user-guide/security-access-control-overview and https://docs.snowflake.com/en/user-guide/security-access-control-configure
- Dynamic data masking and row access policies have Enterprise Edition requirements: verify exact edition/region and effective consuming role. Official: https://docs.snowflake.com/en/user-guide/security-row-intro and https://docs.snowflake.com/en/user-guide/security-column-ddm-intro
- Cross-region sharing is a data-release/legal review, not merely a SQL object change. Official: https://docs.snowflake.com/en/user-guide/secure-data-sharing-across-regions-platforms

## Anticipated routing and evidence failure cases

| Request | Choose | Exclude |
|---|---|---|
| "Profile Snowflake warehouse query spilling and pruning" | snowflake-query-performance | postgres-performance, warehouse vendor decision |
| "Build Snowpipe Dynamic Tables and Streams Tasks with replay" | snowflake-data-pipelines | generic Airflow-only orchestration |
| "Register a Snowpark LightGBM model version and batch inference" | snowflake-snowpark-ml | cortex-ai |
| "Cortex Agent semantic SQL and Search over docs" | snowflake-cortex-ai | Bedrock Converse |
| "Mask Snowflake PII with role-based policies and negative tests" | snowflake-security-governance | cloud AWS IAM policies |
| "Implement general fact dimension grain in dbt" | analytics-modeling | all provider-specific Snowflake skills |
| "Optimize PostgreSQL with EXPLAIN ANALYZE" | postgres-performance | snowflake-query-performance |
| "Configure AWS IAM Lambda trust policy" | aws-iam-security | snowflake-security-governance |
| "Select Snowflake versus Databricks for a lakehouse" | lakehouse-engineering / stack-advisor | any specific Snowflake implementation skill without choice |

**Evaluation requirements:** registry / profile integrity, safe progressive references, non-collision routing, synthetic temporal/replay proof, ordinary CI; follow up with authorized real Snowflake integration (SQL/Python/AI/role tests), cost measurements, feature/version checks, and outcome-based held-out real-agent evaluation. Neither the offline examples nor YAML imply Snowflake account access or production deployment.

Next provider: Databricks, only after its own reuse/extend/create review; no automatic platform skill creation.

**Evidence limitation:** Behavioral scenarios in evals/snowflake-routing.yaml are intentionally **unexecuted**. No Snowflake service connection, data access, warehouse charge, model registration or Cortex inference has been performed by this PR.
