# Cortex Agents, Analyst and semantic views — governed text-to-SQL

Read when: building Snowflake Cortex Agents for structured data questions, migrating Analyst REST callers or repairing semantic SQL generation.

## API and semantic ownership

Snowflake recommends transitioning new integration focus from standalone Cortex Analyst toward Cortex Agents (2026-08-28 notice); the Analyst REST API continues to function. Cortex Agents may use semantic views for SQL tools and combine Search and other tools. A semantic view contains business entities, measures, joins, verified query examples and other semantics; it must reflect the real metric contract, not merely expose every table.

The change from standalone Analyst is an **API/orchestration change**, not necessarily a semantic-layer rewrite. Don't force migration of an existing functioning app without checking actual version, tool contract, region support, privileges and response envelope.

## End-to-end workflow

1. Inventory question set and distinguish simple text-to-SQL, multi-table metrics, conversational follow-up, document retrieval and external actions.
2. Create/test semantic views at the correct **fact grain** with business ownership. Define metric denominators, date logic, currency, filter aliases and authorized dimensions. SQL syntactic validity is not metric correctness.
3. Build verified SQL examples for ambiguous questions: “current month revenue”, “unique customers” or a weighted churn percentage. Include impossible/unauthorized questions and intended abstention.
4. Configure agent tools minimally: which semantic view, which permitted warehouse and bounded SQL timeout; use caller identity and role with **tested** grants, not an all-data administrative role.
5. Parse full Agent Run API response: streaming versus non-streaming differs, there may be multiple content/tool blocks and failures. Do not concatenate arbitrary chunks into a guaranteed-valid SQL string.
6. Apply server-side allowlist/authorization on any SQL or tool that can execute externally. Never treat generated SQL from a model as permission to access confidential objects or perform DDL/DML.
7. Compare generated query results to known gold SQL and check role/tenant isolation and correct uncertainty.

## Response evolution trap

Snowflake's 2026-04-13 release changed some Cortex Agent analytic execution tool result blocks: system_execute_sql replaces older cortex_analyst_text_to_sql in relevant agent traces/outputs. Relying only on an old tool tag can silently lose SQL/result attribution. Verify currently deployed response version and include parser tests for missing/multiple/partial tool blocks and terminal/error envelopes.

## Gold question fixture

~~~text
Question: "Which acquisition channel brought most distinct new customers last quarter?"
Ground truth: versioned SQL at customer acquisition grain, not order grain
Expected query: correct timezone/calendar, DISTINCT entity and channel attribution
Negative: a sales aggregate cannot be substituted for acquisition count
Security: restricted segment cannot be queried by an unrelated role
Abstention: unknown attribution data -> say unavailable rather than invent channel
~~~

Semantic views and generated SQL must be reviewed for ambiguous business terms. Route general business metrics to analytics-modeling, and generic LLM validation patterns to llm-evaluation/agent-tool-safety. This leaf owns Snowflake-specific Agent/Analyst tool and semantic integration.

Sources: https://docs.snowflake.com/en/release-notes/2026/other/2026-08-28-cortex-analyst-transition-cortex-agents and https://docs.snowflake.com/en/release-notes/2026/other/2026-04-13-cortex-agents-agentic-analyst and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-run and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api
