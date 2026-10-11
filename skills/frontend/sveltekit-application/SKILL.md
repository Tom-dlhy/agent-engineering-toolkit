---
name: sveltekit-application
domain: frontend
version: "0.2.0"
description: >-
  Use when building Svelte 5 or SvelteKit 2 with runes, server/universal loads, form actions, hooks, authentication, SSR or progressive enhancement. Do not use for Vue watchers, Next.js server actions or Angular signals.
---

# Svelte/SvelteKit — runes, load boundaries and form correctness

## Implementation procedure
1. Inspect Svelte 5 versus legacy syntax and SvelteKit release/adapter; avoid mixing Svelte 4 `export let` idioms with Svelte 5 `$props()` without an explicit migration plan.
2. Use `$state` for mutable component state, `$derived` for pure computed values and `$effect` for browser-only external effects; `$effect` does **not** run during SSR.
3. `+page.server.ts`/`+layout.server.ts` run only on server; universal `+page.ts`/`+layout.ts` can also run in browser. Never import private env/DB into universal load.
4. Use server form actions in `+page.server.ts` for progressive mutations, validate `request.formData()` and authorize actor/resource; `use:enhance` optimizes UX but isn't a security control.
5. Access identity through `hooks.server.ts` and `event.locals` with per-request lifecycle; prevent data leakage from shared module/global state.
6. Check CSRF settings, cookie SameSite/secure rules and allowed origins for deployed proxy; prevent `{@html ...}` injection with untrusted content.
7. Test direct POST actions, invalid form, disabled JS fallback, cross-tenant access, streamed loading, SSR hydration and adapter-specific build.

## Targeted expertise (open only when needed)
- [Svelte 5 state/derived/effect and typed component API](references/svelte-runes-and-components.md) — **read when** Svelte 5 state/derived/effect and typed component API.
- [server/universal load, form actions, locals, cookies and auth](references/sveltekit-load-actions-security.md) — **read when** server/universal load, form actions, locals, cookies and auth.
- [SSR state isolation, enhancements, adapter and E2E tests](references/sveltekit-ssr-and-deployment.md) — **read when** SSR state isolation, enhancements, adapter and E2E tests.

## Boundaries and completion
Choose the one framework-specific skill matching the actual repository. Delegate visual tokens and UI library APIs to design/ui, security audit to quality, endpoint contracts to backend, and deployment infrastructure to Cloud. Do not install frameworks just to follow a skill. Complete with evidence from typecheck/build, negative authorization tests, realistic browser hydration and documented version limitations. Treat examples as illustrative until executed against pinned dependencies.
