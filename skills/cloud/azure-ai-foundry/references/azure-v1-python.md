# Azure OpenAI/Foundry v1 client — Python

**Read when:** implementing native Azure OpenAI model calls from Python, choosing endpoint/client or wiring Entra authentication.

## Current v1 API
Microsoft documents the OpenAI Python client pointed at the Azure resource v1 base URL. The model parameter is generally **deployment name**, not a globally usable public model ID.

~~~python
from openai import AsyncOpenAI

async def generate_azure(
    azure_endpoint: str, deployment: str, api_key: str, prompt: str
) -> str:
    async with AsyncOpenAI(
        api_key=api_key,
        base_url=azure_endpoint.rstrip("/") + "/openai/v1/",
        timeout=20.0,
        max_retries=1,
    ) as client:
        response = await client.responses.create(
            model=deployment,
            input=prompt,
        )
        if not response.output_text:
            raise ValueError("No usable text; inspect response/output status")
        return response.output_text
~~~

An actual service should construct and close the AsyncOpenAI client at app lifespan, not per request. This example uses injected key to illustrate request API; prefer Entra ID when supported and authorized.

## Entra ID / managed identity
Microsoft v1 docs show standard OpenAI client plus azure.identity DefaultAzureCredential/get_bearer_token_provider with the documented scope. Validate current correct scope for the actual endpoint (Microsoft documents https://ai.azure.com/.default for certain v1 flows); don't blindly carry over prior AzureOpenAI sample scopes or assume all Foundry endpoints share it. Use correct sync/async token provider pattern for installed SDK, with refresh and lifespan.

## Error/response decisions

- 401/403: identity/roles/deployment access; do not retry as generic service unavailable.
- 404: wrong deployment/endpoints or unavailable API; distinguish from business resource 404.
- 429: quota/rate, respect retry policy and any server instructions.
- 5xx/timeouts: bounded retry and possible unknown outcome.
- Responses content: output may include tool calls, refusals, status/finish and non-text parts. Do not assume output_text captures tool actions.
- Some model/endpoint combinations expose only chat completions or different API capabilities. Verify before migrating.

## Test matrix
Invalid deployment, wrong endpoint slash/base path, missing Azure role, expired credential refresh, malformed structured response, unsupported tool, timeout, quota and data residency fallback. Do not log API key or raw prompt.

Official: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle and https://learn.microsoft.com/en-us/rest/api/aifoundry/azureopenai/responses .
