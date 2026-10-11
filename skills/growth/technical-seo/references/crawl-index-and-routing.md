# Technical SEO — crawling, indexing and URL identity

**Read when:** a site is missing from search results, robots/canonical behavior is unclear, duplicate pages appear or routing changes create unexpected redirects.

## Diagnostic ladder

1. Query a representative **deployed** public URL. Check HTTP status and final redirect, plus location, content-type, X-Robots-Tag, alternate/canonical links. Confirm HTML content is available to intended crawlers.
2. Read robots.txt for the specific crawler/path. A crawler disallowed from fetching a page may not see its noindex meta tag. Do not use Disallow as an access control or expect it to delete already indexed URLs.
3. Inspect meta robots/X-Robots-Tag: where appropriate noindex needs to be crawl-visible. For actual removal use the search engine's documented removal process and source status policy.
4. Verify canonical link is consistent with redirects, internal links and sitemaps. Canonical is a strong hint, not an immutable mandate on all search engines.
5. Verify sitemap lists intended absolute, indexable canonical URLs only and has correct XML/lastmod claims. Sitemap is discovery assistance, not a ranking directive.
6. Check server-rendered visible content and semantic HTML links, not only client-side route state. JS-only shells can be fragile for some crawlers.
7. For locale variants, define canonical per language and valid hreflang return-link pairs; don't canonicalize translations to one language by default.

## Example: robots.txt

~~~text
User-agent: *
Disallow: /admin/
Sitemap: https://example.org/sitemap.xml
~~~

This only tells compliant crawlers which paths not to fetch. Admin access still needs authentication; private information must never rely on robots or noindex.

## Common failure paths

- 200 OK with "Page not found" content (soft 404) instead of a real 404 or 410 when appropriate.
- Staging subdomain accidentally indexed; protect preview by authentication and proper indexing controls, do not rely solely on a sitemap omission.
- Infinite or multiple hops http→https→www→path canonical chain.
- Product faceted URLs generating many near-duplicate low-value pages.
- Server and browser disagree on canonical/title because of hydration.
- Migrated URLs not redirected, destroying useful user bookmarks and referring links.
- Pagination state breaks discoverability or accessible navigation.

## Verification

Use read-only HTTP checks and inspect built response HTML. Write a route fixture asserting status, canonical URL and index policy; test old links and locale variants. If live crawl/search console access is missing, clearly label live index status unknown rather than pretending technical checks prove indexing.

Official: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls and https://developers.google.com/search/docs/crawling-indexing/robots/intro and https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview .
