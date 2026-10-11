# Python OpenTelemetry context propagation, privacy and cardinality

**Read when:** sending traces across HTTP, queues or LLM adapters,
building metric dimensions or using async/thread log correlation.

## Trace propagation is not authorization

W3C traceparent and tracestate support cross-service span correlation,
not user authentication. Headers arriving from public clients are
untrusted; don't derive tenant/resource access from them.
Baggage can be propagated to downstream systems; avoid PII, raw
tokens, email, user prompts, tenant secrets and unbounded values.
Separate internal correlation ID from trace IDs and security identity.

## ContextVar scope
Context variables can propagate across asyncio tasks under normal
task-creation context copying, but not automatically through every
thread, logging queue or remote job. If a formatter operates in
another context, snapshot allowed fields into LogRecord when
it is emitted. Reset request context in finally and test two
simultaneous requests with different IDs and cancellations.

## Cardinality and aggregation

Good metric labels: route template (e.g. /resources/{id}),
method, status group, error class and bounded provider name.
Bad: raw path with customer ID, exact correlation ID,
document hash or arbitrary prompt text — these can create
effectively unlimited time series and leak sensitive values.

Use histogram for latency (pool, DB, provider, job queue and
useful end-to-end request), counters for errors/attempts,
gauges for active workers/backlog. Sampling and storage
retention are policy choices; do not assume traces/logs can
be retained indefinitely for debugging.

## Exporter failure
Telemetry must not normally break primary user request when
collector is unavailable. Bound buffered exporter queues,
drop safely under pressure and monitor loss rate. Test
collector timeout, cancellation, concurrent request context
and no sensitive fields in serialized span/log attributes.

## LLM-specific telemetry
Track model/provider/version, approximate token usage,
latency/status and cost where usage metadata is returned.
Do not claim the response quality is measured by latency
and avoid raw prompts/responses by default.

Sources: https://opentelemetry.io/docs/languages/python/instrumentation/ ,
https://www.w3.org/TR/trace-context/ and
https://www.w3.org/TR/baggage/ .
