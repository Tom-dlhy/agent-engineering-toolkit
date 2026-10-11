# Google Gen AI SDK on Vertex AI (Python)

**Read when:** writing direct Google Gemini inference code from a GCP workload or async Python service.

## Current SDK and migration
Current Google guidance uses google-genai for model generation via Vertex; legacy vertexai.generative_models was deprecated and removed according to published migration timeline in 2026. Check google-genai version and avoid mixing Developer API key mode with Vertex enterprise/project authentication without need.

~~~python
from google import genai
from google.genai import types

async def generate_on_vertex(
    project: str, location: str, model_id: str, text: str
) -> str:
    client = genai.Client(
        vertexai=True,
        project=project,
        location=location,
        http_options=types.HttpOptions(api_version="v1"),
    )
    try:
        response = await client.aio.models.generate_content(
            model=model_id,
            contents=text,
            config=types.GenerateContentConfig(max_output_tokens=512),
        )
        if not isinstance(response.text, str) or not response.text:
            raise ValueError("No complete text response; inspect safety/finish")
        return response.text
    finally:
        await client.aio.aclose()
        client.close()
~~~

This demonstrates correct async method and explicit client cleanup, not efficient app lifecycle (create client once at startup for real API throughput). Check model capabilities, supported v1 surface and SDK runtime before selecting a concrete model ID. The SDK may provide a context-managed async client; use that consistently when available.

## Output and structured schemas
For structured output, inspect Google response MIME type/response schema support of selected model. Validate final result against Pydantic; a block/refusal/truncated response may have no text. Tool/function calling may invoke Python functions automatically in some SDK patterns: disable automatic execution when tools have side effects or require user authorization, and process tool requests through an application allowlist.

## Authentication and data access
ADC via runtime workload identity; assign minimum model invocation permissions and project scope. Avoid GOOGLE_APPLICATION_CREDENTIALS pointing to a committed JSON key. Respect location, service perimeter and project routing; "global" endpoint is not automatically consistent with a strict region residency requirement.

## Async and errors
Explicitly close sync and async resources as prescribed by installed SDK; don't open client per request. Set request/transport timeout, bounded retry and per-task semaphore where needed. Classify auth, quota, service, validation and safety separately.

Official: https://googleapis.github.io/python-genai/ and https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart .
