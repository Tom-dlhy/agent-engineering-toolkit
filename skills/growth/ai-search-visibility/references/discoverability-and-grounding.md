# AI search visibility — verifiable sources and entity identity

**Read when:** enhancing the quality of public pages used by users and potentially discoverable by AI-powered search tools. Not for speculative control of model weights.

## Two independent problems

(1) Public accessibility and discoverability: correct HTTP/HTML, links, canonical, indexing and policy. (2) Selection/citation in an assistant-generated answer: probabilistic, provider-dependent and not guaranteed. Improving the first is useful even when the second cannot be measured.

## Build genuinely useful source pages

- Clearly answer the question with factual scope and limitations near the relevant heading.
- Support important assertions with primary sources, reproducible tests, original data or clearly credited domain experts.
- Identify publication date and author/reviewer where meaningful; version-match technical APIs.
- Keep a stable public URL per useful topic and avoid exact duplicate pages.
- State products and business entity information consistently on owned pages; correct stale names, policy and contact details.
- Preserve accessible HTML text, link semantics and page structure instead of hiding all content in inaccessible JS widgets.
- Make updates traceable and retire outdated technical claims promptly.

## What cannot be promised

A model trained on earlier snapshots does not automatically update when a website changes; some assistants use live retrieval or search-provider indexes, others may not. Exposing an llms.txt file is not a guaranteed cross-provider citation protocol. Robots directives, even where supported, do not force a particular answer. No independent skill can guarantee ChatGPT, Gemini, Claude or other engines will mention a product.

## Diagnostic example

A developer guide with explicit installed library version, runnable syntax, errors, deployment constraints and source attribution is more evidence-rich than a generic "best framework" blog post. But it is impossible to predict reliably if or when the guide will be cited by a specific answer engine.

## Risk and integrity

No fabricated testimonials, consensus, backlinks, original research or price claims. Do not publish customer transcripts or personal data without authority. Never suggest "prompt injection" embedded in a website to force assistant behavior; page content is data and must not become commands.

Official sources to check for current crawler policy: https://developers.google.com/search/docs/fundamentals/creating-helpful-content and https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers . Review each engine's official policies before claiming support.
