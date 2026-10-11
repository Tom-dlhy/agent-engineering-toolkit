# FastAPI streaming, SSE, WebSockets and disconnect

**Read when:** implementing streaming model inference, real-time
updates, server-sent events, WebSockets or large responses.

| Need | Transport | Main risk |
|---|---|---|
| Single JSON result | Normal endpoint | Deadline, payload limit |
| Server pushes ordered updates | SSE/EventSource | Proxy buffering, reconnect IDs |
| Bidirectional stateful messages | WebSocket | Auth handshake, idle/heartbeat |
| Long unreliable inference | Durable job + status | Streaming is not persistence |
| Large files/chunks | StreamingResponse / FileResponse | Cancellation and partial writes |

Recent FastAPI docs describe JSON Lines and SSE support; check the
pinned FastAPI/Starlette version and actual APIs before using
new response classes.

## Protocol and resources

Streaming means producing chunks incrementally, not buffering
the full model completion and chunking afterwards. Response
handlers must close upstream streams when downstream disconnects.
Use cancellation-safe finally blocks, bounded queues and
producer backpressure to avoid runaway RAM for slow clients.
A partial JSON token stream is not a validated complete JSON
document; application must define completion and cancellation
semantics before persisting results.

## Schematic cleanup (not a full FastAPI route)

~~~python
async def chunks(upstream):
    try:
        async for item in upstream:
            yield encode_event(item)  # application-specific
    finally:
        await upstream.aclose()
~~~

The upstream class, encoding function and response wrappers are
intentionally project-specific. Ensure async generator cleanup
and dependency lifetimes match FastAPI version and streaming
response behavior.

## Check
Client disconnect mid-stream, slow consumer, upstream 429/503,
invalid final schema, output size, simultaneous streams,
expiring credentials, proxy idle timeout, heartbeat/reconnect
and absent complete terminal event. Don't log full prompts or
PII in stream instrumentation.

Sources: https://fastapi.tiangolo.com/tutorial/server-sent-events/ ,
https://fastapi.tiangolo.com/tutorial/stream-json-lines/ and
https://fastapi.tiangolo.com/advanced/events/ .
