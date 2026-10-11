# LLM reliability, quotas and multi-provider failure boundaries

**Read when:** implementing production retries, routing, fallbacks, quotas, streaming cancellation or tool side effects.

## Failure classification

| Condition | Expected handling |
|---|---|
| 401/403, IAM/managed identity | Configuration/security incident; don't retry endlessly |
| 400 bad request, unsupported model feature | Fix adapter/capability negotiation |
| 429 rate or token quota | Bounded backoff, Retry-After when meaningful, admission controls |
| Provider 5xx/transient timeout | Retry only when safe within total deadline; maybe queue |
| Read timeout after tool execution | Unknown side-effect outcome; reconcile |
| Safety/refusal/content block | Business-appropriate abstention/fallback, not unsafe bypass |
| Malformed/truncated structured output | Validate, bounded repair/abstain, monitor rates |
| Partial stream/client disconnect | Close resources, cancel work when appropriate, no false success |

## Three different budgets
- User request latency budget: total end-to-end deadline including wait, retries and model tokens.
- Provider request rate / token throughput quotas: RPM, TPM, concurrent requests, burst shape.
- Spend/usage: per-request/tenant/organization, prompt cache/embedding/stream charges; prices/model availability must be verified current, not hardcoded in skill.

## Fallback policy

Fallback is a product decision: cross-model outputs may differ in schema, privacy/data residency, latency, safety behavior, tool definitions and billing. Do not silently route sensitive payload from Azure EU deployment to a nonapproved region/provider. For structured output, revalidate after fallback; model equivalence is not guaranteed.

## Tool calling

Map model-requested tool names to explicit allowlist; validate parameters, tenant permissions, side-effect intent and idempotency; limit steps/time/cost; persist state before irreversible effects and require user approval when relevant. Prompt injection may arrive through retrieved docs and tool results; treat it as untrusted data, not an instruction to use a secret or new endpoint.

## Production reliability

Use per-provider token-aware concurrency, queues where bursts exceed rate, semaphores, bounded replay, correlation tracing and metrics. Circuit breakers can reduce cascading failures only when failure classes and half-open policy are sound. Separate synchronous chat response from durable long-running extraction pipelines.

Official: https://docs.litellm.ai/docs/proxy/users and https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html and https://docs.langchain.com/oss/python/langchain/structured-output .
