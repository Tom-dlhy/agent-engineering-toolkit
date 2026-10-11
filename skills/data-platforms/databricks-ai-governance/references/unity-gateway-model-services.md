# Unity Gateway — model services, providers, identity and safe failover

Read when: configuring Databricks Foundation Model API access or external providers, model-service routing and failover constraints.

## Current service boundary
Databricks' **Unity Gateway** (2026) integrates model services, model providers, access, MCP/tools, governed skills and spend controls. It is **not** the same as legacy endpoint-attached AI Gateway. Unity Catalog governs model/provider/tool assets and their privilege ownership; Unity Gateway routes **runtime requests** and enforces service policies. Validate current availability by workspace/region/cloud and actual supported provider/model set.

## Integration contract
1. Caller principal/tenant, data type, region restrictions, expected latency and budget.
2. Named model service and model/provider definition, allowed fallback list and model features (streaming, multimodal, tool calls, structured output).
3. Central provider credentials in secret infrastructure, never passed in prompts/agent logs.
4. Access control to service and underlying model/tool/MCP resources, with an independent tool authorization boundary.
5. Request/response normalization that preserves refusal, partial output, finish reason, model identity, token counts and errors. An OpenAI-compatible envelope is not proof models share semantics.
6. Rate, concurrency, retries, total deadline, circuit-breaker and unknown-outcome handling. Don't retry write-like tool side effects automatically.
7. Explicit fallback policy: refuse fallback to unauthorized provider, region, modality or cheaper but unreviewed safety policy.

## Failure matrix
| Failure | Safe behavior |
|---|---|
| Provider 429/quota | Bounded retry/queue within budget; no uncontrolled fanout |
| Model lacks requested tool type | Return unsupported or approved route, not silent truncation |
| Regional/residency violation | Block fallback and alert owner |
| Provider credential unavailable | Fail closed; never paste key into notebook |
| Mixed tenant identity | Deny model/tool path if principal cannot be proven |
| Model service redirects to new provider | Evaluate stored data/trace and updated policy before release |

The primary evaluation includes **correctness of refusal and authorization**, not solely response quality. No paid request was performed by this reference.

Sources: https://docs.databricks.com/aws/en/unity-gateway and https://docs.databricks.com/aws/en/unity-gateway/concepts and https://docs.databricks.com/aws/en/ai-gateway/
