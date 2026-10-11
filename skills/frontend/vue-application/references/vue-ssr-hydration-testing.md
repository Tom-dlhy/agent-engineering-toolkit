# Vue SSR isolation, hydration and deployment

**Read when:** implementing or testing vue ssr isolation, hydration and deployment.

## Technical method
1. Vue official SSR guide warns about cross-request state pollution from module-level singleton stores. Instantiate app and per-request state at request scope; do not hold mutable current user identity in shared module.

2. Hydration mismatch sources: invalid nested HTML, Math.random(), timezone-specific dates, browser localStorage initial values and different fetched data. Fix deterministically, or render browser-only enhancement after mounted lifecycle; suppressing warnings does not fix structural errors.

3. Vue can recover hydration mismatches but may discard DOM and cost performance. Verify initial server markup equals client VDOM, and ensure serialized state contains no secret/tenant-private field not intended for that actor.

4. Integration test: concurrently SSR tenant A and B, inspect returned personalized HTML/data and isolate stores; simulate locale mismatch, rerun browser hydration and assert no console warnings. Validate no-JS content and links, keyboard, input focus and route navigation in real preview.

5. Verify adapter/runtime and release artifact, private caching, SSR errors and safe request teardown.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://vuejs.org/guide/scaling-up/ssr.html
- https://vuejs.org/guide/best-practices/performance.html
