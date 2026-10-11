# Lifecycle journeys, event triggers and suppression invariants

Read when: designing activation nudges, reminders, dormant-user journeys or messaging that should stop after customer action.

## Activation requires real value
Define successful meaningful product behavior and a qualifying user cohort first. "Opened a welcome email" or "clicked a campaign" are not inherently activation or retention. Decide eligibility, exclusion, journey expiration, maximum messages, timezone and explicit purpose.

### State-driven journey example
~~~text
NEW -> ACTIVATED: verified core product action
NEW -> HELP_ELIGIBLE: no activation during approved window, channel eligible
HELP_ELIGIBLE -> QUEUED: suppression and frequency checks pass
QUEUED -> CANCELLED: user activates, opts out or closes account before send
QUEUED -> PROVIDER_ACCEPTED: provider confirms submission (not delivery)
PROVIDER_ACCEPTED -> SUPPRESSED: unsubscribe, complaint or hard bounce
~~~
Run permission/suppression **again at execution time**, not just when queueing. Do not mistake scheduler success for inbox delivery or completed product activation.

## Idempotency and fault cases
Deduplicate trigger events and messages using appropriate combination of journey, recipient, trigger and version. Expiring eligibility must not be resurrected by delayed webhook retries. If a provider responds ambiguously, use a dedupe provider identifier/status reconciliation before repeating; avoid duplicate charges or spam.

### Required negative fixtures
1. User activates one minute before reminder dispatch -> reminder cancelled.
2. User opts out after entering segment -> all subsequent marketing blocked.
3. Duplicate trigger delivered twice -> at most one logical message.
4. Provider accepts send then callback delayed -> not counted as delivered.
5. Account deleted / access revoked -> no orphaned scheduled marketing send.
6. Provider permanently suppresses recipient -> no queued marketing retry.

## Ownership
Journey rules here; implementation belongs to existing backend queue, CRM/ESP and consent/preference store. Do not implement a second subscriber database or force new workflow tooling when existing provider supports triggers.

Official: https://postmarkapp.com/support/article/what-are-bounces-and-spam-complaints and https://www.cnil.fr/la-prospection-commerciale-par-courrier-electronique
