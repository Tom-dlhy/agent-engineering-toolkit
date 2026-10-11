# Vertex AI inference operations, identity, quota, grounding and safety

**Read when:** deploying or investigating Gemini model calls under project IAM, regions, data policies and rate limits.

## Production identity
Use GCP ADC and workload identity federation for CI/GKE/Cloud Run, minimum service agent/runtime roles for Vertex invocation, logging rights and explicit project/region. Check actual serving model and entitlement. Do not suggest service account JSON keys as the default. Service account privileges and API enabled status are separate controls.

## Quota and capacity
Reason about requests/sec plus input/output tokens and model-specific quota/throughput mode. Bursty document extraction can be limited by TPM, context length or output token cap before VM CPU. Bound concurrent calls, respect resource-exhausted responses, select admission/queue policy and cap overall deadline. Evaluate fallback to another region against data residency and quality requirements; no silent cross-region migration.

## Structured tool and safety boundaries
Treat content parts and function arguments as untrusted. For a tool that sends email, changes a ticket, creates a cloud resource or accesses personal data, require explicit tool allowlist, tenant authorization and idempotent business confirmation independent of model response. Safety blocks/refusals and missing candidates need a controlled application outcome, not a blind retry with weaker settings.

## Observability
Record logical deployment alias, region/project (safe IDs), request/trace identifiers, model finish classification, latency, token input/output when returned, rate limiting and cost estimate with pricing provenance. Do not export raw customer prompts, images or tools to third-party telemetry by default.

## Test matrix
Invalid project/region, missing IAM, API disabled, quota exhausted, malformed structured schema, safety block, cancellation, tool request with unauthorized action, model unavailable, prompt too large, SDK migration compatibility and spend bursts.

Official: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart and https://googleapis.github.io/python-genai/ .
