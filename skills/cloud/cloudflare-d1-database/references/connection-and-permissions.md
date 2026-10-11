# Cloudflare D1 SQLite database — account, binding and identity

**Read when:** connecting Worker or API client to this Cloudflare service, configuring Wrangler or debugging access failure.

## Two separate control planes
Bind database in wrangler JSON/TOML and access via `env.DB` in Worker; deployment uses scoped Cloudflare account API token for migrations, not a SQL username/password. Distinguish Cloudflare API token for management/deployment from Workers runtime bindings; **do not put dashboard account API tokens into public requests or JavaScript client bundles**. Wrangler may use OAuth developer login locally, whereas trusted CI uses narrowly scoped secret token. Inspect actual account ID, zone/routes and selected environment before any deploy.

## Minimum permissions
Binding attached to Worker allows querying configured database; management/migrations via scoped Wrangler deployment account token. Never interpolate raw SQL query parameters, use `.bind()` and validate identifiers.

## TypeScript sketch
~~~typescript
export interface Env { DB: D1Database }
export default {
  async fetch(_req: Request, env: Env): Promise<Response> {
    const row = await env.DB.prepare("SELECT id FROM items WHERE id = ?")
      .bind("synthetic-id").first<{id: string}>()
    return Response.json({ found: Boolean(row) })
  }
}
~~~

This is illustrative and needs a project-specific wrangler config/binding, actual Worker compatibility settings and authenticated runtime environment. Pseudocode comments are not functioning JWT checks. Never call live write/deploy operations without the owner's approval.

## First checks
Check exact binding variable names, target environment, account, runtime compatibility, token scopes and least privilege before suggesting a broadly permissive token. Secret bindings stay server-side; don't infer database row authorization from a successful connection.

## Official docs
- https://developers.cloudflare.com/d1/worker-api/
- https://developers.cloudflare.com/d1/worker-api/prepared-statements/
