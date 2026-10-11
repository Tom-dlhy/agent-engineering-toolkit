# Cloudflare Workers and Pages runtime — account, binding and identity

**Read when:** connecting Worker or API client to this Cloudflare service, configuring Wrangler or debugging access failure.

## Two separate control planes
wrangler CLI authenticated with a narrowly scoped Cloudflare API token; runtime services via bindings passed as env, not a management API token. Distinguish Cloudflare API token for management/deployment from Workers runtime bindings; **do not put dashboard account API tokens into public requests or JavaScript client bundles**. Wrangler may use OAuth developer login locally, whereas trusted CI uses narrowly scoped secret token. Inspect actual account ID, zone/routes and selected environment before any deploy.

## Minimum permissions
Token permissions scoped to intended account/zone/Workers edit for deployment; production runtime secret binding not equivalent to dashboard/API token. Separate preview/production vars and domains.

## TypeScript sketch
~~~typescript
export interface Env { API_TOKEN: string }
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return new Response("ok", {status: 200})
  }
}
// API_TOKEN is a secret binding. Never return its value.
~~~

This is illustrative and needs a project-specific wrangler config/binding, actual Worker compatibility settings and authenticated runtime environment. Pseudocode comments are not functioning JWT checks. Never call live write/deploy operations without the owner's approval.

## First checks
Check exact binding variable names, target environment, account, runtime compatibility, token scopes and least privilege before suggesting a broadly permissive token. Secret bindings stay server-side; don't infer database row authorization from a successful connection.

## Official docs
- https://developers.cloudflare.com/workers/configuration/secrets/
- https://developers.cloudflare.com/workers/runtime-apis/bindings/
