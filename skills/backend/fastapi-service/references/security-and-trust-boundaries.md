# FastAPI auth, proxy and file upload trust boundaries

**Read when:** adding protected endpoints, multitenancy, CORS/cookies,
public proxy deployments or untrusted user uploads.

## Authorization is not authentication
A verified JWT only says who a caller is and possibly its scopes.
Enforce object and tenant permissions for read, list, update,
delete, export and background work. Bind resource query to the
authenticated principal, never to untrusted tenant ID from body.
Use 401 for missing identity, 403 for denied action, optionally
404 to avoid exposing object existence under a documented policy.

## HTTP security
CORS is browser cross-origin reading policy, not authentication.
Cookie-authenticated mutations require suitable CSRF protection;
bearer token requests differ. Validate trusted reverse proxy
scheme/client IP/host headers with explicit allowed proxy ranges
and documented FastAPI/Uvicorn configuration.

Rate limits and request size/time limits need enforcement at
appropriate API gateway and application boundaries. An
untrusted upload needs streamed-size limits, content inspection
and safe storage names; file extension alone is insufficient.
Never store uploaded file with raw client-controlled filesystem path.

## Negative case checklist
- Missing/expired token, wrong audience/scope.
- Cross-tenant list, guessed object ID, export and update.
- Forged Origin with cookies and unsupported CORS preflight.
- Forged X-Forwarded-Host and trusted-host redirect bypass.
- Oversized multipart/stream, archive traversal/decompression bomb.
- Public error handler must not expose token/provider exception text.

## Test limitations
Mock principal tests prove business check branch, not identity
provider signature/JWKS or reverse proxy behavior. Use
disposable authorized integration and ingress tests when
those systems materially affect security.

Sources: https://fastapi.tiangolo.com/tutorial/security/ ,
https://fastapi.tiangolo.com/tutorial/cors/ ,
https://fastapi.tiangolo.com/advanced/behind-a-proxy/ and
https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html .
