---
name: lifecycle-retention
domain: growth
version: "1.0.0"
description: >-
  Use when designing permissioned activation, onboarding, retention, re-engagement or churn-prevention messaging journeys across email, in-app and push channels. Do not use for one-off transactional email APIs, unsolicited bulk outreach, general editorial calendars or unauthorized contact list enrichment.
---

# Lifecycle retention — helpful journey, explicit permissions

## Qualification
1. Define lifecycle state and actual customer value: activation (first successful outcome), usage habit, renewal, re-engagement or cancellation recovery. Do not assume more messages equal retention.
2. Inspect the current CRM/ESP, preference center, consent records, unsubscribe/suppression source, transactional/marketing streams, event taxonomy and regional legal constraints. Reuse current provider contracts; **never** introduce parallel subscriber truth.
3. Separate **service/transactional** communications from **promotional** intent by actual content and context. Mixed marketing content may change legal treatment. Check lawful basis and channel rules per audience/jurisdiction; don't infer universal consent from account creation.
4. Build a trigger/state contract: who is eligible, qualifying event, delay, timezone, suppression, frequency cap, expiration, deduplication key, channel fallback, cancel conditions and what happens after success or account deletion.
5. Design the least intrusive useful intervention: first-run in-app guidance, contextual help, optional reminders, preference-based communication and a clear stop path. Segment by verified behavior with privacy minimization rather than opaque profiling.
6. Protect delivery: explicit opt-outs, complaints, bounces, blocked recipient status, provider callback verification, retries/idempotency and rollback. Respect provider anti-abuse/rate limit requirements; no autonomous outbound send from a planning request.
7. Measure **meaningful retained behavior** on a declared cohort/time window, not email opens alone. Account for deliverability, attribution, confounding and delayed effects; test messaging impact using `growth-experimentation` only where lawful and statistically credible.

## Targeted branches
- [Trigger journeys, retention cohorts and idempotency](references/lifecycle-state-and-journey-contracts.md) — **read when** configuring onboarding, dormant-user journeys or stopping/resuming scheduled messages.
- [Consent, opt-out, suppression and deliverability](references/permission-and-deliverability.md) — **read when** handling email/push preferences, legal basis, SMTP/provider suppression or abuse controls.
- [Measurement, channel fit and ethical review](references/retention-measurement-and-channel-choice.md) — **read when** defining activation/retention metrics, choosing in-app/email/push and evaluating incremental impact.

## Boundaries and done
`content-strategy` owns editorial plans; `design/content-design` owns UI microcopy; `backend` owns queue/API/worker delivery; the installed ESP owns provider integration; `growth-experimentation` owns randomized impact evaluation. Review consent and send authorization in actual jurisdiction; this skill is **not legal advice**. Deliver a journey map, eligibility/suppression rules, test fixtures and approval/rollback requirements; never claim emails were sent unless the provider confirms.
