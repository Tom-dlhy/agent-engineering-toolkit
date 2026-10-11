---
name: python-llm-gateways
domain: ai
version: "2.1.0"
description: >-
  Use when selecting and operating Python LiteLLM SDK/Proxy, LangChain
  model abstraction and multi-provider routing, budgets or fallback.
  Do not use when a direct native SDK is simpler or when the task is
  implementing durable agent state, RAG indexing or MCP wire protocol.
---

# Python multi-provider LLM gateways — no free abstraction

## Choose based on actual responsibility
- Native SDK + minimal owned adapter for one provider/security region,
  provider-only tools and exact capability support.
- LiteLLM Python SDK Router for multi-deployment routing in one process;
  review feature translation and SDK error taxonomy.
- LiteLLM Proxy if several apps need centralized key access, spend
  governance, routing and audit. It is an **additional service** with
  database, Redis/cache options, uptime and identity obligations.
- LangChain only when its compositional model/tool/retrieval abstractions
  reduce complexity, not as a mandatory wrapper around every native call.
- LangGraph orchestrator belongs to agent-orchestration when needing
  checkpointed flows and human review; avoid burying reliability in a
  generic gateway adapter.

## Reliability and privacy
Pin SDK/proxy versions; validate model feature matrix and regional
allowlist. Fallbacks can alter structured outputs, model quality,
reasoning content, safety, token billing and data residency. Do not
silently fallback to an unauthorized cloud or model.
LiteLLM budget enforcement for Proxy depends on database-enabled
operation; a DB-less configuration can fail open for spend caps.
Retries must remain bounded across app, router, proxy and provider.

## Deep references
- [LiteLLM SDK, Proxy and deployment router](references/litellm-routing.md)
  — **read when** configuring virtual keys, budgets or router fallbacks.
- [LangChain model abstraction and LangGraph boundaries](references/langchain-and-langgraph.md)
  — **read when** choosing framework composition, typed models and checkpoint integration.
- [Abstraction tradeoffs and scaling](references/provider-selection-and-scale.md)
  — **read when** comparing providers, reliability and capacity.
- [Gateway failure isolation and cost guardrails](references/gateway-failure-and-budget-tests.md)
  — **read when** testing budget fail-open, authentication, fallback regions and layered retries.

## Boundaries
llm-integration owns app contract; agent-orchestration owns workflow
durability; agent-tool-safety owns authorization/injection; cloud
specialists own IAM/quota/native provider APIs.

## Done
Smallest justified stack, proven feature coverage, isolated budgets,
observed routing/failure modes, and explicitly untested live quotas.
