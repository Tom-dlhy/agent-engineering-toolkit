---
name: gcp-vertex-ai
domain: cloud
version: "2.0.0"
description: >-
  Use when calling Gemini/Google models through GCP Vertex AI and the Google Gen AI Python SDK, including ADC, projects, regions, tool use, structured outputs, quotas and model safety. Do not use for Google Cloud Run-only deployment or generic non-GCP prompts.
---

# Vertex AI Python — Gen AI SDK and GCP boundaries

## Preconditions
Check project, region, model ID, API enablement, IAM principal and the requested transport/API version. For Gemini inference use current google-genai SDK rather than deprecated vertexai.generative_models. Availability and feature support are regional/model dependent.

## Procedure
1. Resolve application default credentials in runtime (Workload Identity/GCE/Cloud Run/ADC), not hard-coded service account JSON.
2. Construct Gen AI client with vertexai=True, project/location and appropriate stable API version when supported; choose sync vs async according to hosting runtime.
3. Identify response type (text, parts, tool use, structured schema, multimodal) and handle finish/safety metadata; never assume response.text is always complete.
4. Restrict automatic function calling when tool side effects require authorization; validate arguments against application-owned contracts.
5. Set retry/timeout/quotas carefully and close client at lifespan end. Instrument latency, tokens if available, errors and region without sensitive content.
6. Unit test fake SDK responses and staged GCP integration. Verify model/region/permissions at deployment.

## Deep references
- [Gen AI SDK Python native integration](references/google-genai-sdk.md) — read when implementing Vertex Gemini requests, async calls, credential lifecycle, responses and structured output.
- [GCP IAM, safety, quota and operation](references/gcp-production-operations.md) — read when deploying, handling model support, tool actions, rate limits and data governance.

## Related
llm-integration owns app port; python-llm-gateways owns LangChain/LiteLLM; gcp-integration owns other GCP services.

## Done
Project/region/principal verified, model feature compatibility confirmed, tool authorization tested, closed resources and staging test evidence.
