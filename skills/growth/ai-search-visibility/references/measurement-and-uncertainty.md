# AI search visibility — evidence, repeatability and honest metrics

**Read when:** designing a benchmark of AI search mentions/citations, comparing content changes or evaluating "AI SEO ranking" claims.

## Freeze evaluation scenarios first

Select actual target answer engines and modes that you are permitted to test. Define queries from authentic customer intent across: branded, nonbranded category, geographic, how-to, troubleshooting and comparison. Record exact text, language, locale, test date, account/device/mode and whether visible citations are available. Use the same prompt set before and after an intervention.

### Recording schema (illustrative only)

~~~json
{
  "query_id": "comparison-001",
  "engine": "example-answer-engine",
  "locale": "fr-FR",
  "query": "Which service supports this workflow?",
  "timestamp": "2026-10-11",
  "cited_urls": [],
  "brand_mentioned": false,
  "claim_correct": "not-assessed",
  "citation_supports_claim": "not-assessed",
  "notes": "EXAMPLE, NOT A REAL OBSERVATION"
}
~~~

## Metrics and denominators

- Mention rate = tested queries mentioning the brand / all applicable frozen queries.
- Citation rate = tested queries with a target URL cited / queries on which the engine exposed source citations. Report how often citations were unavailable.
- Citation support = target references that actually substantiate the accompanying claim / audited target references.
- Factual fidelity = human-graded accuracy relative to verified source facts, with a visible rubric.
- Variability = distribution across repeat runs, sessions and days; a one-shot screenshot has low evidentiary strength.

Do not fabricate exact traffic or rank. Answer engines change models, retrieval sources and UI. Search personalization, location, login state and prompt phrasing affect observations. Be explicit about partial comparability.

## Intervention experiment

1. Collect a baseline from the same frozen scenario set; record errors and absent citation modes.
2. Ship **one** factual/source clarity improvement, with release timestamp; do not claim instant index adoption.
3. Wait an observation window based on practical use, not an invented crawler SLA.
4. Rerun scenarios and compare output changes, quality and citation evidence.
5. If differences are unstable, report uncertainty or inconclusive findings, not a causal SEO success story.

## Claim review

Reject guaranteed placement/citation services, undefined "rank #1 in ChatGPT" offers, invented LLM score tools and scraping methods that violate access terms. Demand the engine/mode/query list, baseline, date, source logs and clear denominators.

Context: https://www.nist.gov/itl/ai-risk-management-framework and https://developers.google.com/search/docs/fundamentals/creating-helpful-content .
