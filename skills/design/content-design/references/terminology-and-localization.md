# Consistent terminology, localization and responsive writing

Read when: maintaining product vocabulary, translation, inclusive language, right-to-left support or long-content resilience.

## Product lexicon
Build a small glossary `term -> definition -> visible label -> forbidden synonyms -> owner`. A "workspace" should not become "organization" on an error page unless they truly differ. Keep navigational nouns aligned with `information-architecture`; keep SEO language separate from in-app task clarity.

## Translation without broken UI
Do not concatenate fragments that translators must reorder. Prefer semantic ICU-style pluralization handled by the installed i18n stack, not invented per-language rules. Be aware of gender/declension, dates/timezones, number/currency separators, locales and units. Check long translations with actual components; don't fix by always truncating essential instructions.

```text
Bad: "You have " + count + " item(s) in " + folder
Better: localized complete message with a plural/select-capable formatter.
```
The example explains the contract without choosing a localization package. `frontend/<framework>` and existing i18n tools implement it; this skill owns correctness of text/meaning.

## Accessibility and tone
Visible button text should be specific; accessible name may include context but must not contradict visible label. Explain errors in words, not just color. Avoid idioms or jokes in critical financial/medical/safety workflows. Test zoom, reduced viewport, RTL direction and screen-reader pronunciation where possible.

Sources: https://www.w3.org/WAI/tutorials/forms/ and https://design-system.service.gov.uk/
