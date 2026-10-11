# Growth — governance decision audit and operational refactor

**Review:** 2026-10-11, on main following Design PR #22 and #23. **Policy:** Agent Engineering Toolkit charter v2. **Scope:** Growth category, not data engineering or platform marketing vendor APIs.

## Reuse/extension/creation matrix

| Candidate | Decision | Unique responsibility | Existing overlap and handoff |
|---|---|---|---|
| `technical-seo` | **EXTEND** | HTTP/HTML crawl/index/SSR canonical/schema/redirect regression evidence | Frontend owns framework render APIs; Quality owns performance engineering; AI search visibility does not rewrite Google SEO |
| `content-strategy` | **EXTEND** | Evidence-led editorial content inventory, creation/refresh, topic and distribution governance | `design/content-design` owns UI microcopy; `landing-page-design` owns actual CTA/landing composition |
| `ai-search-visibility` | **EXTEND** | External answer-engine citations/mentions and reproducible factual support grading | `technical-seo` owns crawl/index; `ai/llm-evaluation` covers own LLM products; no universal AI-search ranking tricks |
| `growth-experimentation` | **CREATE** | Causal experiment design, bucketing/exposure, SRM, primary and guardrail metrics, preregistration and decision | `landing-page-design` designs page; `data/analytics-modeling` defines metric/grain; installed analytics/flag provider owns real APIs |
| `lifecycle-retention` | **CREATE** | Permissioned activation/re-engagement journeys, opt-out/suppression and retention measurement | `content-strategy` owns editorial calendar; backend/ESP owns sending; `growth-experimentation` owns randomized impact |

**Result:** 3 extended, 2 created, zero deletion/import, **5 Growth skills**, **18 targeted references** (the original six preserved plus twelve new).

## Rejected or deferred alternatives

| Idea | Decision | Why |
|---|---|---|
| `conversion-rate-optimization` (separate skill) | **REFERENCE** | Landing UX from `design/landing-page-design`, hypothesis/testing from `growth-experimentation`. Separate CRO skill would own no new independently routable task. |
| `growth-analytics` | **REFERENCE** | Event/funnel/consent design is in `growth-experimentation`; trusted data warehouse/metric ownership remains `data/analytics-modeling`. Evaluate future need for an independent attribution specialist using real held-out tasks. |
| `email-marketing` | **REFERENCE** | Opt-in, marketing streams and messaging lifecycle are a subset of `lifecycle-retention`; don't fragment by channel. |
| `programmatic-seo` | **REFERENCE / defer autonomous skill** | Page-template crawl/duplicate/quality risk belongs to technical SEO plus truthful content strategy; no permission to mass-generate location/keyword pages. |
| `local-seo` | **DEFER** | Entity listings/reputation may become a distinct operational vertical after separate evidence/trigger review; not justified from current repo tasks. |
| `paid-acquisition` / `social-media-growth` | **DEFER** | Platform-specific ad bidding/policy/compliance and social channel operations need different primary research and execution harness; avoid unverified vendor recipes now. |

## Sources and verified constraints (consulted 2026-10-11)

**Search:** Google canonical declarations are signals, not guarantees; dynamic rendering is not its favored solution; structured data must reflect visible facts and doesn't guarantee rich results.
- https://developers.google.com/search/docs/crawling-indexing/canonicalization
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering
- https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data

**AI answers:** Google explicitly states ordinary Search eligibility and no required special AI optimization for AI Overviews/AI Mode; display/citations are not guaranteed. The `ai-search-visibility` benchmark therefore measures third-party observations, not "guaranteed GEO rank."
- https://developers.google.com/search/docs/appearance/ai-features

**Measurement and experiments:** GA4 recommends known event names and DebugView/Realtime validation but does not prove real business outcomes. Sequential-valid approaches are needed for planned repeated looks at frequentist evidence; naïve early peeking inflates false positives.
- https://developers.google.com/analytics/devguides/collection/ga4/events
- https://developers.google.com/analytics/devguides/collection/ga4/reference/recommended-events
- https://docs.statsig.com/experiments/advanced-setup/sequential-testing

**Privacy/lifecycle:** CNIL analytics-exemption conditions are narrow, marketing consent varies by audience/jurisdiction, and UK ICO updated email-marketing guidance in 2026. ESP suppression and unsubscribe handling are security/legal gates, not growth conversion hacks.
- https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies-solutions-pour-les-outils-de-mesure-daudience
- https://www.cnil.fr/la-prospection-commerciale-par-courrier-electronique
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-direct-marketing-using-electronic-mail/
- https://postmarkapp.com/support/article/what-are-bounces-and-spam-complaints

All content is original technical synthesis, not a vendored provider skill. Product/region/version-sensitive guidance must be rechecked before real execution. No tools, mailing lists, trackers, or services were imported or installed.

## Routing ownership map

| User request | Activate | Explicitly avoid |
|---|---|---|
| "Why does Google index the wrong canonical?" | `technical-seo` | AEO/LLM benchmarking |
| "What support questions should become articles?" | `content-strategy` | Automated blog publishing |
| "Measure brand citation accuracy in AI Mode" | `ai-search-visibility` | Promised ranking optimization |
| "Run randomized signup variant with primary/guardrail metric" | `growth-experimentation` | New A/B vendor by default |
| "Send an approved reminder only to eligible opted-in users" | `lifecycle-retention` | CRM replacement or unsolicited outreach |
| "Implement GA4 `sign_up` provider transport in this app" | existing frontend/provider docs | Abstract design replacing API docs |
| "Fix SQL grain for signup analytics mart" | `data/analytics-modeling` | Growth formulas invented ad hoc |
| "Polish a landing page headline/layout" | `design/landing-page-design` or `design/content-design` | Randomized experiment without request |

## Risks, validation and evidence boundaries

- All skill descriptions include positive and negative triggers; references are only read after activation. New Growth skills are installed **only in the `growth-marketing` profile** or explicitly requested; no new generic UI/cloud profile bloat.
- Local `tests/test_growth_expertise.py` checks catalog/routing/reference and negative cases, source guardrails and profile context, but this is static proof only.
- `examples/growth-contracts/` contains isolated stdlib-only, non-network deterministic examples of assignment/suppression checks; tests exercise those contracts. They do **not** certify a statistical platform, actual consent compliance or exactly-once email delivery.
- `evals/growth-routing.yaml` contains held-out scenarios for future **real-agent** replay, not completed agent evaluations.
- No claim of live Search Console indexing, real Google AI citations, growth uplift or delivered marketing messages.
- CI includes catalog/path validation, unit tests, offline examples, context budgets and existing backend tests. No deployment, external publishing, tracking or CRM send is authorized.

Next: Stacks refactor, then held-out baseline-vs-toolkit evaluations and real authorized browser/crawler/provider integration checks.
