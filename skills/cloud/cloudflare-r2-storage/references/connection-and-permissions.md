# Cloudflare R2 object storage — account, binding and identity

**Read when:** connecting Worker or API client to this Cloudflare service, configuring Wrangler or debugging access failure.

## Two separate control planes
Inside Worker use `env.BUCKET` R2 binding; outside Worker use scoped R2 S3-compatible API token and account endpoint, not ordinary Cloudflare dashboard token. Distinguish Cloudflare API token for management/deployment from Workers runtime bindings; **do not put dashboard account API tokens into public requests or JavaScript client bundles**. Wrangler may use OAuth developer login locally, whereas trusted CI uses narrowly scoped secret token. Inspect actual account ID, zone/routes and selected environment before any deploy.

## Minimum permissions
R2 bucket binding rights derive from Worker deploy configuration; S3 API tokens are separately bucket-scoped. Bucket private by default; r2.dev public URL intended for development, not production custom-domain security control.

## TypeScript sketch
~~~typescript
export interface Env { BUCKET: R2Bucket }
export default {
  async fetch(_request: Request, env: Env): Promise<Response> {
    const found = await env.BUCKET.get("health/example.txt")
    if (!found) return new Response("not found", { status: 404 })
    return new Response(found.body)
  }
}
~~~

This is illustrative and needs a project-specific wrangler config/binding, actual Worker compatibility settings and authenticated runtime environment. Pseudocode comments are not functioning JWT checks. Never call live write/deploy operations without the owner's approval.

## First checks
Check exact binding variable names, target environment, account, runtime compatibility, token scopes and least privilege before suggesting a broadly permissive token. Secret bindings stay server-side; don't infer database row authorization from a successful connection.

## Official docs
- https://developers.cloudflare.com/r2/api/workers/workers-api-reference/
- https://developers.cloudflare.com/r2/buckets/public-buckets/
