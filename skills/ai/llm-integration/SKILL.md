---
name: llm-integration
domain: ai
version: "2.0.0"
description: >-
  Use when designing model-backed application boundaries, structured output, tool safety, retrieval, LLM failure classification, evaluations and multi-provider contracts. For native Bedrock, Vertex AI or Azure operations activate the service-specific cloud skill; for LangChain/LiteLLM activate python-llm-gateways.
---

# LLM integration — application contract independent of SDK

## Start with capability, not brand
1. Define input modality, output schema, max latency, reliability, compliance/residency, budget, rate limits, eval data and tool side effects.
2. Evaluate **native SDK** if using one provider or provider-only capability. Use a minimal application-owned Protocol/adapter to avoid bleeding SDK responses into domain.
3. Evaluate LiteLLM for many provider deployments needing routing/budgets/gateway; LangChain for tool/prompt/retrieval component composition; LangGraph for durable orchestrated agent state. Don't install all three by default.
4. Validate untrusted model text and tool arguments with Pydantic/schema; tool calls must pass authorization, allowlists, idempotency and human approval gates.
5. Define classification and deadlines for 429/quota, auth errors, invalid outputs, safety blocks, tool cycles and cancellation; default to **no silent fallback** across models without quality/compliance approval.
6. Establish evaluation and telemetry of output quality, schema violations, p95/99 latency, retries, token/cost per task and provider differences.

## Targeted references
- [Typed LLM ports and structured output](references/typed-boundary-and-outputs.md) — read when creating domain/provider-independent LLM adapter or validation contracts.
- [Reliability, token budgets, fallbacks and security](references/reliability-and-risk.md) — read when implementing retries, quotas, gateway, model routing, streaming and tool side effects.
- [Production LLM verification and rollout](references/testing-evals-and-rollout.md) — read when testing model changes, building evals, staging and canary.

## Native specialists
aws-bedrock for Bedrock Converse and tool use, gcp-vertex-ai for Google Gen AI/Vertex, azure-ai-foundry for Azure Foundry and managed identity; python-llm-gateways for LangChain/LiteLLM/agent orchestration.

## Done
Contract tested and versioned, model/mode capabilities explicitly confirmed, privacy and fallback policy agreed, budget/latency measured where available, real evaluation evidence distinguished from mock tests.
