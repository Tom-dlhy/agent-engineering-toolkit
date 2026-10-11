---
name: python-observability
domain: backend
version: "2.0.0"
description: >-
  Use when working on Python structured JSON logging, contextvars correlation IDs, OpenTelemetry traces/metrics, redaction and production incident signals. Do not use for generic aesthetic logging or as a replacement for infrastructure SRE monitoring.
---

# Python observability — actionable signals and safe context

## Selection
1. Determine operational questions first: which request? which tenant without logging PII? which upstream? what latency/cost? what failed?
2. Prefer standard logging with JSON adapter/formatter, stable event names, safe correlation and trace IDs, log sampling and retention controls.
3. Use OpenTelemetry spans/metrics for distributed path, attach HTTP/database/LLM instrumentation as configured, not duplicated per request.
4. Correlation headers received from callers are untrusted; sanitize length/charset and never use as access or auth identifiers.
5. Exclude raw secrets, bearer tokens, signed URLs, model prompts/responses, customer payload and PII by default; opt-in diagnostic capture requires permissions, redaction and retention.
6. Test concurrent requests, error/cancellation, streaming and deployments with real exporters or explicitly mark gaps.

## Deep references
- [Safe JSON logging and context propagation](references/logging-and-context.md) — read when implementing formatter, ContextVars, request IDs, log boundaries and redaction.
- [OTel, SLO and model telemetry](references/tracing-metrics-and-operations.md) — read when implementing traces/metrics, cost and token usage or incident dashboards.

## Related
observability-sre handles global SLO/alerts, fastapi-service owns middleware and inbound transport, python-http-clients owns outbound adapter traces.

## Exit
Fields and privacy policy documented; tracing/metrics aggregation and alerts are actionable; no fabricated test or production signal claims.
