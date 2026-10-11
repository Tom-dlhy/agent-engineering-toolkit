# Astro content collections, server islands and actions

**Read when:** implementing or testing astro content collections, server islands and actions.

## Technical method
1. Use content collections with schema validation and stable slugs for content-oriented sites. Schema and content loaders evolve across Astro majors: verify installed version before migrating collection configuration.

2. server:defer renders server islands independently with fallback and requires a compatible deployment adapter. A personalized fragment needs its own per-request authentication and private cache policy even when the static shell is public.

3. Illustrative: <AccountSummary server:defer><p slot='fallback'>Loading...</p></AccountSummary>. AccountSummary itself must validate session and resource access; never put user secrets in static template or HTML cache.

4. Astro Actions/server endpoints can perform mutations where runtime supports them; validate request schema, actor and CSRF/origin, choose errors and idempotency. SSR vs build-time execution affects freshness and private data handling.

5. Tests: missing slug/schema error, dynamic route unauthorized, cross-tenant island URL, stale cache after revocation, public preview code path and rollback.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://docs.astro.build/en/guides/content-collections/
- https://docs.astro.build/en/guides/server-islands/
- https://docs.astro.build/en/guides/actions/
