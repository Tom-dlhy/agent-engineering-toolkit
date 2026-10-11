---
name: responsive-visual-qa
domain: design
version: "2.0.0"
description: >-
  Use when checking rendered web or app UI across real viewport widths, zoom, languages, themes and interaction states, including screenshot regressions. Do not equate reading CSS or passing a snapshot with complete visual or accessibility QA.
---

# Responsive visual QA — reproduce, capture, repair

## Procedure
1. Identify affected routes/components, relevant critical user tasks, existing screenshots/baselines, browser engines, fonts, device scale, viewport dimensions and actual content.
2. Build an **adaptive matrix** (narrow phone, wider phone, tablet, desktop, plus 320 CSS px-equivalent reflow and text scaling where relevant). Include landscape, long strings, empty/loading/error, open menus, dialogs, virtual keyboard and light/dark when applicable.
3. Run real render checks when a browser is available; record viewport CSS pixels, browser/OS, DPR/zoom, route, viewport state, fixture, date and screenshot artifact. Code inspection alone is not visual proof.
4. Inspect content clipping, horizontal scrolling, overlap/sticky headers, crop, landmarks, type, focus, touch targets, hover-only affordances, localization, responsive image loading and layout shift.
5. Separate deterministic diffs from environment noise (font rasterization, animations, timestamps, asynchronous data). Never approve snapshot changes blindly.
6. Repair the smallest reusable root cause (container, intrinsic sizing, min-width, breakpoints or tokens), then retest the affected state and adjacent widths.

## Deep branches
- [Adaptive viewport and state matrix](references/viewport-and-state-matrix.md) — **read when** choosing breakpoints, checking reflow/zoom, complex content and mobile overflow.
- [Screenshot baseline discipline and defect reproduction](references/screenshot-baselines-and-triage.md) — **read when** writing visual regression tests, stabilizing screenshots or assessing screenshot diffs.

## Hand-offs and evidence
Use `accessibility-wcag` for conformance and real assistive-tech testing, `ux-audit` for user-journey impact and `frontend-design` for art-direction changes. Report tested/not-tested browser-viewports, defects, fixes and artifacts; do not claim a visual pass when rendering was unavailable.
