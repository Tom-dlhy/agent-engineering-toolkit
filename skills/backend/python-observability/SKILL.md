---
name: python-observability
domain: backend
version: "2.1.0"
description: >-
  Use when implementing Python structured logs, request correlation,
  OpenTelemetry traces/metrics, log privacy and runtime diagnostic signals.
  Do not substitute for generic print debugging or SRE alert/incident governance.
---

# Python observability — truthful signals without data leakage

## Method
1. List diagnostic questions and required signals before instrumentation:
   which request/tenant **reference**, external dependency, queue wait,
   error category, latency, useful outcome and model usage.
2. Use structured JSON logs with stable fields and carefully sanitized
   context; correlation header is **untrusted input**, not identity.
3. `ContextVar` context usually follows asyncio tasks but not every thread
   or queue logger formatter. Capture context **at LogRecord creation**
   if formatting on another thread; test concurrent isolation.
4. Use OpenTelemetry parent-child spans + metrics and semantic conventions
   supported by pinned SDK/instrumentation; avoid duplicate instrumentation.
5. Control trace propagation/baggage across trust boundaries. **Baggage can
   carry user data in outbound headers**; never attach secrets/PII.
6. Bound cardinality, sampling and retention. Use route templates, not
   raw user paths/IDs as metric dimensions; instrument pool and provider
   waits as well as handler duration.
7. Test error/cancellation/stream paths, exporter outages and redaction.
   No fabricated telemetry claims when exporter/collector unavailable.

## References
- [JSON logs, correlation and context](references/logging-and-context.md) — read when implementing ContextVar/formatter.
- [OTel metrics, traces and operations](references/tracing-metrics-and-operations.md) — read when instrumenting API/DB/model.
- [Trace propagation, cardinality and privacy](references/propagation-cardinality-and-privacy.md) — read when instrumenting across services or sensitive payloads.

## Boundaries
observability-sre owns alerting/SLO policy, fastapi-service owns HTTP
middleware, llm-integration owns model output evaluation.

## Exit
Diagnostic signal coverage, privacy review, context isolation, cardinality
budgets, actual exported trace/metric verification or explicit gaps.
