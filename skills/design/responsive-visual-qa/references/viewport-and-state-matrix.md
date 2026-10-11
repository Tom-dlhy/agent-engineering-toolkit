# Adaptive viewport and content state matrix

Read when: deciding screen widths, overflow/reflow acceptance or testing complex responsive content, localization and zoom.

## Select cases from actual layout breakpoints
Rather than checking only 375/768/1440 screenshots, inspect CSS containers, min-width constraints and content structure. Include near-breakpoint widths on **both sides**; target known bugs in between. Representative baseline: narrow ~320 CSS px, common mobile ~390, tablet ~768, desktop ~1280, plus browser zoom equivalent and real text scaling. These are **test candidates**, not guaranteed universally sufficient. Use more if the product has unusual display surfaces.

## Matrix dimensions
```text
route | viewport CSS px | browser/DPR | theme/locale |
state | interaction | expected | actual | artifact
/product | 320x720 | Chrome / 1 | light/fr |
long title | menu open | no clipped CTA | [fill after run] | [path]
```
Test keyboard navigation, tab order and sticky offsets; sidebar and modal with viewport height constraints; media aspect ratios and width/height/responsive `srcset`; long localized labels, user-generated content, lists and loaded charts. Responsive is also input method, not just width.

## Intrinsic sizing fix before extra media queries
Use `min-width: 0` for flex/grid children that refuse to shrink, `minmax(0, 1fr)` for min-content traps, `max-width: 100%` on media and well-defined wrapping/overflow strategies on dense tables. Do not hide essential actions with `overflow: hidden`. Two-dimensional charts/tables may require a labeled horizontal scroll region plus a usable alternative, not truncation.

## Evidence
When browsers cannot be run, provide a static risk analysis and explicit unverified cases. Checking breakpoints from source is not a screenshot pass. Prefer path + reproducible URL, UI state and captured artifact, then re-test one width below/above a correction.

Official: https://www.w3.org/WAI/WCAG22/Understanding/reflow and https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Accessibility
