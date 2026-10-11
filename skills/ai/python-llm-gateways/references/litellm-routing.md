# LiteLLM Python SDK, Router and Proxy — production tradeoffs

**Read when:** building one Python client that can call several providers/deployments, or deploying a centralized LLM gateway.

## Three operating modes

| Mode | Fit | Dependencies/risks |
|---|---|---|
| Native SDK | One provider / deep features | Provider adapter maintenance |
| LiteLLM Python SDK | One Python service needs unified requests | Package size, normalized error/capability gaps |
| LiteLLM Proxy | Several services/teams need virtual keys, budgets, logging | Separate operational deployment, database, optional Redis, auth, uptime and privacy |

LiteLLM supports asynchronous acompletion and a Router with retry/fallback/load balancing. Do not assume every model supports every OpenAI-like parameter; check supported endpoints/features and translate response content faithfully.

~~~python
from litellm import acompletion

async def generate_with_litellm(model: str, prompt: str) -> str:
    response = await acompletion(
        model=model,  # e.g. configured "bedrock/...", "vertex_ai/...", "azure/..."
        messages=[{"role": "user", "content": prompt}],
        timeout=20,
        max_retries=1,
    )
    content = response.choices[0].message.content
    if not isinstance(content, str) or not content:
        raise ValueError("No usable text response; inspect tool/finish reasons")
    return content
~~~

This is a minimal text-only example; model IDs and credentials must be configured per the target provider and verified against installed LiteLLM version. Do not hardcode provider keys or log prompts. Model stop reasons and tool content may require different handling.

## Routing
Configure allowed model groups, deployment weights, retryable failure classes, cross-model fallback policy, region/tenant allowlists, token budgets, concurrency and request tracing. A fallback can change price, data residency, tool behavior or answer quality. Test exactly which errors trigger fallback and that cost controls still apply under database/network failure.

## Critical budget caveat
LiteLLM Proxy budget enforcement depends on its backing database. Official documentation explicitly warns DB-less proxy configurations can fail open for budget caps; where hard ceilings are required, assess fail-closed budget configuration and its availability/latency tradeoffs. Avoid promising budget enforcement from a YAML setting alone.

## Verification
SDK adapter tests vs real provider, retry/fallback sequence and latency, model alias mapping, unauthorized tenant/virtual key, circuit breaker behavior, DB/Redis failure, cost and trace redaction, egress region.

Official: https://docs.litellm.ai/docs/python_sdk and https://docs.litellm.ai/docs/proxy/users and https://docs.litellm.ai/docs/proxy/architecture .
