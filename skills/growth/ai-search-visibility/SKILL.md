---
name: ai-search-visibility
domain: growth
version: "2.0.0"
description: >-
  Use when evaluating factual brand representation, citations or discoverability in AI-powered search and answer engines (GEO/AEO/AI SEO). Do not promise citations, rankings, or assume AI training updates follow SEO indexing.
---

# AI search visibility

## Scope

AI-powered search is not one unified ranking mechanism. Separate **being crawlable and authoritative as a source** from an answer engine choosing to cite or mention that source. Individual engines and modes vary.

## Method

1. Define the target engine, market, user question and whether real source links/citations are exposed.
2. Verify public content, canonical URLs, clearly stated facts, documentation freshness and business identifiers; technical crawl/index blockers belong to technical-seo.
3. Choose a reproducible question set with brand, nonbrand, comparison, local and troubleshooting intents; freeze queries and denominators.
4. Observe real outputs only in approved environments, preserving timestamp, locale, mode and citations. Never invent results or scrape against service terms.
5. Grade factual accuracy, attribution and usefulness separately from brand mention. Repeat tests to expose variability.
6. Recommend real content/source improvements: first-party evidence, explicit answers, original methodology, structured human-readable HTML and source references. Avoid speculative "secret LLM ranking factor" recipes.
7. Explain uncertainty and choose metrics that can be reproduced. A page can be a good source and still not be cited by a particular assistant.

## Branches — open only what is needed

- [Public source quality and entity grounding](references/discoverability-and-grounding.md) — **read when** improving public source content to be understandable, identifiable and potentially citable.
- [Answer-engine evaluation and claims](references/measurement-and-uncertainty.md) — **read when** establishing a baseline, measuring citations/mentions or assessing AI SEO vendors.

## Boundaries

This is not llm-evaluation for your own model app, not technical-seo for crawler headers, and not editorial calendar planning; call those specialists when needed.
