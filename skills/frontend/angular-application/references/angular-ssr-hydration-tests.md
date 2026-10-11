# Angular hybrid route rendering, hydration and cache

**Read when:** implementing or testing angular hybrid route rendering, hydration and cache.

## Technical method
1. Angular SSR hybrid routing supports RenderMode.Client (CSR), RenderMode.Prerender (build HTML) and RenderMode.Server (per-request SSR) in app.routes.server.ts. Only use routes supported by configured angular/ssr and outputMode.

2. Prefer browser-only initialization via afterNextRender instead of divergent isPlatformBrowser template markup that causes layout shift/hydration mismatch. Check invalid HTML, timezone and dynamic IDs.

3. HttpClient transfer cache can serialize selected GET/HEAD responses; official defaults exclude credentialed/private headers and no-store controls under documented conditions. Explicit overrides must be reviewed for accidental PII leak.

4. SSR useValue providers configured globally are not necessarily per-request; avoid storing current authenticated user in a root global value. Test two simultaneous users and ensure isolated serialized HTML.

5. Run ng build, template strict mode, initial SSR/hydration browser test, real deep links, redirects, transfer cache behavior, no-JS content and INP/LCP/CLS observation.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://angular.dev/guide/hybrid-rendering
- https://angular.dev/guide/hydration
