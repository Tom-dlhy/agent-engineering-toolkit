# Search, filtering and facet design

Read when: introducing or improving content discovery using search, category filters, facets or query states.

## Contract
Define searchable entities, text fields, exact match/fuzzy semantics if supported by actual search backend, category facets, sorting, typo handling, visibility/permissions and zero-results recovery. Filters should have visible names, selected state, clear/reset affordance and stable URL state if navigation/back/forward must reproduce results.

Example synthetic search specification:
```yaml
objects: public help articles
query: words typed by user
facets: category, language
sort: relevance (default), updated_date
zero_results: remove filters + spelling suggestion if supported
permissions: only authorized/public results
url_state: query + selected filters
```
This is not a contract for a specific search engine. Do not promise instant fuzzy relevance or implement new Elasticsearch/Postgres extensions without evaluating backend ownership and cost.

## Usability and accessibility
Provide labels for search and filters, result count changes announced without excessive live-region spam, keyboard-usable comboboxes where appropriate, stateful clear/reset. Distinguish no matching results from loading, service error or authorization restrictions. Do not leak restricted object labels through autocomplete or counts.

## Delegation
`backend` or `data` owns query implementation, relevance algorithm and tenant filtering. `ui/<provider>` owns Combobox, Select, Search and pagination APIs. `growth/technical-seo` owns crawlers, not internal app search.

Reference: https://design-system.service.gov.uk/components/ and https://www.w3.org/WAI/tutorials/forms/
