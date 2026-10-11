# Frontend engineering — primary-source refactor audit

Research date: 2026-10-11. Base: main after merged Cloud PR #19.
Owner charter: consistent quality for all skills, explicit positive/negative
triggers, reuse before creation, selective deep references, real expertise
rather than recommendations without implementation details.

## Starting audit and design decisions

Four existing frontend skills:
- react-architecture: short guidance on state/effects, no deep references.
- nextjs-application: short SSR/client/caching guidance, version risks.
- tanstack-start: short routing/server function guide, missed CSRF nuance.
- vue-svelte-patterns: one generalized skill spanning two distinct languages
  and server frameworks, creating uncertainty about which APIs to use.

Decisions: strengthen React, Next.js and TanStack Start in place. **Replace**
vue-svelte-patterns with distinct vue-application (Vue 3/Nuxt 4) and
sveltekit-application (Svelte 5/SvelteKit 2). Add angular-application and
astro-application, each with an independently identifiable execution model
and production testing responsibilities. No general frontend-safety or
performance micro-skill duplicated from Quality/Design.

Total: **7 Frontend skills, 21 targeted references, 144 catalog skills,
20 opt-in profiles**. This is one uniform quality bar, not a maturity rank.
All framework knowledge is only read on explicit activation and leaf choice.

## Verified official references and conclusions

| Framework | Official docs | Verified implementation consequence |
|---|---|---|
| React | https://react.dev/learn/you-might-not-need-an-effect | Derive state in render; Effects synchronize external systems |
| React RSC | https://react.dev/reference/rsc/server-components | RSC may execute at build; bundler framework internals are version-sensitive |
| Next.js App Router | https://nextjs.org/docs/app/getting-started/server-and-client-components | Server Components default; use client expands imported bundle boundary |
| Next.js data | https://nextjs.org/docs/app/getting-started/fetching-data | Request-scoped React cache differs from shared persisted caching |
| TanStack Start | https://tanstack.com/start/latest/docs/framework/react/guide/server-functions | Same-origin server RPC is directly callable; route beforeLoad does not authorize endpoint |
| TanStack Start security | https://tanstack.com/start/latest/docs/framework/react/guide/middleware | Custom src/start.ts must register CSRF middleware explicitly, unlike no-custom-start default |
| Vue SSR | https://vuejs.org/guide/scaling-up/ssr.html | Shared mutable SSR stores can leak between users; hydration mismatch from random/timezone/HTML |
| Nuxt 4 | https://nuxt.com/docs/4.x/getting-started/data-fetching | useFetch/useAsyncData are SSR-aware; raw fetch in setup can duplicate requests |
| Svelte 5 | https://svelte.dev/docs/svelte/%24derived and https://svelte.dev/docs/svelte/%24effect | Derived values and browser-only effects have distinct roles |
| SvelteKit | https://svelte.dev/docs/kit/load and https://svelte.dev/docs/kit/form-actions | Universal load can execute browser-side; server load/actions keep private operations server-side |
| Angular | https://angular.dev/guide/signals/effect and https://angular.dev/guide/hybrid-rendering | Use computed rather than effect for propagation; Client/Server/Prerender route modes |
| Astro | https://docs.astro.build/en/concepts/islands/ and https://docs.astro.build/en/guides/server-islands/ | HTML by default; client and server islands require explicit hydration/adapter and auth handling |
| Browser tests | https://playwright.dev/docs/intro | Actual browser SSR and navigation tests remain required |
| Component tests | https://testing-library.com/docs/react-testing-library/intro/ | Accessible user-observable queries preferred over hook internals |

Current docs are primary authority for API claims. Stack Overflow helps
with reproducible bugs but cannot overrule actual installed-version API.
SOTA means current and measurable, not universally superior framework.

## Tests and evidence

- 7 positive/8 neighboring-negative routing fixtures and no-match cases.
- Source/depth/path and progressive budget checks for all 21 leaves.
- Educational Node HTTP fixture tests direct endpoint authorization,
  tenant separation, escaping, deterministic HTML and private caching.
- Prior toolkit, PostgreSQL, FastAPI and Node tests must stay green.

Not claimed: complete pinned builds for all seven frameworks, browser E2E
hydration in every hosting adapter, real credentialed auth/CSRF provider,
measured CWV on production traffic or model selection benchmark.
These require concrete applications and authorized runtime testing.

PR remains Draft. No merge and no production deployment.
