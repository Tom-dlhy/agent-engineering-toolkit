# SvelteKit SSR lifecycle, adapter and test suite

**Read when:** implementing or testing sveltekit ssr lifecycle, adapter and test suite.

## Technical method
1. Choose adapter-node/static/cloudflare/vercel based on dynamic form actions, private load, runtime API and deployment requirements. Static output cannot handle server mutation without a separate backend.

2. Server code with module-level currentUser or cached mutable per-user state is a cross-request leak; use event.locals. Mark private imports $lib/server or $env/*/private as appropriate and keep them out of universal load/client bundle.

3. Hydration is sensitive to locale/timezone/random values and invalid nested markup. Test production preview on direct deep links, login/logout flow, disabled JavaScript and form use:enhance progression.

4. Check cache-control of SSR private pages, redirects, streamed promises, canceled client navigation, large form bodies and proxy Origin behavior. Do not report success merely because vite dev works.

5. Run svelte-check, typecheck, build, adapter smoke and Playwright on real browser; monitor data leakage across concurrent users and verify no cookie/session text in logs.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://svelte.dev/docs/kit/state-management
- https://svelte.dev/docs/kit/server-only-modules
- https://svelte.dev/docs/kit/adapters
