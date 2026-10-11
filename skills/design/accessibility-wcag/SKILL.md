---
name: accessibility-wcag
domain: design
version: "2.0.0"
description: >-
  Use when implementing, auditing or remediating WCAG 2.2 accessibility, keyboard journeys, focus, screen readers, accessible forms or touch targets. Do not claim WCAG conformance from linting or automated scans alone.
---

# Accessibility WCAG — user journey first, evidence always

## Observe and scope
1. Identify the actual product, WCAG target (typically 2.2 AA if required), supported languages, devices, browsers, critical user journeys, design system and allowed assistive technology.
2. Separate a **normative WCAG success criterion** from a recommended technique, usability heuristic or AAA enhancement. Log criterion number/level only when verified against the actual requirement.
3. Start with native semantics (landmarks, buttons, links, labels and form elements), then apply ARIA only when HTML cannot express the interaction. Preserve the UI provider's documented keyboard and focus contracts.
4. Trace each critical journey with keyboard alone: entry, focus visibility/order, forms/errors, overlays, escape/restore focus and success announcement. Check screen-reader name/role/state and reading order on representative platforms.
5. Measure text/nontext contrast, target size **or permissible spacing exceptions**, reflow/zoom, obscured focus, motion, reduced-motion and high-contrast/forced-colors behavior. Distinguish WCAG 2.2 AA Focus Not Obscured (Minimum) from AAA Focus Appearance.
6. Fix the smallest semantic or component-root cause; add a regression test and verify the actual user flow, not just the DOM snapshot.

## Select one deep branch
- [WCAG 2.2 AA interpretation and issue triage](references/wcag22-audit-and-triage.md) — **read when** mapping concrete findings to criteria, assessing contrast/zoom/target/focus or prioritizing remediations.
- [Forms, dialogs and dynamic updates](references/accessible-interaction-contracts.md) — **read when** implementing or fixing labels, errors, modal focus, status messages or composite widgets.
- [Real-device verification and evidence](references/manual-a11y-verification.md) — **read when** assembling keyboard/screen-reader test plans, accessibility regression evidence or a conformance report.

## Boundaries and exit
`ux-audit` owns holistic usability prioritization; `responsive-visual-qa` owns cross-viewport capture; `ui/<provider>` owns exact component APIs; `design-system` owns accessible semantic tokens. Activate them only as needed. Never claim certification, user testing or actual screen-reader testing without evidence. Deliver reproducible issues, applicable criteria, impact, verification method, unresolved risks and tested environments.
