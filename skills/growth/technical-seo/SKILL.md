---
name: technical-seo
domain: growth
version: "3.0.0"
description: >-
  Use when investigating or implementing crawlability, indexing, canonical URLs, redirects, sitemaps, JavaScript SEO, metadata, structured data or search-facing performance on public web routes. Do not use for editorial planning, guaranteed rankings, authentication of private pages or AI-answer citation benchmarking.
---

# Technical SEO — observable HTTP before speculation

## Inspection to implementation
1. Inventory public origin(s), environments, target markets/languages, route generation (SSR/SSG/CSR), auth boundaries, canonical host, expected public indexable URLs and known nonindexable routes. Preserve user-set stack. Do not auto-deploy or submit URLs.
2. Test the **actual response** (when reachable), not only React/browser DOM: chain/status, Content-Type, robots.txt, X-Robots-Tag, meta robots, canonical, alternate hreflang, visible HTML content and navigable anchors. Read-only example: `curl -sSIL https://example.org/path` (HEAD may behave differently from GET); follow with GET/HTML inspection.
3. Separate **crawl allowed**, **fetchable**, **indexable**, **selected canonical** and **ranked** as independent facts. `Disallow` is neither private-route protection nor a guaranteed deindex. A declared canonical is a signal, not proof of Google's selection.
4. Trace real route variants: case/trailing slash, parameter facets, filtered/paginated views, 3xx chains, soft 404s, expired inventory, locales, JS content and prerender/SSR hydration. Avoid contradictory canonical, sitemap and hreflang declarations.
5. Keep titles/descriptions, structured data and social metadata truthful and relevant. Google rich-result eligibility is not guaranteed by valid JSON-LD; test the relevant current feature documentation and rendered page facts.
6. For performance, collect field Core Web Vitals (LCP/INP/CLS) if available; lab traces are diagnostic, not representative ranking/traffic proof. Coordinate framework fixes with the frontend skill and measured bottlenecks with quality/performance-profiling.
7. Produce a reproducible URL-level defect ledger with **observed evidence vs untested hypotheses**, safe change plan, redirects/regression coverage and allowed environments. Deployment/Search Console changes require authorization.

## Open only the relevant technical reference
- [Crawl, index, redirects and localization](references/crawl-index-and-routing.md) — **read when** differentiating indexability/canonical failures, route migrations, robots and multilingual URLs.
- [Structured data, metadata and performance](references/structured-data-and-performance.md) — **read when** implementing metadata, JSON-LD and measured Core Web Vitals fixes.
- [JavaScript rendering and search route migration](references/javascript-rendering-and-migrations.md) — **read when** diagnosing blank client shells, SSR/hydration, bot rendering gaps or route/locale migration.
- [Search Console investigation and URL test contracts](references/search-console-and-url-contracts.md) — **read when** establishing a measurable baseline, diagnosing indexed-vs-submitted mismatches or building route-level regression tests.

## Ownership and release
`content-strategy` owns what to publish; `ai-search-visibility` owns **external answer-engine observation**, never special Google AI ranking tricks; `frontend/<framework>` owns rendering APIs; `quality/performance-profiling` owns performance instrumentation. Do not read credentials, bypass robots/security controls or bulk crawl public services without permission. Deliver HTTP/HTML/header evidence, precise routes, limited verified fixes, browser/build tests actually run and an explicit list of unverified index/search outcomes.
