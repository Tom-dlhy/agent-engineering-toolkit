# Cloudflare integration coordinator — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Route runtime/Pages to cloudflare-workers-runtime, R2 to cloudflare-r2-storage, D1 to cloudflare-d1-database, Access to cloudflare-access-security. KV/Queues/Durable Objects remain explicit future candidate only when real implementation demand exists.

## Implementation decisions
Worker runtime receives env bindings and secrets; Wrangler/deployment accesses Cloudflare control plane via scoped token or developer OAuth. Runtime binding credentials are not dashboard tokens. Preview/prod env can bind different databases/buckets.

## Starter illustration
~~~bash
npx wrangler types # local types only
# Inspect wrangler.jsonc environment bindings before deploy; don't run deploy automatically
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://developers.cloudflare.com/workers/runtime-apis/bindings/
- https://developers.cloudflare.com/workers/configuration/secrets/
