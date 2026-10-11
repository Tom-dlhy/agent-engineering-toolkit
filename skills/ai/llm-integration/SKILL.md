---
name: llm-integration
domain: ai
version: "2.1.0"
description: >-
  Use when defining production model-backed app contracts, typed outputs,
  streaming, rate/cost policies, provider-native API capabilities and
  safe error mapping. Do not implement agent durability, RAG indexing
  or protocol-level MCP servers with this general integration skill.
---

# LLM integration — application-owned contract, provider-specific reality

## Model boundary method
1. Specify input/output modalities, structured schema, safety/abstention,
   data residency, latency, quota, allowed tool actions and acceptance evals.
2. Prefer native SDK plus a thin owned adapter for one provider or
   deep provider features; use python-llm-gateways only when its
   multi-provider routing or central governance is justified.
3. Pin exact SDK/model/api versions and test feature matrix: structured
   output, streaming, function calls, reasoning blocks, context caching
   and usage metrics vary across model and deployment.
4. Validate output at runtime; strict JSON schema or function arguments
   are **not** guaranteed semantic truth or permission to execute a tool.
   Handle refusal, incomplete output, content filter and token truncation.
5. Preserve provider-specific completion reason/tool identifiers and
   multiline/multimodal parts; never join arbitrary stream deltas
   and declare a structured document valid before terminal event.
6. Assign total deadline, retries and token/cost capacity at tenant and
   provider, including cancellation, 429 and unknown remote outcome.
7. Establish versioned negative/behavioral evals, privacy-safe telemetry,
   controlled release and stop/rollback thresholds.

## Targeted references
- [Typed LLM ports and structured output](references/typed-boundary-and-outputs.md)
  — **read when** building Pydantic/application-owned schema or adapters.
- [Reliability, token budgets, fallbacks and security](references/reliability-and-risk.md)
  — **read when** handling quotas, provider errors and side effects.
- [Production LLM verification and rollout](references/testing-evals-and-rollout.md)
  — **read when** changing provider/model/prompt in production.
- [Provider capability matrix and streaming envelopes](references/provider-capabilities-and-streaming.md)
  — **read when** mapping AWS/GCP/Azure/native response shapes,
  refusals, tool results and partial streams.

## Distinct specialist routes
aws-bedrock for Bedrock Converse, gcp-vertex-ai for Gemini on Vertex,
azure-ai-foundry for Azure; python-llm-gateways for LiteLLM/LangChain;
agent-orchestration for durable runs; rag-engineering for indexing and
retrieval, mcp-integration for protocol mechanics.

## Done
Supported deployment capability, typed response, explicit error taxonomy,
resource/budget and privacy controls, reproducible negative tests and
documented unverified provider/cloud features.
