---
name: technical-seo
domain: growth
version: "2.0.0"
description: >-
  Use when auditing or implementing search-engine crawlability, indexability, canonicals, redirects, sitemaps, metadata, schema.org markup or search-facing web performance. Do not promise rankings or use for generic editorial strategy.
---

# Technical SEO

## Engineering procedure

1. Identify the public canonical host, intended indexable URLs, private routes, locales, framework rendering mode, preview sites and existing analytics/Search Console permissions.
2. Inspect the **actual HTTP response**: status, redirects, robots directives, canonical, HTML content, links, sitemap and JS/SSR behavior. Source code alone is not proof.
3. Distinguish crawl restrictions from noindex, and indexability from ranking. A robots.txt Disallow is not access control nor a guarantee of deindexing.
4. Define unique page purposes, titles/descriptions, headings, canonical/hreflang policy and internal links; avoid keyword stuffing and duplicated near-empty routes.
5. Add only accurate structured data matching visible facts; verify eligibility in current official docs.
6. Measure Core Web Vitals with real field data if available; use lab profiles to diagnose expensive images, scripts, layout shift and hydration.
7. Test production and staging separately so staging/admin content cannot leak. External console submission or deployments require authorization.

## Reference selection

- [Crawl, index, redirects and localization](references/crawl-index-and-routing.md) — **read when** diagnosing missing pages, duplicate URLs, robots/noindex, sitemaps, redirects or multilingual canonicalization.
- [Structured data, metadata and performance](references/structured-data-and-performance.md) — **read when** implementing JSON-LD, title/social tags or web performance improvements.

## Distinct responsibility

Content-strategy chooses subjects and publishing priority. AI-search-visibility studies answer-engine citations and attribution. Both may rely on sound technical SEO, but neither is a substitute for this skill.

## Done

Report exact URLs inspected, observed vs inferred cause, actionable fix, status/header/HTML tests and any measurement still unavailable. Do not claim indexing or search rank improvements without evidence.
