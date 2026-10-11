---
name: python-llm-gateways
domain: ai
version: "2.0.0"
description: >-
  Use when implementing Python multi-provider LLM routing with LiteLLM SDK/Proxy, LangChain model/tool orchestration or LangGraph persistence, including retries, budgets and shared gateways. Do not activate for a single provider's native SDK feature when abstraction brings no value.
---

# Python LLM abstraction and routing — choose the smallest useful tool

## Decision tree
- **One provider, strict regional/security/feature controls?** Prefer native SDK + application-owned thin adapter.
- **Multiple providers/deployments from one Python app?** Evaluate LiteLLM SDK Router with explicit per-model capability and error policy.
- **Multiple teams/services and central spend/keys/logging?** Evaluate LiteLLM Proxy/gateway (new service, DB/Redis/ops dependencies), not just SDK.
- **Complex chains, tools or RAG composition?** Evaluate LangChain; test actual integration package and model capabilities.
- **Durable stateful agent/human approval and recovery?** Evaluate LangGraph persistence and checkpoint semantics, not in-memory tool loop.
Avoid stacking LangChain → LiteLLM Proxy → generic adapter by default; each layer adds latency and error mapping complexity.

## Targeted references
- [LiteLLM SDK, Proxy, deployment router](references/litellm-routing.md) — read when adding cross-provider routing, quota, fallback or governance.
- [LangChain structured outputs and LangGraph durability](references/langchain-and-langgraph.md) — read when composing tools, agents, retrieval chains or checkpointed workflows.
- [Abstraction tradeoffs and system scaling](references/provider-selection-and-scale.md) — read when deciding native vs framework, tenancy, quotas and reliability under load.

## Related
llm-integration owns common output contracts/quality; aws-bedrock, gcp-vertex-ai, azure-ai-foundry own provider-native behavior; agent-tool-safety owns tool authority and injection mitigation.

## Done
Chosen framework justified, per-provider exceptions and response capabilities verified, explicit fallback/residency policy, budgets and evaluation benchmark, no hidden recursive retry storm.
