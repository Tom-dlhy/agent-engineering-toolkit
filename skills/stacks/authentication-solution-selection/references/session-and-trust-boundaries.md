# Session architecture, token validation and negative access tests

Read when: comparing cookie sessions vs bearer tokens, OIDC claims, MFA/recovery and client/server authorization boundaries.

## Session is not a UI login state
- Browser login state is a **display hint**; all private server handlers and direct endpoints must enforce user identity and object/tenant authorization.
- For browser sessions prefer secure `HttpOnly` cookies with `Secure`, an appropriate `SameSite` strategy and CSRF mitigation. `SameSite` is defense in depth, **not** a universal replacement for a CSRF token.
- Do not store access/refresh/session tokens in `localStorage` or `sessionStorage` for convenience; JS XSS can read them. Prefer session cookies/BFF when feasible.
- OIDC authorization callback must validate protocol state and redirect handling; validate ID token `iss`, `aud`, expiry and nonce **where applicable**, via a maintained SDK.
- Beware expired JWTs, key rollover/JWKS cache, revocation semantics: stateless validation is not instant revocation without an additional mechanism.
- MFA/passkeys should match actual risk level; NIST notes phishing-resistant cryptographic methods such as WebAuthn/FIDO2. OTPs typed into a site do not provide the same phishing resistance.
- Machine/service principals use different flows from human login; don't share web browser cookies with API workers.

## Negative route fixtures
~~~text
missing session -> 401 or safe unauthenticated result
expired/revoked session -> denied, no stale authorization
valid user, wrong tenant document ID -> 403/404 by declared policy
user role changes -> sensitive operation rechecks current permissions
untrusted redirect next=https://attacker.test -> rejected
forged callback state / nonce mismatch -> rejected
stolen session after logout -> should be revoked per stated contract
cross-site form mutation without CSRF proof -> rejected as applicable
bad aud/iss/key signature -> rejected even if token parses
~~~
These are **required test intentions**, not claims that an auth SDK performs them by default. Check installed provider's actual session strategy (DB/cookie/JWT). Better Auth's documented cookie-based sessions differ from other library variants and can be configured differently; do not transfer default behavior to every provider.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html and https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ and https://better-auth.com/docs/concepts/session-management and https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
