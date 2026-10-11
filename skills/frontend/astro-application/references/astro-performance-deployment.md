# Astro adapter, image performance and deployment QA

**Read when:** implementing or testing astro adapter, image performance and deployment qa.

## Technical method
1. Use static generation for stable public content, SSR adapters for request-dependent routing/personalization and server islands. Adapter Node/Cloudflare/Vercel differences affect filesystem, cookie, runtime streaming and edge APIs.

2. Measure LCP/CLS/INP from lab plus field where available; set image dimensions, responsive srcset, compression and appropriate font loading. Do not lazy-load the LCP hero blindly; a good score on one machine isn't production proof.

3. Ensure correct cache-control for private SSR fragments; preview secrets and routes must match production. Verify 404/redirect/header behavior, SEO metadata, canonical/sitemap and no-JS content.

4. Bundle third-party interactive islands deliberately, test JS-disabled static shell, browser console hydration, progressive server island fallback and failed network.

5. Release with pinned Astro/adapter, production build, Playwright deep-route smoke, role-based access negative tests and rollback artifact. Record unsupported performance/platform assumptions.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://docs.astro.build/en/guides/on-demand-rendering/
- https://docs.astro.build/en/guides/images/
- https://web.dev/articles/vitals
