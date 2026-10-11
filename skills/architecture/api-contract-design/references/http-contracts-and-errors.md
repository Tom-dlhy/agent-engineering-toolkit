# HTTP API contracts, conditional requests and errors

**Read when:** designing HTTP methods, replay semantics, errors, status,
concurrency preconditions or state-changing API endpoints.

## RFC 9110: methods are client promises

GET/HEAD are safe; PUT, DELETE and safe methods are idempotent
in intended server effects. POST and PATCH usually require an explicit
replay contract. A custom Idempotency-Key only helps when the *server*
has durable deduplication and payload binding; assigning a random new
key for each retry defeats it.

| Operation | Typical response | Verify |
|---|---|---|
| GET | 200/304, bounded list | No side effect, tenant ownership, caching |
| POST create | 201 + Location where appropriate | Duplicate request after timeout |
| PUT replace | 200/204 and known resource | Replace semantics, conditional version |
| PATCH | 200/204 or documented validation error | Missing vs explicit null |
| DELETE | 204/404 by contract | Repeating leaves requested state absent |
| Async work | POST 202 + job status | Durable state, cancellation, retry |

Strong ETags and If-Match support optimistic concurrency: stale
updates may receive **412 Precondition Failed**. A 409 can indicate
a separate business state conflict. A GET is not safe if it charges
a payment or sends an email.

## RFC 9457 — Problem Details

~~~json
{
  "type": "https://api.example.org/problems/conflict",
  "title": "Resource conflict",
  "status": 409,
  "detail": "The supplied version is stale.",
  "instance": "/requests/example-trace-id"
}
~~~

Set Content-Type: application/problem+json. Problem type URIs
and machine-readable extension fields should be stable; do not
expose SQL/provider exception traces or secret-bearing URLs.
RFC 9457 **obsoletes RFC 7807**.

## Nullability and transport contracts

An omitted PATCH field is not equivalent to explicit JSON null.
Define whether null means clear/remove, invalid value or
domain-specific absence. Distinguish request DTO, domain object,
ORM model and public response; returning DB rows directly risks
private fields and lazy-loading failures.

## Tests

Exercise 401/403/404/409/412/422/429/5xx, stale ETag,
missing/null, duplicated POST after timeout, malformed payload,
tenant isolation, pagination, quota and structured safe errors.
A valid OpenAPI file is not a working HTTP implementation.

Sources: https://www.rfc-editor.org/rfc/rfc9110.html ,
https://www.rfc-editor.org/rfc/rfc9457.html and
https://www.rfc-editor.org/rfc/rfc5789 .
