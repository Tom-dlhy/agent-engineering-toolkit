---
name: angular-application
domain: frontend
version: "0.2.0"
description: >-
  Use when developing Angular standalone components, Signals, router, HttpClient, forms, DI, SSR/hybrid rendering and hydration. Do not use for Vue Composition API, SvelteKit form actions or React Server Components.
---

# Angular — standalone architecture, signals and hybrid rendering

## Implementation procedure
1. Inspect exact Angular major, zoneless/change-detection setup, standalone conventions, router and SSR output mode; use installed CLI schematic and docs for that release.
2. Prefer standalone components, typed signals with `computed()` derivations, template control flow, scoped services/DI and explicitly owned asynchronous resources.
3. Use `effect()` to synchronize with non-reactive APIs, not to copy one signal to another; avoid state propagation cycles.
4. Define routes/guards/resolvers with service authorization independently: **client route guards are not API access control**. Typed HTTP client errors and interceptors need explicit failure handling.
5. Use `RenderMode.Client`, `RenderMode.Server`, `RenderMode.Prerender` per route when SSR configured, and hydrate without browser-dependent server markup.
6. Beware SSR provider `useValue` at module/global level persisting across requests; do not store current user in cross-request singleton.
7. Verify `ng build`, template typecheck, testing harness, route protected behavior, hydration mismatch, network prefetch/transfer cache and deployment rewrite.

## Targeted expertise (open only when needed)
- [signals, computed/effect, standalone DI, typed forms](references/angular-signals-di-and-forms.md) — **read when** signals, computed/effect, standalone DI, typed forms.
- [router, HTTP, authz, interceptors and data boundary](references/angular-router-http-security.md) — **read when** router, HTTP, authz, interceptors and data boundary.
- [hybrid SSR/SSG, transfer cache, hydration and release QA](references/angular-ssr-hydration-tests.md) — **read when** hybrid SSR/SSG, transfer cache, hydration and release QA.

## Boundaries and completion
Choose the one framework-specific skill matching the actual repository. Delegate visual tokens and UI library APIs to design/ui, security audit to quality, endpoint contracts to backend, and deployment infrastructure to Cloud. Do not install frameworks just to follow a skill. Complete with evidence from typecheck/build, negative authorization tests, realistic browser hydration and documented version limitations. Treat examples as illustrative until executed against pinned dependencies.
