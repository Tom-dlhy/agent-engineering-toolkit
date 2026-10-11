---
name: vue-application
domain: frontend
version: "0.2.0"
description: >-
  Use when building Vue 3 Composition API components or Nuxt 4 applications with reactivity, useFetch/useAsyncData, SSR, route/data lifecycle and Vue security. Do not use for Svelte runes, React hooks or Angular signals.
---

# Vue/Nuxt architecture — request-safe reactivity and SSR

## Implementation procedure
1. Determine Vue/Nuxt major, Composition API versus legacy Options API, Nitro hosting target, Vue Router/Pinia needs and SSR mode.
2. Use `ref`/`reactive` for owned state, `computed` for pure derived values; `watch` or `watchEffect` for needed external side effects with cleanup, not to propagate copied derivations.
3. Vue SSR creates per-request app/store state; **never reuse module-scoped mutable user/tenant state across SSR requests**.
4. In Nuxt use `useFetch`/`useAsyncData` for SSR-aware transfer/caching, not raw `$fetch` in a page setup causing duplicate server/client fetching without reason.
5. Apply `server/api` or server routes for private DB and secrets with per-request authorization; route middleware improves navigation UX but is not server-side API permission.
6. Prevent unsafe `v-html` with untrusted content; handle UTC/timezone, random IDs and invalid HTML nesting that cause hydration mismatches.
7. Test payload serialization, Nuxt key/dedupe invalidation, per-request state isolation, browser hydration, accessibility and built artifact deployment.

## Targeted expertise (open only when needed)
- [refs, computed, watch lifecycle, component contracts and composition](references/vue-reactivity-and-components.md) — **read when** refs, computed, watch lifecycle, component contracts and composition.
- [Nuxt 4 data fetching, private API, authorization and payload cache](references/nuxt-routing-data-security.md) — **read when** Nuxt 4 data fetching, private API, authorization and payload cache.
- [SSR request isolation, hydration pitfalls, tests and deploy verification](references/vue-ssr-hydration-testing.md) — **read when** SSR request isolation, hydration pitfalls, tests and deploy verification.

## Boundaries and completion
Choose the one framework-specific skill matching the actual repository. Delegate visual tokens and UI library APIs to design/ui, security audit to quality, endpoint contracts to backend, and deployment infrastructure to Cloud. Do not install frameworks just to follow a skill. Complete with evidence from typecheck/build, negative authorization tests, realistic browser hydration and documented version limitations. Treat examples as illustrative until executed against pinned dependencies.
