---
name: astro-application
domain: frontend
version: "0.2.0"
description: >-
  Use when building Astro content-oriented sites with islands, client directives, server islands, content collections, SSR endpoints and adapter deployment. Do not use when a full interactive React/Next/TanStack app is the actual requirement.
---

# Astro — ship HTML by default and hydrate only required islands

## Implementation procedure
1. Inspect Astro major, site rendering mode, adapter, asset pipeline, content source and which sections genuinely require client interactivity.
2. Default Astro components render HTML with no client runtime JS; hydrate interactive components with deliberate `client:load`, `client:idle`, `client:visible` or `client:only` and benchmark hydration budget.
3. `server:defer` server islands enable independently fetched/personalized fragments behind a fallback; verify adapter support and security/caching of personalized responses.
4. Use content collections with schema validation and stable slugs for content sites; build API endpoints/server functionality only where deployment adapter and runtime support them.
5. Keep secrets and privileged operations in server endpoints or action handlers with reauthorization; public static HTML and build output must never contain secrets.
6. Ensure proper headers for static/SSR/CDN layers and avoid accidentally caching personalized HTML publicly.
7. Test built HTML with JS disabled, islands hydration/browser/network failure, dynamic/server island privacy, images/CLS, semantic accessibility and adapter preview.

## Targeted expertise (open only when needed)
- [client hydration directives, choosing islands and JS budgets](references/astro-islands-and-interactivity.md) — **read when** client hydration directives, choosing islands and JS budgets.
- [content collections, server islands, endpoints and security](references/astro-content-and-server.md) — **read when** content collections, server islands, endpoints and security.
- [SSR/static adapters, Web Vitals, browser tests and SEO correctness](references/astro-performance-deployment.md) — **read when** SSR/static adapters, Web Vitals, browser tests and SEO correctness.

## Boundaries and completion
Choose the one framework-specific skill matching the actual repository. Delegate visual tokens and UI library APIs to design/ui, security audit to quality, endpoint contracts to backend, and deployment infrastructure to Cloud. Do not install frameworks just to follow a skill. Complete with evidence from typecheck/build, negative authorization tests, realistic browser hydration and documented version limitations. Treat examples as illustrative until executed against pinned dependencies.
