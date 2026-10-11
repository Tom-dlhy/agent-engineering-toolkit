# Node async I/O, AbortSignal, context and shutdown

**Read when:** implementing outbound fetch, deadlines, long-lived Node
requests, AsyncLocalStorage, CPU-heavy handlers or graceful stop.

## Fetch with bounded cancellation

~~~typescript
async function getPartner(id: string, signal: AbortSignal): Promise<unknown> {
  const url = new URL(
    "/resources/" + encodeURIComponent(id), "https://partner.example.org"
  );
  const response = await fetch(url, {
    headers: { Accept: "application/json" },
    signal,
    redirect: "error",
  });
  if (response.status === 404) return null;
  if (response.status === 429) throw new Error("rate_limited");
  if (!response.ok) throw new Error("upstream_error");
  return response.json() as Promise<unknown>;
}
~~~

The upstream base must be approved and credentials scoped to it.
AbortSignal cancels pending local work but does not roll back
an external POST already committed. Preserve stable idempotency
keys and reconcile unknown remote outcomes.

## AsyncLocalStorage is not auth
Store non-sensitive request correlation in a fresh context.
Test propagation across framework callbacks and concurrent
requests; no global mutable current-tenant variable. Don't
log or propagate credentials/PII in arbitrary baggage/headers.

## CPU and resources
Node's event loop can be blocked by CPU-heavy synchronous
work even though outbound fetch is asynchronous. Use bounded
worker_threads, child processes or job queues where needed.
Apply per-tenant/partner admission to API calls and
database connections, not unlimited Promise.all fanout.

## Graceful termination
On SIGTERM stop accepting new requests, drain or cancel
existing work under a finite deadline, close DB/HTTP clients,
and persist durable jobs before process exit. In-memory timers
and unpersisted callbacks can be lost when replica shuts down.

Test client disconnect, concurrent context IDs, stale auth,
unknown commit timeout, invalid JSON, pool exhaustion,
worker restart and no hanging handles.

Official: https://nodejs.org/api/globals.html#fetch ,
https://nodejs.org/api/async_context.html ,
https://nodejs.org/api/worker_threads.html .
