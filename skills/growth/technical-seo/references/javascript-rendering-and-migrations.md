# JavaScript SEO, rendered content and route migration

Read when: a public web route shows a client shell, metadata differs after hydration, or an SSR/static migration changes live URLs.

## Different evidence layers
An HTTP GET response, a JavaScript-rendered DOM, and a search crawler's **selected** canonical are not interchangeable. Browsers loading the page successfully do not prove crawlability by every robot.

### Safe read-only inspection
~~~bash
curl -sS -L -D /tmp/seo-headers.txt -o /tmp/seo-body.html https://example.org/products
grep -Ei '^(HTTP/|location:|x-robots-tag:|content-type:)' /tmp/seo-headers.txt
grep -Ei '<title|rel="canonical"|name="robots"|<h1' /tmp/seo-body.html
~~~
Run only against authorized real URLs. Grep illustrates triage, **not** a robust HTML parser; quotes/attribute order vary. A HEAD response may differ from GET. Verify source and rendered representations separately.

## SSR/SSG and route decisions
1. Inspect actual project framework, routes and deployment adapter. Public SEO content often suits SSG/SSR, but personalized UI needs careful server-data boundaries.
2. Ensure critical public text, link destinations, canonical, title, lang and markup are in server-delivered HTML when applicable.
3. Protect private data with authentication/authorization, not noindex or bot-specific shells; never serialize session secrets to public SSR HTML.
4. Do not default to **dynamic rendering** as an SEO workaround. Google now recommends server-side rendering, static rendering or hydration instead of separate bot-only views.
5. Diagnose content hidden behind login, blocked resources, asynchronous client fetches, missing links and server/client metadata disagreement; do not assume JS causes every indexing issue.

## Route migration contract
~~~text
old URL             -> new URL                  -> outcome
/fr/ancien-produit  -> /fr/produit              -> authorized permanent redirect
/fr/page-retiree    -> explicitly agreed policy -> correct 404/410 or destination
/admin              -> remains authenticated    -> NOT just robots.txt
~~~
Check redirect loops/hops, case/trailing slash variants, hreflang reciprocity, canonical consistency, sitemap and internal links. URL changes are potentially irreversible SEO/product changes; get deployment approval first.

## Negative fixtures
200 status with a missing-page body = soft 404 risk; canonical points to a page with no corresponding content; locale URL canonicalized to another language without justification; preview hostname exposed; only client-injected metadata appears after hydration. A source-only failure is a **risk**, not automatically observed search deindexing.

Primary: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics and https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering and https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
