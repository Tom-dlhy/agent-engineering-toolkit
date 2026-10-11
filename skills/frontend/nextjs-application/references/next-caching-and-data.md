# Next.js request caching, streaming and invalidation

**Read when:** the task touches next.js request caching, streaming and invalidation, rather than unrelated framework concerns.

## Decision and implementation
**Version gate:** Next.js caching behavior and API defaults have changed across releases; inspect installed Next major/minor, App Router page config, use of Cache Components, `use cache`, cache tags, route segment settings and hosting adapter before making claims. Distinguish React `cache()` request-scoped memoization from caches shared across requests and deployed CDN caches. Never share authenticated tenant rows in a public cache key.

**Choose route mode:** Static/prerender for stable public content, dynamic SSR for per-request user context, streaming/Suspense for expensive independent portions. Fetch independent data in parallel instead of nested sequential awaits when consistent business transaction isn't required; place meaningful Suspense fallbacks.

**Mutation:** Invalidate or revalidate authoritative data after a server mutation with APIs supported by installed release; ensure browser/navigation cache semantics are tested as well. Avoid assuming revalidation immediately flushes every CDN/SSR cache; verify actual deployment.

**Example hazard:** caching `listOrders()` with global key `orders` will cross tenants if result is user-specific. Prefer explicitly nonshared/private read or a strictly authenticated tenant-and-permission-scoped key with a tested revocation strategy.

**QA:** cold first render, warm render, cross-tenant requests, action then navigation, invalidation across two server replicas, browser back/forward, streaming error, no-JS content. Capture cache headers and server traces; do not use an unknown default as 'SOTA'.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://nextjs.org/docs/app/getting-started/fetching-data
- https://nextjs.org/docs/app/getting-started/caching-and-revalidating
