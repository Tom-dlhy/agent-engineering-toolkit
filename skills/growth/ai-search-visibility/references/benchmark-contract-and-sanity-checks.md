# Reproducible visibility benchmark and anti-cherry-picking review

Read when: measuring mentions/citations against a frozen prompt set, auditing AI-search vendors or writing evaluator fixtures.

## Dataset before interventions
Construct cases from real user tasks: brand, nonbrand, comparison, local, implementation and troubleshooting where relevant. Freeze the prompt, locale, engine/mode, date range and query weight *before* evaluating changes. Don't insert brand into generic questions just to force mentions; no private customer content in prompts.

~~~yaml
version: 1
cases:
  - id: nonbrand-001
    locale: fr-FR
    intent: category-compare
    question: "Which services document this customer workflow?"
    weight: 1
    source_requirement: verifiable public content
~~~
This is synthetic **configuration**, not a benchmark result.

## Run record contract
~~~json
{
  "case_id": "nonbrand-001",
  "engine": "NOT_RUN",
  "mode": "NOT_RUN",
  "timestamp_utc": null,
  "brand_mentioned": null,
  "citations_exposed": null,
  "target_url_cited": null,
  "citation_supports_claim": "not-assessed"
}
~~~
Do not turn `null` (unknown/not observed) into `false` or zero. Store actual cited URL, exact claim, public source snapshot where licensed, reviewer and confidence. Keep citation availability denominator distinct from total queries. User location, session/login state, search index drift and engine updates affect repeatability.

## Compute only grounded metrics
Mention rate = observed brand mentions / valid observed queries, within the same configured mode. Citation rate = runs with a target-source citation / runs *where source citations were available*; always report absent interfaces. Claim support rate = verified supported claims / claims actually reviewed, with an explicit rubric. For variable outputs, report repeated run distributions and unknowns; don't pretend a one-shot screenshot represents universal ranking.

## Adversarial audit
Include ambiguous brand names, competitor/nonbrand prompts and queries that should yield *no* citation. Blind-check whether cited sources actually substantiate claims. Compare same frozen cases pre/post, label changes **observational** absent randomized causal design, and report missingness and exclusions. Reject secret "LLM rank #1" claims without complete denominator and reproducible trace.

Official: https://developers.google.com/search/docs/appearance/ai-features and https://www.nist.gov/itl/ai-risk-management-framework
