# GraphQL, webhook and asynchronous API contracts

**Read when:** choosing GraphQL vs REST, validating signed
webhooks or defining message/event schemas for consumers.

## Style choice

- REST: stable resource operations and HTTP caching/status semantics;
  don't implement a chatty endpoint for every field.
- GraphQL: flexible nested client selection and schema federation;
  budget query depth/complexity, resolver N+1 and field-level auth.
- Webhook: HTTP delivery of business events with sender
  authentication; retries and duplicates are expected.
- Broker event: async independent consumers, partition/order/durability
  semantics, versioned messages and idempotent handlers.

A GraphQL schema cannot enforce tenant-level authorization on its own:
nested resolvers require object/field checks too.

## Signed webhook contract (protocol pseudocode)

~~~text
Event: event_id, schema_version, emitted_at, type, tenant_scope, payload
Signature: provider-defined HMAC over canonical raw body + timestamp
Receiver:
  validate signature using provider-specific rules
  enforce replay window AND durable event_id deduplication
  check tenant authorization and validate schema
  persist/queue required work BEFORE acknowledging success
~~~

Different webhook providers define different canonicalization and
header conventions. Do **not** copy a generic signature formula
into production cryptography code; follow provider documentation and
use constant-time comparison as appropriate. A timestamp window
alone cannot prevent replays within the window.

## AsyncAPI 3.0

AsyncAPI 3.0.0 defines operations, channels and messages
with protocol bindings. A valid schema describes
**message-driven API contracts**, not exactly-once broker
delivery, transaction atomicity or runtime authorization.

## Failure tests

GraphQL nested field authorization, complexity limits, stale
schemas and N+1. Webhook invalid signature, duplicate, late,
out-of-order and redirect behavior. Async consumer version
compatibility, DLQ, replay, message key ordering and idempotency.

Sources: https://spec.graphql.org/ ,
https://www.asyncapi.com/docs/reference/specification/v3.0.0
and https://www.rfc-editor.org/rfc/rfc9110.html .
