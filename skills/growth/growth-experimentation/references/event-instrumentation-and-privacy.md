# Consent-aware event instrumentation and funnel evaluation

Read when: specifying a real conversion tracking event, diagnosing duplicated analytics signals or constructing a privacy-aware acquisition funnel.

## Event schema first, tools second
Inspect installed analytics SDK/tag manager, actual backend result events, company data governance, consent and browser privacy settings. Prefer a provider-recommended event name if it really matches meaning. A client-side click is an interaction, not necessarily a persisted order, subscription or lead.

~~~yaml
event: inquiry_confirmed
producer: server after durable successful persistence
entity_key: synthetic inquiry ID, not email or form free text
dedupe_key: inquiry ID plus event kind
eligible_population: explicitly defined within consent rules
time: UTC event time plus reporting timezone policy
forbidden_fields: [email, phone, free_text, access_token]
analytics_provider: existing installed implementation
~~~
Illustrative schema; actual provider contracts, server/client transport and legal basis must be validated separately. Don't send real user identifiers or sensitive values into test fixtures.

## Funnel grain and QA
Define who enters the funnel, each event, unit (unique account, user, visit), timing and eligible denominator. Never sum repeated retries as new conversions; do not accidentally compare 100 marketing clicks to 100 server-validated inquiries from a different attribution window. Model missing events, consent opt-outs, bot exclusion, latency, anonymous-to-login identity transition and timezone changes.

### Negative scenarios
- Client hydration sends `page_view` twice and creates duplicate counts.
- A user clicks "Pay" but the gateway declines: count click, **not** purchase.
- Server retries a durable write and emits duplicate success events: dedupe by stable business identifier.
- Consent denied: required legal/privacy behavior honored; acknowledge measurement gaps rather than secretly tracking.
- Experiment variant assigned but not rendered: assigned unit is not automatically a valid exposed unit; document estimand.

## Privacy prerequisites
France's CNIL allows certain **narrowly configured** audience-measurement exemptions, not a blanket exemption for GA4, personalization or any analytics vendor. Google's Consent Mode changes tag behavior but is not itself legal consent. Inspect actual CMP, jurisdiction and processing agreements before adding trackers or recording sessions. No data uploads, cookies or service account access from a documentation task.

Official: https://developers.google.com/analytics/devguides/collection/ga4/events and https://developers.google.com/analytics/devguides/collection/ga4/reference/recommended-events and https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies-solutions-pour-les-outils-de-mesure-daudience
