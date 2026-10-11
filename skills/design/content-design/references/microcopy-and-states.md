# Product microcopy: label, instruction and result state

Read when: writing CTA labels, form help/error text, confirmation messages or empty/loading/retry interface states.

## One verb, one outcome
Text should tell users what they can do and what will happen; avoid generic "Submit", "Oops", "Something went wrong" when context allows specificity. Use nouns users recognize, not internal API terms. Error copy pairs what happened with a safe next step. For irreversible actions explain consequences without alarming users needlessly.

| UI state | Weak | Better grounded approach |
|---|---|---|
| Empty search | "No data" | "No matching results. Clear filters or try a different term." |
| Invalid phone | "Wrong" | "Enter a phone number including the country code." (only if truly required) |
| Loading | "Please wait" | "Saving draft…" if saving is genuinely in progress |
| Server failure | "Error 500" | "We couldn't save your changes. Try again." if safe retry exists |
| Success | "Done!" | "Draft saved." only after confirmed persistence |

Examples are conditional patterns; don't claim action completion before server acknowledgement and don't use "retry" when repeating can double-charge or duplicate a side effect.

## Comprehensive state table
For a field/action specify: idle label, hint, error (specific), disabled reason if important, loading, result success, result failure, retry/recovery and screen-reader announcement when needed. Avoid duplicate labels in tooltip and visible text. Replace placeholder-only labels with persistent labels; legal disclosures require domain review.

Sources: https://design-system.service.gov.uk/components/error-message/ and https://www.w3.org/WAI/tutorials/forms/
