# Technical SEO — metadata, structured data and real web performance

**Read when:** implementing route metadata, social cards, rich-result structured data or technical fixes for slow SEO landing experiences.

## Route metadata contract

Use page-specific meaningful titles and heading hierarchy that match real visible content. Descriptions can help snippets but do not guarantee what search engines display. A canonical link should identify the intended page version. SSR/SSG routes must expose the metadata in server-delivered HTML and preserve it across hydration. Social Open Graph tags serve social sharing and are not substitutes for crawl/index metadata.

## Structured data

Use an applicable schema type, with complete facts also visible on the page. Do not add fake review stars, dates, prices or organizations to pursue enhanced search snippets. A schema validator passing does not guarantee rich results.

~~~html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "An example explanation of safe object uploads",
  "author": { "@type": "Person", "name": "Example Author" },
  "datePublished": "2026-10-01"
}
</script>
~~~

This is **illustrative**. Before publishing, replace title, author, date and page type with actual verified facts and validate the current structured-data documentation relevant to that type. Schema.org syntax and search provider eligibility are separate checks.

## Core Web Vitals and underlying causes

Use field metrics such as LCP, INP and CLS where available; diagnose specific pages/devices with traces before coding. Check current official definitions/thresholds when the task is performed. Typical paths:
- LCP: correct hero asset source, image dimensions/priority, caching and avoiding blocking critical resources.
- INP: measure long tasks, framework hydration and heavy event handlers; don't optimize arbitrary handlers without trace evidence.
- CLS: reserve image/iframe space; address font swaps, inserts and hydration differences.

Audit semantic HTML, readable zoom, contrast, touch accessibility and mobile layout. A faster page that hides important content or breaks keyboard access is a regression.

## Validation loop

Record a baseline, deploy approved changes, recheck actual generated HTML, headers, schema validator results, web performance traces and relevant search console reports where access exists. Do not promise rank, rich-result inclusion or an instant crawl.

Official: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data and https://web.dev/articles/vitals and https://developers.google.com/search/docs/appearance/snippet .
