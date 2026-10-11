# Search Console investigation and URL-level regression contracts

Read when: diagnosing index/coverage issues, monitoring migrations or proving which HTTP/HTML properties actually exist in production.

## Source observability
| Source | Signal | Cannot infer |
|---|---|---|
| GET response | status, redirects, robots header, HTML | actual index inclusion |
| HTML tags | declared canonical/hreflang/meta robots | Google-selected canonical |
| XML sitemap | intended discovery targets | successful crawl or ranking |
| URL Inspection | Google-observed state (when accessible) | instant fresh recrawl |
| Search Console performance | aggregated clicks/impressions by dimension | sales, conversions or causal improvement |

Search Console reports may lag; not all query/page combinations are surfaced. Missing data is not automatically zero. Don't join GSC clicks and GA4 sessions without a documented unit and attribution scope.

## Representative route assertion fixture
~~~yaml
id: product_fr
path: /fr/produit/exemple
expected_status: 200
index_policy: public-indexable
canonical: https://example.org/fr/produit/exemple
hreflang:
  fr: https://example.org/fr/produit/exemple
  en: https://example.org/en/product/example
server_visible_content: true
~~~
The example is synthetic, not a claim about a real site. In tests use a proper HTTP client and HTML parser; assert status, canonical, index policy and route variations. Include negative paths: 404 must not be soft 200, /admin stays authenticated, preview is not accidentally indexed, redirected route resolves directly, hreflang and canonical remain internally consistent.

## Incident response
Record property/locale, deployed revision and date, representative URLs, actual GET headers/body, bot restrictions, canonical and sitemap. Consult Search Console/URL Inspection only if authorized. Fix one root cause, retest routes and monitor over realistic windows; do not promise immediate Google index/ranking updates.

## Safety
Avoid scraping Search Console or bulk crawling outside authorization; no automatic sitemap submission, domain config update or indexing API call. Clearly separate observed request-level faults from Search Console signals and hypotheses.

Official: https://developers.google.com/search/docs/monitor-debug/search-console-start and https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
