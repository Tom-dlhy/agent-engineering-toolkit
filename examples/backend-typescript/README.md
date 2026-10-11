# TypeScript/Node HTTP example — executable educational slice

Purpose: demonstrate runtime schema validation on unknown JSON, route error
mapping, injected authentication rather than trusting a header, tenant-scoped
reads, idempotent local replay and server shutdown. Node's built-in test runner
can execute erasable TypeScript on the pinned Node 24 runtime without third-party
runtime dependencies.

From repo root on Node 24+:

~~~bash
node --test examples/backend-typescript/tests/*.test.ts
~~~

This example does **not** prove strict TypeScript typechecking. Production
projects must pin and run tsc with their actual Node type definitions.
It is **not production-ready**: no trusted identity provider, persistent
database, durable idempotency, CSRF/CORS/TLS ingress, rate limits, metric
exporter, audit retention or hardened resource quotas. In-memory Map cannot
prevent duplicate external side effects after crashes/redeploys.
Never expose this example as a real API.

Official docs: https://nodejs.org/api/typescript.html ,
https://nodejs.org/api/test.html and
https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/ .
