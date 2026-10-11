---
name: snowflake-cortex-ai
domain: data-platforms
version: "1.0.0"
description: >-
  Use when implementing Snowflake Cortex Agents, Cortex Analyst text-to-SQL, Cortex Search retrieval, semantic views or Cortex AI observability and access controls. Do not use for generic LLM provider chat APIs, conventional ML Model Registry work or unsupervised SQL execution outside authorized roles.
---

# Snowflake Cortex AI — grounded structured and unstructured enterprise answers

## Mission

Build safe, verifiable Snowflake-hosted GenAI retrieval and analytics using **Cortex Agents, semantic views, Cortex Analyst and Cortex Search**. Protect semantic metric correctness, role-based permissions, sensitive traces, generated SQL and predictable cost. Know the difference between model generation, query tool execution and user authorization: a fluent response is not proof that the generated query or retrieved evidence is correct.

## Selection gates

1. Establish user question classes: structured analytical metrics, unstructured enterprise content, hybrid questions, workflow tool actions or plain text generation. Confirm account/region, feature availability, role grants, budget and data classification.
2. For structured natural-language-to-SQL, define stable **semantic views**, verified query examples and metric/grain contracts. Legacy Cortex Analyst REST remains available, but as of 2026-08-28 Snowflake recommends transitioning to Cortex Agents for new integrations; migrate only if compatible and approved.
3. For search over unstructured documents, design Cortex Search source, service owner, indexing lag and document ACL/row filter semantics; retrieval is not universal access enforcement. Confirm what the selected retrieval service **actually** enforces in the deployed configuration.
4. Cortex Agents can compose structured and unstructured tools. Tool outputs remain untrusted; explicitly gate any SQL execution and external side effects under least privilege. Avoid giving the agent a broad role merely to "make it work".
5. Define task success: SQL semantic correctness and authorized row exposure; retrieval groundedness/citations, abstention, latency/credits/tokens and trace retention. Do not benchmark only friendly questions.

## Contracted execution loop

~~~text
USER IDENTITY / ROLE AND TASK
 -> SELECT SEMANTIC VIEW / SEARCH SCOPE
 -> AGENT + ALLOWED TOOLS + DATA ACCESS
 -> GENERATED SQL / RETRIEVED EXCERPTS
 -> SERVER-SIDE PERMISSION AND QUERY SAFETY
 -> GROUNDING / METRIC VALIDATION
 -> ANSWER WITH UNCERTAINTY / TRACE METADATA
 -> HOLD-OUT EVALUATION / COST & DRIFT MONITORING
~~~

Beware response-block evolution: the 2026-04-13 Cortex Agents update can emit system_execute_sql blocks rather than older cortex_analyst_text_to_sql blocks. Never parse one hard-coded response envelope and silently drop other tool calls, errors or provenance.

## Select one deep reference

- [Agents, Analyst and semantic view SQL contracts](references/agents-analyst-semantic-views.md) — **read when** implementing Cortex APIs, semantic modeling or SQL execution traces.
- [Cortex Search grounding, permissions and threat model](references/search-grounding-and-permissions.md) — **read when** retrieving enterprise data or protecting sensitive content.
- [Evaluation, telemetry and Cortex credit governance](references/evaluation-observability-cost.md) — **read when** measuring answer quality, analyzing traces, quotas and release gates.

## Ownership

data/analytics-modeling defines business metric grain, ai/rag-engineering designs general RAG, ai/llm-evaluation grades generalized model behavior, cloud/aws-bedrock covers **Bedrock Converse** and ai/agent-tool-safety owns general untrusted tool protocol. This skill owns **Snowflake-specific Cortex tools, views, data-access semantics, API versioning and observability**. No broad admin grants, live AI agent deployment or external action without permission.

## Completion gate

Deliver versioned agent/search/semantic configuration, role and tool privilege map, gold SQL and retrieval question set, normal and negative tests, token/credit boundaries, observability privacy, rollback route and exact unverified capabilities. An answer that seems correct without a held-out check is not release evidence.
