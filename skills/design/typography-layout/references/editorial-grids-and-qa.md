# Responsive composition — grids, negative space and reading order

**Read when:** implementing editorial or content-heavy layouts, grids, dense screens or typography QA across breakpoints.

## Layout invariants

Visual hierarchy must track DOM/keyboard reading order. A dramatic asymmetrical grid that visually moves content ahead of its accessible DOM sequence can confuse keyboard/screen reader users. Start from semantic article/section structures; use CSS Grid/Flex to enhance relationships.

### Example editorial shell

~~~css
.editorial-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(1rem, 2vw, 2rem);
}
@media (min-width: 56rem) {
  .editorial-layout {
    grid-template-columns: minmax(0, 15rem) minmax(0, 68ch);
    justify-content: center;
  }
}
.editorial-layout > * { min-width: 0; }
~~~

Breakpoints should be content-led. A minmax(0, ...) child can prevent overflow, but code editors and wide data tables may need their own scroll containment rather than page-level clipping.

## Content hierarchy checklist

- Primary action and core message visible before decorative supporting details.
- Distinct eyebrow, heading, body and caption semantics, not only varying font sizes.
- Line length readable; whitespace establishes grouping instead of huge unused voids.
- Consistent alignment anchors across sections even when section backgrounds differ.
- Avoid uncontrolled text overflow, orphan buttons, heading widows and cropped CTA labels.
- Use logical properties (padding-inline etc.) where RTL is required.

## Real viewport review

Validate widths approximately 320–375px, tablet and desktop according to project support; inspect orientation and large text. Use actual localized copy, long field errors, empty state, navigation and table rows. At 200% browser zoom check that controls remain reachable.

## Performance details

Reserve space for image/media. Review loading fallback font metrics to limit CLS. Use content visibility sparingly; not on sections needing immediate focus/accessibility. Avoid artificially truncating important headings just to preserve screenshot shape.

## Evidence

Report viewport, device/browser, actual screenshot/test availability, observed overflow/reading bugs and smallest scoped fix. No CSS-only self-assertion that responsive design passed.

Further reading: https://web.dev/articles/responsive-web-design-basics and https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/67803eac81607188194aea9842a723b89326d90d/.claude/skills/ui-ux-pro-max/SKILL.md .
