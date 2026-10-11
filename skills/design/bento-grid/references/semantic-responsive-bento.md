# Semantic and responsive CSS bento layout

Read when: implementing explicit varied tile sizes, bento focus/reading order or stable responsive tile layout.

## Choose content first
Write content in *logical DOM reading order*: the most important feature, secondary proof, supporting explanation, last action. Don't position tile DOM nodes based only on a desktop screenshot. Grid `order` and `grid-auto-flow: dense` can create a **visual order different from keyboard/screen-reader order**; don't use them to rescue arbitrary composition gaps.

## Adaptable CSS pattern
```css
.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(.75rem, 2vw, 1.5rem);
}
.feature-grid > * { min-width: 0; }
@media (min-width: 64rem) {
  .feature-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .feature-grid > .feature--primary { grid-column: span 2; grid-row: span 2; }
  .feature-grid > .feature--wide { grid-column: span 2; }
}
@media (max-width: 42rem) {
  .feature-grid { grid-template-columns: minmax(0, 1fr); }
}
```
This is a starting pattern for a known number of ordered tiles, not a guarantee against gaps; test placement with real content and ensure spans don't force overflow. Avoid fixed heights for text-heavy cards; use `aspect-ratio` only for visual media, not content capacity.

## Negative and acceptance
A dense analytics table is not automatically a bento. Never duplicate KPI/partner facts to fill holes. Check mobile cards stack in semantic order, focus order follows visible reading sequence, long translated copy wraps, hover info is also available with keyboard/touch, tile CTA naming is unambiguous and no chart renders invented metrics.

Official: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Accessibility and https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Auto-placement
