# Secure review — trust boundaries, OWASP ASVS and system context

**Read when:** security review touches untrusted input, authentication,
authorization, tenant isolation or privileged side effects.

## Establish what can be attacked

Map entrypoints (HTTP routes, webhooks, queue messages, LLM tool output,
file uploads, admin UI), authenticated identities, credentials,
trusted and untrusted data paths, and sinks (SQL, filesystem, network,
mail/payment/cloud commands, logs). Trace whether permission checks execute
for *each* object and action.

### Distinguish authentication and authorization

Authentication asserts identity; authorization decides whether that actor
may perform a specific action on a specific resource. Valid JWT alone does
not establish tenant ownership. With resource /tenants/A/objects/123,
a logged-in user of tenant B must not read/update/delete it via numeric ID
or a bulk export. Check object-level, property-level and function-level
authorization (BOLA/BOPLA/IDOR), as relevant in OWASP ASVS 5.0 sections
covering authorization.

## Contextually select ASVS controls

- Untrusted text → canonicalize once, validate boundaries, parameterize SQL.
- Session/browser app → session binding, CSRF defenses in cookie-authenticated
  state-changing requests, secure cookies, logout and rotation.
- API/bearer token → audience, issuer, expiry and least privilege;
  distinguish 401 vs 403 with resource enumeration risk.
- User-provided URL → controlled allowlist or validated destination plus
  redirect/DNS/IP restrictions against SSRF.
- Upload/file paths → traversal, MIME/content check, scanner where warranted,
  size/decompression budgets and safe storage names.
- Secrets → no hard-coded keys, proper identity/rotation, redaction and
  safe exception handling.

Avoid treating ASVS as a single fixed checklist for every small change.
Record the applicable control family and actual evidence. A passing scanner
or a JWT middleware proves neither complete ASVS compliance nor safe domain
authorization.

## Data-flow review checklist

For each sensitive path:
1. What can an untrusted actor control, including headers/metadata?
2. Where are decode/normalize/validate steps applied, and in what order?
3. Is permission checked against the same resource/tenant being mutated?
4. Are security decisions made before the side effect and again where needed?
5. Can exceptions/logs/metrics expose tokens, signed URLs, PII or prompts?
6. How can an attacker retry, race, enumerate or bypass an approval gate?

## Test matrix

Valid same-tenant access; denied cross-tenant access; token missing/expired/
wrong audience; forged webhook; bulk operation bypass; direct object ID
enumeration; malformed input; duplicate mutations and log-redaction.

Official primary references:
https://owasp.org/www-project-application-security-verification-standard/ and
https://cheatsheetseries.owasp.org/IndexASVS and
https://csrc.nist.gov/pubs/sp/800/218/final .
