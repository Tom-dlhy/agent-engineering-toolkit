# Azure Foundry deployment and operations

**Read when:** running Azure-hosted LLM inference in production with access control, deployments, quotas and region governance.

## Runtime contract
Record tenant/subscription/resource/region, endpoint family, API version, Azure deployment name, permitted model features, network access restrictions, and whether public/private endpoint and managed identity apply. Treat Azure OpenAI v1 protocol and other Foundry catalog models as separate integrations when their capabilities differ.

## Identity and secret handling
Use DefaultAzureCredential in managed infrastructure with minimum supported data-plane RBAC, correct token audience and refresh; a local developer should authenticate with approved dev credential path, not committed key. Rotate keys if used. Keep endpoint and deployment pinned in settings; validate at startup only with safe bounded call if appropriate.

## Rate, spend and fallback
Quota and provisioning vary by model/region/deployment. Define per-tenant admission and total inference deadline, requests/tokens per minute and dynamic cost thresholds. Endpoint fallback may change model quality, data residency or allowed governance: require policy-based approval, not automatic failover across arbitrary regions.

## Tool outputs and PII
Azure-hosted model output is still untrusted; tool arguments must be schema validated and authorized at application boundary, especially for tickets, files and cloud operations. Guardrails/content filtering are additional safety controls, not proof of tool safety. Record usage, region and latency, no raw user data in general logs or tracing callbacks.

## Compatibility tests
Real deployment ID vs catalog model ID, incorrect base_url, expired Entra identity, 429/503, content filter/refusal, unsupported Responses operations, structured output schema invalid, tool_use, streamed partial result and per-tenant isolation.

## Rollout
Version application prompt/model/deployment together and benchmark quality/cost. Establish canary/rollback on error rate, latency and evaluated task quality. For strict sovereignty, check regional processing/document retention under current Azure contracts rather than assuming region based on endpoint hostname.

Official: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle and https://ai.azure.com/api-reference/responses/ .
