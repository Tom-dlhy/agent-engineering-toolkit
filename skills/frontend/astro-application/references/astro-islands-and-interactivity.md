# Astro islands, client hydration and shipped JS

**Read when:** implementing or testing astro islands, client hydration and shipped js.

## Technical method
1. Astro renders .astro static HTML without client JavaScript by default. Introduce a framework island only for real interaction. client:load hydrates eagerly, client:idle on idle, client:visible on visibility and client:only skips server rendering.

2. Example intent: <ProductFilters client:visible products={publicProducts} /> within Astro page, with explicit framework integration. No private data should be serialized into island props; server/build reading secrets is not permission to expose props.

3. Use client:only carefully on SEO-critical content because it lacks initial server-rendered markup. Split interactive widget from static heading/product copy and measure real network/CPU/INP.

4. Choose between static shell, dynamic server island and full-page SSR by content personalization and update cadence. Islands do not create authorization boundaries.

5. Test no-JS reading/navigation, scroll visibility hydrate, slow network, CSP, keyboard, responsive states, accessibility and shipped JS size per page.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://docs.astro.build/en/concepts/islands/
- https://docs.astro.build/en/reference/directives-reference/
