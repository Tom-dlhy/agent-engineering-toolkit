# OpenTelemetry and Python production diagnostics

**Read when:** tracing cross-service workflows or measuring throughput, tail latency, LLM usage/cost, retries and error budget.

## Architecture
ASGI request span → application use case span → DB/HTTP/LLM provider span → async job link. Use W3C trace context and standards-supported instrumentation, not a home-grown distributed trace system. Install OTel SDK/exporter in application bootstrap; reusable libraries should depend only on API.

## Signals
| Signal | Purpose | Cardinality/privacy cautions |
|---|---|---|
| Request rate/error/latency histograms | SLOs and capacity | Use route template, not raw resource ID |
| DB pool wait/transactions | Lock/pool health | Avoid query literal parameter logging |
| Outbound HTTP attempts/429/5xx | Retry storms and dependency faults | No sensitive full URL/header |
| LLM queue wait/inference latency | Provider bottleneck | Model/deployment alias controlled |
| LLM token input/output and spend | Costs/quotas | May not exist on every response/provider |
| Tool call outcomes | Agent correctness/side effects | No arguments or raw user data by default |
| Jobs oldest age/DLQ | Background recoverability | No payload in metric label |

## Span events
Mark error category, retry count, model alias, provider and allowed tenant hash (if truly needed) — not raw prompts, secrets or emails. Model/provider request IDs are useful diagnostics if safe and authorized. Sampling can hide rare failure traces; consider preserving errors and consistent upstream/downstream sampling policies.

## Observability and privacy

Define data minimization, tenant boundaries, log access, retention and alert routing. Raw model prompts and tool results can contain extremely sensitive data; default to off. If regulated, ensure data residency of exporters and third-party callbacks as well as model provider.

## Incident decision tree
If p99 increases: separate queue wait, HTTP pool wait, provider inference, database locks and local CPU. If spend spikes: check retry amplification, prompt/token changes, per-tenant usage and fallback to expensive models. If failures rise: correlate status codes, SDK exceptions, quotas and deployments, not only top-level 503 count.

## Verify
Generate synthetic healthy/error samples in authorized staging, check traces correlate inbound and outbound spans, metrics reach exporter, and no forbidden payload lands in logs. Actual OTel Python log SDK is still described as in development; treat trace/metric maturity separately.

Official: https://opentelemetry.io/docs/languages/python/instrumentation/ and https://opentelemetry.io/docs/languages/python/ .
