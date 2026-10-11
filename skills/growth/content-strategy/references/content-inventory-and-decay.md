# Content inventory, consolidation and decay review

Read when: existing pages duplicate user intent, conflict with the current product or become stale and expensive to maintain.

## Inventory schema
For each owned URL record its real user question, audience, product/source owner, status, updated/reviewed date, canonical identity, incoming/internal links, evidence freshness, current traffic if authorized, duplicate intent candidates and language coverage.

Do not manufacture search volumes, lead attribution or user interviews when tools aren't connected. Duplicate **wording** is not necessarily duplicate **intent**, while different keywords can conceal pages competing for the same task.

## Page-level decision matrix
- KEEP: accurate, distinct user task, evidence current, responsible owner.
- UPDATE: useful core intent but outdated API, pricing, regulation or steps; preserve working bookmarks and source attribution.
- CONSOLIDATE: redundant pages serving materially the same intent; choose the reader-helpful canonical and coordinate redirects with technical-seo after approval.
- RETIRE: obsolete content with a reviewed replacement, archival or legitimate gone status; do not delete an existing published page solely for low traffic.
- CREATE: verified unmet need where team has original evidence and maintenance capacity.

### Example (illustrative)
~~~yaml
url: /guides/file-upload
question: How to securely upload a document?
evidence: current support questions plus outdated SDK example
decision: UPDATE
action: verify version; add constraints and error recovery
owner: designated technical reviewer
refresh_trigger: next SDK major version or auth changes
risk: translated pages and external backlinks
~~~
Never present a fictitious example as an actual inventory result.

## Reliable maintenance
Source links/version labels on product claims; a named review owner; review trigger for pricing/security/legal changes; high-risk articles refreshed earlier than evergreen content; process for retracting errors without erasing attribution or user bookmarks. Avoid mass-generated topic farms.

## Outcome measurement
Use observed task usefulness, outdated-page incidence, successful search/help resolution, source corrections and maintenance cost. Traffic alone is insufficient; search impression fluctuations cannot prove content change caused growth.

Official: https://developers.google.com/search/docs/fundamentals/creating-helpful-content and https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
