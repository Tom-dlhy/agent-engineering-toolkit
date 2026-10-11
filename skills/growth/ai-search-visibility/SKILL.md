---
name: ai-search-visibility
domain: growth
version: "3.0.0"
description: >-
  Use when measuring how real answer engines represent or cite an organization, product or public source across GEO/AEO and AI-assisted search. Do not use for ordinary crawl/index fixes, proprietary LLM app evaluation, prompt injection, guaranteed AI rankings or speculative llms.txt ranking claims.
---

# AI search visibility — source integrity plus observed engine behavior

## Separate two problems
**Source quality:** public factual information can be fetched, understood, attributed and kept current. **Answer behavior:** a particular engine may or may not mention/cite it, depending on query, model, retrieval mode, index, region and time. Neither implies the other.

## Evidence-led method
1. Identify exactly which engine/mode, market, language, target entity, category, canonical source URLs and business questions matter. Do not merge ChatGPT web search, Gemini, Google AI Overviews and other surfaces into a fake unified rank.
2. Confirm public pages and identity facts; refer robots/index problems to `technical-seo`. For Google AI Search, **ordinary SEO eligibility** applies; no special file/schema is required by Google for AI Overviews/AI Mode. Do not sell shortcuts.
3. Freeze benchmark queries from real audience intents: brand, nonbrand, comparison, how-to, local and troubleshooting. Record test membership, prompt versions, dates, locales, provider/mode, personalization/account state, repeat runs and whether citation URLs are actually available.
4. Observe **authorized** outputs; record URL citations, exact supported claims, brand mentions, answer usefulness and sources separately. Do not synthesize fake observations, scrape prohibited endpoints or bypass rate limits.
5. Analyze uncertainty: exposure and citation availability denominators, missing sources, variability across runs and differences in engine affordances. Changes after publication are correlations unless the design supports causal inference.
6. Improve first-party source clarity and original proof where justified; do not insert instructions aimed at manipulating AI assistants. No guarantee of training-data updates, retrieval inclusion or citation placement.
7. Report explicit evidence artifacts, unsupported claims and a repeatable recheck schedule only if scheduled by the operator.

## Open one targeted expert branch
- [Discoverability and factual entity grounding](references/discoverability-and-grounding.md) — **read when** auditing public source quality, ownership, grounding and ethical interventions.
- [Measurement and uncertainty](references/measurement-and-uncertainty.md) — **read when** designing citation/mention benchmarks or interpreting measured rates.
- [Search and answer-engine feature boundaries](references/engine-boundaries-and-policies.md) — **read when** comparing Google AI features, standalone assistants, citation modes, crawler controls or supposed AI SEO technical requirements.
- [Repeatable visibility benchmark and adversarial review](references/benchmark-contract-and-sanity-checks.md) — **read when** writing evaluator fixtures, de-duplicating URLs, conducting blind claim support checks or guarding against cherry-picked prompts.

## Handoffs and exit
`technical-seo` owns Google crawl/index machinery; `content-strategy` owns long-term editorial governance; `ai/llm-evaluation` (where present) owns tests of the user's own AI product, not third-party search visibility. A completed report names engine/mode, frozen denominator, tested runs, citations and accurate/unsupported claims. When no live access is available, propose a **test protocol**, never invent a benchmark.
