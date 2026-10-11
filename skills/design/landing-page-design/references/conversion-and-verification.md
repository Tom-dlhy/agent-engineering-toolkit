# Conversion flow, forms and measurable acceptance

Read when: building lead/order CTA journeys, consented analytics, experiment plans or release criteria for marketing pages.

## Trace the real action
Start with a path from discovery -> proposition -> CTA -> input if required -> submission/result -> retry. Specify the actual conversion event before instrumenting it: button click is **not** a completed inquiry or purchase. Distinguish microconversions (open contact, download guide) and confirmed outcomes. Avoid forcing complex forms when a mail or telephone contact is the real flow.

## Accessible conversion contract
CTA is a clear link when navigating and a button when changing state. Forms need meaningful labels, correct input types/autocomplete, client-side hints and server-side validation, errors attached to fields, success feedback and keyboard use. Test double-submission, invalid input, network failure, delayed response, back navigation and small viewport keyboards. No analytics dependency should block the primary action.

## Measurement without invented lift
Capture event name, trigger condition, provenance, consent/legal basis, deduplication, environment and success definition. Run tests against a fixed mock dataset where possible; if no real analytics or representative traffic exists, say the experiment is **proposed**, not successful. A/B tests require an appropriately defined population, guardrails, stopping rule and honest uncertainty; never promise a conversion rate uplift.

## Performance and search boundaries
Real page performance, image optimization, semantic landmarks and useful content matter. `technical-seo` owns canonical/indexing/sitemap. Use `responsive-visual-qa` for rendering and `accessibility-wcag` for formal success criteria.

Official: https://www.w3.org/WAI/tutorials/forms/ and https://web.dev/articles/vitals
