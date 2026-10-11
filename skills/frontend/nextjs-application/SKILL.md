---
name: nextjs-application
domain: frontend
version: "0.2.0"
description: >-
  Use when building or auditing Next.js App Router pages, React Server Components, server actions, route handlers, caching, streaming and deployed Next.js apps. Do not use for TanStack Start APIs or merely client-only React component state.
---

# Next.js App Router — request authority, caching and React boundaries

## Implementation procedure
1. Confirm Next.js installed major/minor, App Router vs Pages Router, rendering target (Node/edge/static), React version and deployment platform.
2. By default App Router pages/layouts are Server Components; use `'use client'` only for required interaction/browser APIs. This directive makes the imported module subtree part of the client graph.
3. Server Components can read secrets but **props and serialized responses can still leak sensitive data**. Scope access at database/service layer before rendering, not only in page navigation.
4. Mark Server Functions/Actions with `'use server'` and **reauthorize every mutation invocation**; enforce cookies/CSRF/origin assumptions, validate form data server-side and prevent uncontrolled redirects.
5. Determine explicit caching/freshness, request memoization versus cross-request cache and invalidation. Do **not** copy historical Next.js caching defaults without inspecting installed version and configured cache settings.
6. Make Suspense/loading/error/not-found boundaries intentional; avoid private data inside public/static caches; plan revalidation after mutations.
7. Run production build, per-route static/dynamic inspection, auth/CSRF negative tests, source-map/client-bundle secret audit and browser preview for real hydration.

## Targeted expertise (open only when needed)
- [RSC versus Client Components, serialization and hydration](references/next-rsc-boundaries.md) — **read when** RSC versus Client Components, serialization and hydration.
- [version-aware caching, streaming and dynamic/personalized fetching](references/next-caching-and-data.md) — **read when** version-aware caching, streaming and dynamic/personalized fetching.
- [server action authorization, form validation, cache mutation and deployment tests](references/next-actions-security-testing.md) — **read when** server action authorization, form validation, cache mutation and deployment tests.

## Boundaries and completion
Choose the one framework-specific skill matching the actual repository. Delegate visual tokens and UI library APIs to design/ui, security audit to quality, endpoint contracts to backend, and deployment infrastructure to Cloud. Do not install frameworks just to follow a skill. Complete with evidence from typecheck/build, negative authorization tests, realistic browser hydration and documented version limitations. Treat examples as illustrative until executed against pinned dependencies.
