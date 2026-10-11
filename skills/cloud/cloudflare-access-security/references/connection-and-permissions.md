# Cloudflare Access Zero Trust — account, binding and identity

**Read when:** connecting Worker or API client to this Cloudflare service, configuring Wrangler or debugging access failure.

## Two separate control planes
Configure Access app and Include/Require/Exclude policies via scoped Zero Trust console/API; origin verify Access JWT signature/issuer/audience as required, don't trust bare email headers. Distinguish Cloudflare API token for management/deployment from Workers runtime bindings; **do not put dashboard account API tokens into public requests or JavaScript client bundles**. Wrangler may use OAuth developer login locally, whereas trusted CI uses narrowly scoped secret token. Inspect actual account ID, zone/routes and selected environment before any deploy.

## Minimum permissions
Access policy controls who passes proxy; per-resource tenant authorization stays in origin code. Service tokens for machine-to-machine and interactive identity are distinct; service token credentials stay secrets.

## TypeScript sketch
~~~typescript
// Pseudocode guard at trusted origin; use an audited JWT validator:
const jwt = request.headers.get("Cf-Access-Jwt-Assertion")
if (!jwt) return new Response("Unauthorized", { status: 401 })
// Verify JWT signature with Access JWKS, issuer, app audience and expiry.
// This is NOT a working verifier. Never accept merely presence of header.
~~~

This is illustrative and needs a project-specific wrangler config/binding, actual Worker compatibility settings and authenticated runtime environment. Pseudocode comments are not functioning JWT checks. Never call live write/deploy operations without the owner's approval.

## First checks
Check exact binding variable names, target environment, account, runtime compatibility, token scopes and least privilege before suggesting a broadly permissive token. Secret bindings stay server-side; don't infer database row authorization from a successful connection.

## Official docs
- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/
- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/application-token/
