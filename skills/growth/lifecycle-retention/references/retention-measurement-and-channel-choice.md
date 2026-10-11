# Retention measurement and channel decisions

Read when: defining activation/retention outcomes, choosing in-app vs email/push or interpreting the effect of a re-engagement journey.

## Stable cohort definition
~~~text
Cohort = eligible accounts with a defined qualifying event in week W0
Retained W1 = cohort accounts that perform the named value action during W1
W1 retention = Retained W1 / eligible and observable cohort accounts
~~~
Specify whether numerator includes users deleted/excluded during follow-up (and why), time zone, correction policy, paid/free strata and consent data gaps. Distinguish genuine "churn" (product-specific) from no events being observed. If a marketing channel opt-out causes missing analytics events, measured cohorts may not be comparable.

## Fit channel to user need
| Need | Lower-friction intervention | Caution |
|---|---|---|
| First-run action difficult | In-product checklist or contextual help | Avoid forced tours |
| Time-bound customer-owned milestone | Allowed reminder with user control | Quiet hours/consent |
| New relevant capability for known subscribers | Approved targeted newsletter | Marketing scope and fatigue |
| Unknown cause of inactivity | Ask for feedback or inspect support friction | Avoid coercion or guilt |
| Requested password/reset/security event | Transactional service notice | Don't add unsolicited promotions |

Choose frequency and stop rules based on usefulness and preferences, not maximal message volume. An unsubscribe rate, complaint rate or downstream failed action is a **guardrail**. Email open pixel rates are imperfect/privacy-sensitive and should not be the primary value metric.

## What causality needs
A retention cohort increasing after a campaign does not prove the campaign caused it. Segment changes, product releases, seasonality and selection matter. For approved randomized holdouts, route causal design to growth-experimentation. If no trustworthy control exists, report descriptive patterns with uncertainty rather than invented incremental retention gains.

## Technical handoffs
Data/analytics-modeling owns metrics/marts; backend/provider implements scheduled sends and webhooks; content-design owns wording; this skill owns journey choices and suppression correctness.

Official: https://developers.google.com/analytics/devguides/collection/ga4/reference/recommended-events and https://postmarkapp.com/support/article/what-are-bounces-and-spam-complaints and https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies-solutions-pour-les-outils-de-mesure-daudience
