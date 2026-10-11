---
name: content-design
domain: design
version: "1.0.0"
description: >-
  Use when designing or auditing product microcopy, labels, instructions, form help, empty states, confirmation/error text and consistent UI terminology. Do not use for SEO editorial strategy, long-form marketing campaigns or generic proofreading detached from user actions.
---

# Product content design — language as interface behavior

## Decide from the task
1. Inspect existing product terminology, audience, locale, brand voice, accessibility patterns and genuine UI action/outcome. Preserve approved wording unless a real defect exists.
2. Specify what a user must understand **before** acting, what changed **after**, and what they can do next. Avoid adjectives that add no information and accidental promises.
3. Establish a small terminology glossary for domain entities, navigation verbs, input labels and statuses; use one label for one concept consistently.
4. Write states together: idle/hint, required/invalid, loading, success, empty, permission denied, timeout and retry. Make errors specific, actionable and non-blaming without exposing sensitive internals.
5. Coordinate exact labels with form semantics, localization/RTL constraints, pluralization and variable substitution. Text is not decorative; preserve meaningful accessible names and structured error announcements.
6. Reuse the existing provider's labels, field descriptions and feedback components. No duplicate stateful components or unrequested global rebrand.
7. Validate comprehension in real interface width and actual states. Keep copy variants reviewed by product/subject expert when legal, financial or regulated claims are present.

## Deep branches
- [Microcopy and actionable state contracts](references/microcopy-and-states.md) — **read when** writing labels, helper text, empty states, errors or confirmations.
- [Terminology, localization and responsive content](references/terminology-and-localization.md) — **read when** standardizing product nouns/actions, translations, placeholders, truncation and accessibility names.
- [Content QA and experiment boundaries](references/content-quality-and-evaluation.md) — **read when** reviewing UI wording in journeys, proposing copy tests or validating release readiness.

## Coordination
`growth/content-strategy` owns editorial strategy, `landing-page-design` owns landing conversion narrative, `information-architecture` owns cross-page labels/taxonomy, `ux-audit` owns findings, and `ui/<provider>` owns component API. Do not claim tested comprehension without participants.

## Exit
Concise copy table keyed by UI state and source/context, glossary changes, localization risks and a reproducible review procedure.
