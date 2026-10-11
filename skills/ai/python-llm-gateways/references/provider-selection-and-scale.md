# Choosing LLM SDK/framework and scaling by actual load

**Read when:** deciding between native Bedrock/Vertex/Azure SDK, LiteLLM, LangChain, or a gateway at different deployment sizes.

## Decision record

| Axis | Native SDK | LiteLLM SDK | LiteLLM Proxy | LangChain / LangGraph |
|---|---|---|---|---|
| One-cloud feature fidelity | Highest | Check mapping | Check mapping and proxy support | Check integration version |
| Multi-provider calls | Write adapters | Unified Python APIs | Shared network API | Composable provider integrations |
| Central virtual keys/spend | External infra | App-owned | Built-in gateway mechanisms (configure DB) | External infra |
| Multi-agent orchestration | Custom app | Not core purpose | Not core purpose | LangChain + LangGraph |
| Ops burden | Small | Package/runtime | Separate HA service/DB/monitoring | Framework/state storage, evaluations |
| Failure provenance | Direct native errors | Normalized mapping | Double network boundary and gateway faults | Multiple wrappers may obscure cause |

## Workload-specific plan

POC: one provider, single call, JSON validation and controlled token cap. MVP: async client lifetime, timeouts, error taxonomy and visible result status, evaluation set. Production: quotas by tenant, dedicated observability, cache when semantically safe, idempotency, model feature pinning, cost alarms, incident runbook. High throughput: admission controls by tokens (not only request count), queue durable asynchronous extraction, response streaming where useful, batched inference only when provider supports it, fallback-region governance.

There is **no universal number of users** that mandates LangChain, LiteLLM or multiple workers. Twenty users submitting huge 30k-token documents can exhaust a TPM budget faster than thousands of users sending small cached queries. Model throughput, output tokens, latency and concurrent requests.

## Reliability budgets
Total app deadline must include queue time, routing gateway, model inference, retries and output validation. Two SDKs each retrying three times can cause six or more actual calls; choose one clear retry owner and instrument attempts. Cache must key tenant, prompt/model config and source version, and must not cross privacy boundaries.

## Approval and quality
A model fallback is a behavioral release with measurable task quality and residency implications; require explicit approval for sensitive tenant data and important business decisions. Test denial and unavailable-model path.

Docs: https://docs.litellm.ai/docs/python_sdk and https://docs.litellm.ai/docs/proxy/architecture and https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model .
