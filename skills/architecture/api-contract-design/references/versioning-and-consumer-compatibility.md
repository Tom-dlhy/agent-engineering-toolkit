# API schema evolution, compatibility and pagination

**Read when:** adding/removing fields, changing enum/error semantics,
choosing OpenAPI dialect, paging and deprecation of a public API.

## Check the spec and the toolchain

The OpenAPI Initiative currently lists **3.2.1**, 3.2.0 and 3.1.x
releases; many generators and validators still target 3.0/3.1.
Pin the version actually supported by the project tools instead of
assuming latest automatically works. JSON Schema Draft 2020-12
supports modern keywords; validation of format depends on
vocabulary and validator configuration, not syntax alone.

| Contract change | Often compatible? | Falsifying test |
|---|---|---|
| Add optional response field | Often | Strict consumer rejects unknown field |
| Add enum value | Not universally | Exhaustive generated client breaks |
| Change required to optional | Depends | Existing clients assume populated |
| Remove/rename required | Usually breaking | Older client fails decode |
| Change error status | May break retry policy | Simulate client on old status |
| New pagination order | May break cursors | Concurrent insert shifts results |
| Change auth scope | Behaviorally breaking | Old client gets denied |

## Paging semantics

Offset/limit is simple but deep offsets can be expensive; concurrent
inserts/deletes can move items across pages. Keyset/cursor paging
depends on a stable unique order (including tie-breakers), cursor
validation, filters and tenant identity. An opaque cursor should not
leak sensitive values or allow tampering with isolation boundaries.

## Migration contract

Inventory actual consumers and usage. Publish additive shape where
possible, preserve old behavior for an agreed window, communicate
deprecation, monitor clients, then remove under explicit policy.
Version path/header/schema only where real compatibility warrants it.
A spec diff and generated SDK smoke are useful but insufficient:
test actual serialized wire behavior and representative consumers.

## Security and limits

Paginate bounded results; cap filters and GraphQL-like query cost
where appropriate, never use raw user-controlled SQL identifiers.
Treat API contract as authorization and privacy surface, not only JSON.

Sources: https://spec.openapis.org/oas/ ,
https://json-schema.org/draft/2020-12 and
https://www.rfc-editor.org/rfc/rfc9110.html .
