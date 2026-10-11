# HTTPX outbound authorization, SSRF and response limits

**Read when:** integrating partner APIs with credentials, user
controlled identifiers, redirects or potentially hostile responses.

## Destination is an authorization decision

Fix scheme+approved origin at deployment. HTTP clients that accept
arbitrary user URL can fetch localhost, cloud metadata and internal
admin endpoints. Validating a URL's string syntax is insufficient
against DNS rebinding, redirects or private IP resolution. Favor
a partner-specific fixed base URL, egress restrictions and redirect
policy. User path segments should be encoded/validated, never
concatenated into unrestricted base URLs.

## Credential boundary

Use managed identity/OAuth token or secret backend where
appropriate, inject auth header only for approved origin and
avoid forwarding it during redirects to a different host.
Credentials must not be in query parameters, exception
messages, access logs or response bodies. Token refresh
must be concurrency-safe to avoid thundering herd.

## Client resource controls

Set connect/read/write/pool timeout, connection limits, TLS
verification, allowable redirects, response byte limit and
safe content-type/schema validation. HTTPX timeout protects
inactivity phases, not automatically an absolute end-to-end
request deadline. Streaming downloads need explicit cap and
close even after decode/error/cancellation.

~~~python
import httpx
client = httpx.AsyncClient(
    base_url="https://partner.example.org",
    timeout=httpx.Timeout(5.0, connect=2.0, pool=1.0),
    limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
    follow_redirects=False,
    verify=True,
)
# Close via async context manager / app lifespan.
~~~

Values are illustrative and must be sized to actual worker/
partner quotas. Avoid disabling verify even in "temporary" fixes.

## Test cases
Disallowed origin, path traversal/redirect target, 3xx credential
leak, 2xx huge body, unsupported content-type, invalid JSON,
invalid signature, expired token, connect/read/pool timeouts.
MockTransport is useful for local behavior but cannot prove
real DNS/TLS/redirect infra rules without integration tests.

Sources: https://www.python-httpx.org/advanced/timeouts/ ,
https://www.python-httpx.org/advanced/resource-limits/ and
https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html .
