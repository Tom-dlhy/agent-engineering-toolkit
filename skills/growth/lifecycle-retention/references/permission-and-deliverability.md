# Permission, opt-outs, suppressions and deliverability

Read when: determining whether marketing messages are allowed, implementing unsubscribe preferences or diagnosing hard bounces/spam complaints.

## Classify the actual message, recipient and jurisdiction
Transactional/service notifications and direct marketing often have **different rules**, and a service message with added promotional content can become direct marketing. Local GDPR/ePrivacy/PECR rules may differ by country, individual vs business relationship, existing-customer exceptions and channel. Do not infer opt-in from account creation or silently reuse a contact list for new purposes.

France: CNIL generally requires prior consent for B2C email marketing; B2B scenarios can allow opt-out under conditions. UK ICO updated 2026 guidance details electronic-mail marketing and specific soft opt-in exceptions. These are **jurisdiction-specific**; involve a legal/privacy owner before real campaigns. Consent/privacy scopes are not interchangeable with technical email authentication.

## Permission/suppression record
Store source, timestamp, purpose, recipient category, channel, applicable notice/version, withdrawal history, and provider suppression ID. Global unsubscribe/complaints take precedence over campaign membership. Never overwrite a current opt-out by importing stale marketing data. Consent withdrawal must be actionable and effective before next send.

## Provider guardrails
Verify sender-domain SPF/DKIM/DMARC setup in current ESP docs and provider quotas. Respect permanent hard bounce, spam complaint and explicit unsubscribe suppressions. Keep transactional and marketing streams separated where supported; do not smuggle marketing into a transactional stream to bypass suppression. Secure webhooks before changing recipient preference or status; avoid secrets and personal data in logs.

### Negative checks
Unsubscribed recipient qualifies for campaign but is blocked; duplicate webhook stays idempotent; revoked consent halts queued send; expired opt-in isn't trusted; mailbox hard bounce leads to suppression policy; bounced message is not counted as customer engagement. A provider's HTTP success is not proof of inbox placement.

Do not send real emails, test spam, scrape contacts or upload subscriber lists absent explicit authorization. Check terms/law and staging sandbox provider features first.

Sources: https://www.cnil.fr/la-prospection-commerciale-par-courrier-electronique and https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-direct-marketing-using-electronic-mail/ and https://postmarkapp.com/support/article/1217-why-broadcasts-require-an-unsubscribe-link
