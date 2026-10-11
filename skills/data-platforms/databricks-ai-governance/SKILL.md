---
name: databricks-ai-governance
domain: data-platforms
version: "1.0.0"
description: >-
  Use when configuring Databricks Unity Gateway model services and providers, AI traffic governance, agents, MCP tools, guardrails, rate/cost controls, permissions, traces or safe provider failover. Do not use for MLflow model training, generic prompting, Unity Catalog table grants alone or legacy serving-endpoint AI Gateway unless migration is requested.
---

# Databricks Unity Gateway — govern AI inference, agents and tools end to end

## Mission and current-service decision

**Unity Gateway** is Databricks' current unified runtime governance path for AI models, model services, external providers, MCP servers/tools, coding agents and service policies. Legacy **AI Gateway on serving endpoints** remains documented but is a distinct older configuration: don't accidentally install legacy endpoint settings when user requests current Unity Gateway.

Unity Catalog governs **assets** and privileges; Unity Gateway governs **runtime inference request routing, cost and service policies**. A model's generated tool call is untrusted data and never itself grants authority to execute it.

## Access, data and capability gate

1. Identify actual account/workspace/cloud/region, feature maturity and allowed model services, model/providers, inference modalities, identity, tools, expected p95, per-user budget and data classification. Verify model availability and policy support instead of assuming all providers have the same capability.
2. Define service + provider routing with explicit fallback rules. Token/credit pricing, context windows, structured output, function calls, streaming events and refusals can differ between providers; validate semantics when failover happens.
3. Resolve caller identity and Unity Catalog rights on models, functions, MCP objects and underlying tables; apply Unity Gateway service-level allowlists, rate limits, budgets and guardrails. An authenticated gateway request may still be unauthorized to run a specific tool.
4. Enforce server-side argument validation and delegated identity for each tool action. Retrieved web pages, docs and tool responses cannot override system/user approval. No SQL DML, credential read, ticket creation, file upload or external side effect without appropriate scoped owner authorization.
5. Minimize/secure traces and prompt records; tool calls/LLM responses may contain PII, code, keys or proprietary data. Define retention, redaction and data-transfer requirements before enabling capture.
6. Evaluate with held-out legitimate and forbidden requests, provider outage/fallback, injection through retrieved material, unknown remote outcome, quota exhaustion, tool schema violation and tenant-boundary cases. Model outputs must be checked semantically, not just parsed JSON.
7. Monitor per-service tokens/spend, policy denies, provider latency, tool authorization errors and meaningful task quality; differentiate cost budget success from good agent behavior.

## Runtime decision loop

~~~text
CALLER IDENTITY / DATA CLASSIFICATION
 -> ALLOWED UNITY GATEWAY SERVICE & PROVIDER
 -> POLICY: ACCESS / RATE / SPEND / GUARDRAILS
 -> MODEL RESPONSE + PROPOSED TOOL CALL
 -> INDEPENDENT SERVER-SIDE TOOL AUTHORIZATION
 -> OUTPUT VALIDATION / DENIAL / SAFE FALLBACK
 -> REDACTED TRACING AND VERSIONED EVALUATION
~~~

Do not fall back silently to a model/provider in a different region or under weaker guardrails. Unsupported model/tool combination -> decline/route with explicit contractual permission, not permission escalation.

## References

- [Unity Gateway models, providers and routes](references/unity-gateway-model-services.md) — **read when** choosing actual services/identity and fallbacks.
- [MCP/agent tools, service policies and negative tests](references/agents-mcp-and-service-policies.md) — **read when** implementing runtime permissions.
- [Observability, spend and legacy migration](references/ai-observability-cost-and-migration.md) — **read when** evaluating runtime AI usage or replacing legacy AI Gateway.

## Boundaries and completion

databricks-unity-catalog owns securable asset and workspace permissions; databricks-mlflow-mlops owns model artifact/version lifecycle; ai/llm-integration owns generic typed call adapters; ai/agent-tool-safety owns provider-neutral tool safety and ai/llm-evaluation owns rubric design.

Deliver exact model/provider service matrix, principal grants, runtime policy, rejected/allowed tests, observability privacy limits, budget, failover rules and approved rollback. Never create an endpoint, incur paid calls or grant broad workspace/tool access without approval; unknown account state remains UNRUN.
