---
name: azure-ai-foundry
domain: cloud
version: "2.0.0"
description: >-
  Use when integrating Python applications with Azure OpenAI or Microsoft Foundry models, v1 Responses/chat APIs, deployment names, Entra managed identity, quotas or model/tool differences. Do not use for unrelated Azure Functions or storage.
---

# Azure AI Foundry — native Python and managed deployments

## Choose endpoint and identity
1. Identify whether resource is Azure OpenAI v1 endpoint or another Foundry model service, deployment name, region, enabled APIs and feature compatibility. Do not assume all Foundry model endpoints use identical protocol.
2. Prefer Entra-managed workload identity where available; otherwise injected SecretStr API keys and rotation plan. Verify token audience from the current Microsoft API docs.
3. For Azure OpenAI v1, current documentation supports OpenAI Python client with base_url ending in /openai/v1/ and deployment name as model; older AzureOpenAI api_version patterns are not universally interchangeable.
4. Handle Responses output items/tools, final status/refusal and usage, not only flattened text. Enforce structured response and permissions via app-owned schema/port.
5. Bound request latency, 429 quotas and retries, avoid cross-region fallback without approval; test staging with actual deployment.
6. Redact prompts/secrets, trace allowed error IDs and evaluate version/model migration.

## Targeted references
- [Azure OpenAI v1 Python client and authentication](references/azure-v1-python.md) — read when implementing Responses with API key or Entra token provider.
- [Foundry deployment, quota, governance and tests](references/azure-operations.md) — read when deploying, quotas, fallback, model compatibility or security.

## Related
llm-integration owns normalized contract; python-llm-gateways owns LiteLLM/agent abstractions; azure-integration owns other Azure platform services.

## Done
Endpoint/region/deployment and principal verified, exact API mode supported, no unsafe credential persistence, retries and telemetry bounded, tools authorized and release tests reported.
