# Design category — governance decision matrix and source-reviewed refactor

Review date: 2026-10-11. Base: main after UI PR #21. Governance: Agent Engineering Toolkit charter v2.
Scope: exactly 12 existing Design skills, keeping Core/Frontend/UI/Growth ownership explicit.

## Decision matrix — assess before editing

| Skill | Decision | Why this level of responsibility survives / changes | Deep expertise and boundaries |
|---|---|---|---|
| `accessibility-wcag` | **EXTEND** | Formal normative compliance mapping and manual AT journeys are independent of UI aesthetics/UX | Added WCAG 2.2 triage, accessible interactions, manual verification. UI-provider owns concrete component API. |
| `bento-grid` | **EXTEND (opt-in)** | Narrow autonomous explicit "implement bento" request, but inappropriate as an always-installed generic design skill | Added source-order, grid and responsive reference; removed from broad ui-ux-design profile. Reconsider REFERENCE if observed routing collisions. |
| `brand-identity-visualization` | **REUSE** | Distinct purpose: visual identity concept boards, not page implementation; already two technical references | No duplication of frontend art direction or image production in other skills. |
| `dark-mode-theming` | **EXTEND** | Independent theme state, SSR and accessibility behaviors are not just global tokens | Added precedence/SSR tokens and contrast/assets references. Design-system retains token ownership. |
| `design-system` | **REUSE** | Existing product tokens, ownership, migration and component contracts are coherent | Two references retained; no parallel theme provider. |
| `frontend-design` | **REUSE** | Art direction, grounded composition and anti-template critique improved in UI PR #21 | Three existing references retained, no "anti-slop" duplicate skill. |
| `glassmorphism` | **EXTEND (opt-in)** | Explicit surface-effect implementation has distinct CSS and fallback constraints; no default promotion | Added progressive enhancement/fallback/QA; removed from broad profile. Reconsider consolidation if usage is rare. |
| `interaction-motion` | **REUSE** | Motion construction, easing, performance and review already have four leaves | Don't add another animation discipline skill. |
| `landing-page-design` | **EXTEND** | Conversion narrative, factual claims and landing-page journeys are distinct from generic art direction | Added narrative/evidence and conversion/verification; no invented social proof or measured uplift. |
| `responsive-visual-qa` | **EXTEND** | Rendered screenshot and state matrix is independently testable from UX critique | Added viewport matrix and screenshot baseline/diff triage. No static-review-as-browser claim. |
| `typography-layout` | **REUSE** | Type scale, editorial grid and reading hierarchy already scoped and referenced | Two existing leaves retained; layout is not synonymous with "bento everywhere". |
| `ux-audit` | **REUSE** | Evidence-based usability diagnosis, severity and repro distinct from WCAG conformance | Two existing leaves retained; no replacement by screenshots alone. |

Decision tally: **6 EXTEND, 6 REUSE, 0 CREATE/IMPORT/DELETE**.
Design retains **12 opt-in catalog skills** and gains **11 local task-scoped references** (26 local Design leaves in total).
No third-party skill copied; educational synthesis draws on authoritative public specifications and existing prior source review.

## Why not delete bento-grid and glassmorphism today?

Both are specialized and sometimes dispensable, but they have explicitly searchable names, unique triggers and potential direct installation consumers. Deleting them now would break opt-in profiles and scripts while forcing global test/catalog count rewrites. The least-risk durable action is:
- Preserve the explicit opt-in names and paths, including `SKILL.md` entry points.
- Narrow discovery descriptions/keywords and discourage unsolicited stylistic application.
- Remove from the **general** `ui-ux-design` profile. Users who need the style can request/install it intentionally with `--skill`.
- Review collisions and real activation frequency in later behavioral evaluation before deprecation or converting to a leaf.

This is **not** an assertion that every visual trend deserves a skill. No new style micro-skills are authorized by this refactor.

## Concrete ownership map

| Request | Primary owner | Conditional peer |
|---|---|---|
| "Make this interface distinctively on-brand" | frontend-design | design-system, typography-layout |
| "Audit WCAG 2.2 AA for checkout" | accessibility-wcag | ui/provider, responsive-visual-qa |
| "Dialog API and focus trap in Base UI" | ui/base-ui | accessibility-wcag |
| "Implement dark mode with SSR no-flash" | dark-mode-theming | design-system + selected frontend |
| "Compare two component libraries" | stacks/ui-library-selection | UI provider only after choice |
| "Fix responsive screenshots at 320 and 390 px" | responsive-visual-qa | accessibility-wcag if criterion suspected |
| "Build a landing page to capture real inquiries" | landing-page-design | frontend-design, technical-seo for crawl |
| "Create bento layout" or "frosted overlay" | explicitly named specialist | frontend-design when page aesthetics affected |

## Source verification and supported facts

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/ ; Understanding target size minimum: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
- W3C Focus Not Obscured (Minimum) AA: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum ; Focus Appearance AAA: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance
- WAI Accessible Rich Internet Applications Dialog Pattern: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- MDN CSS grid accessibility: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Accessibility
- MDN `prefers-reduced-transparency`: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-transparency — limited support; not assumed universal.
- MDN `color-scheme`: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
- Playwright screenshot assertions: https://playwright.dev/docs/test-snapshots

Sources are used for **technical rules**, not copied as wholesale third-party skills. Any version-sensitive runtime assumption must be checked against the actual installed stack.

## Validation scope and honesty

Deterministic CI can verify metadata, local path-safe reference loading, breadth of new technical leaves, routing examples and profile budgets. The new `evals/design-routing.yaml` is a **manual behavioral evaluation specification**; it is not an observed result. Before certifying improved agent performance, run held-out tasks with and without toolkit on actual codebases and screens; record source selection, loaded references, actual context tokens, defects, browser/AT coverage and reviewer outcomes. Do not claim that passing unit tests proves real WCAG conformance, higher conversion or visual originality.

## Scope boundaries / next phase
- No invasive edits to already-depthful Brand, Design System, Frontend Design, Interaction Motion, Typography or UX skills.
- No new UI library, automatic animations, runtime dependency or external executable script.
- No unapproved merge into main.
- Growth and Stacks remain separate next refactors.
