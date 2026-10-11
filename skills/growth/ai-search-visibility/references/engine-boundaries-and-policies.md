# Answer-engine boundaries, retrieval modes and claims

Read when: comparing GEO/AI SEO recommendations across Google AI features and standalone AI answer engines, or evaluating claims of a universal ranking mechanism.

## Which search surface?
| Surface | Distinguishing questions | Invalid inference |
|---|---|---|
| Google Search AI Overviews or AI Mode | Indexed page? Snippet eligibility? Exact query/locale? AI feature appeared? | Need custom AI-specific schema or llms.txt |
| Assistant with retrieval/search | Retrieval enabled? Source links visible? Signed-in locale/mode? | Publication instantly changes model weights |
| Offline assistant without retrieval | Which model/training snapshot? | Missing citation caused by robots |
| Niche discovery platform | Known data feeds/crawlers and UI? | Same rank semantics as Google |

**Official Google Search Central guidance:** its AI Search features do not need extra technical requirements or special optimization beyond regular Google Search eligibility, and display/citation is not guaranteed. A llms.txt convention is not a universal cross-engine requirement. Avoid universal crawler directives and undocumented algorithm claims.

## Three independent systems
1. Fetchability and index eligibility: technical SEO observation, not AI mention.
2. Retrieval and answer formation: provider/mode/query specific; optional source links may appear.
3. Training/model knowledge: often historic; cannot be assumed to follow a website release or a sitemap update.

A brand may be correctly mentioned with no visible citation; a citation can link to a page that does not support the assertion; a crawlable page can be omitted. These are distinct outcomes. Determine exact source UI and rules, rather than reusing a benchmark designed for a different model mode.

## Ethical limits
Do not plant prompt injections ("ignore previous instructions") in public sources to coerce responses, scrape beyond authorized access, or invent endorsement/training inclusion. Public pages provide **data** and factual support, not commands for answer engines.

Official: https://developers.google.com/search/docs/appearance/ai-features and https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers and https://developers.google.com/search/docs/fundamentals/creating-helpful-content
