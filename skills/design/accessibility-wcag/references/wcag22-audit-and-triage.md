# WCAG 2.2 AA interpretation and issue triage

Read when: mapping reproducible issues to normative WCAG success criteria, or prioritizing keyboard/contrast/reflow/touch remediation.

## Method: map real behavior, not a rule-of-thumb
1. Capture route, step, browser, platform, element, observed behavior, expected behavior and affected users.
2. Identify the precise criterion and level in the W3C normative standard; report `not assessed` when tests are missing.
3. Check exceptions before declaring failure; record the reasoning. Automated tools detect a subset of issues.
4. Group repeated defects by shared component root cause and prioritize by user impact and critical journey.

| Issue | Relevant criterion | Practical test |
|---|---|---|
| Normal text illegible | 1.4.3 Contrast (Minimum), AA | Contrast ratio at least 4.5:1, or 3:1 for large text, subject to exceptions |
| Control outline/border invisible | 1.4.11 Non-text Contrast, AA | 3:1 for visual information necessary to identify UI and state |
| Narrow reading forces horizontal scroll | 1.4.10 Reflow, AA | 320 CSS px width equivalent, except genuine two-dimensional content |
| Keyboard focus hidden by sticky banner | 2.4.11 Focus Not Obscured (Minimum), AA | Focused item must not be **entirely** hidden by author-created content |
| Targets densely clustered | 2.5.8 Target Size (Minimum), AA | At least 24x24 CSS px **or** applicable spacing/equivalent/inline/essential exception |
| Focus indicator too faint | 2.4.7 Focus Visible, AA | Visible keyboard focus; 2.4.13 Focus Appearance has separate **AAA** requirements |

Do **not** conflate WCAG AA minimum touch sizing with a stronger internal 44x44 px design heuristic. Do not claim that all controls must be 24 px if an actual criterion exception applies.

## Reproducible triage example
```text
Route: /checkout
Journey: keyboard Tab from postal code to Submit
Viewport: 390x844 CSS px, browser + version noted
Observed: sticky consent banner covers focused Submit button entirely
Normative candidate: WCAG 2.2 2.4.11 (AA)
Fix: content offset or scroll-margin/padding, then verify with real keyboard
Evidence: screenshot before/after + keyboard steps + browser
```
A failed static selector assertion is not the same as an observed keyboard failure. A screen-reader accessibility claim requires an assistive-technology run.

## Verified primary references
- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
- https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum
- https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast
