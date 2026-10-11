# Theme contrast, images and forced-color verification

Read when: checking dark/light tokens, interactive states, content graphics, brands/logos, glass surfaces or high-contrast fallbacks.

## Test combinations instead of colors in isolation
Enumerate semantic roles: background/surface/raised/overlay, primary/muted/disabled copy, links/visited, focus/borders, required/invalid/success/warning, chart data, skeleton, selection and code. For each role check actual **foreground against adjacent rendered background**, including hover/pressed/selected and dynamic photography. Contrast is not a single palette score.

A critical form should demonstrate readable label, hint, field border, error, focus ring and disabled indication in both themes. Non-text necessary control borders and meaningful icons have WCAG 1.4.11 AA 3:1 expectations; text requirements differ by text size and exceptions. Disabled components are exceptions in some WCAG contrast criteria, but don't treat that as permission for unreadable key workflow information.

## Assets
- Prefer theme-neutral SVG with semantic colors where brand guidelines permit; never recolor third-party logos without permission.
- Provide light/dark asset variants when essential, with coherent alt text and no duplicate announcement.
- Charts need legends/patterns or labels, not hue alone. Tables must retain row dividers/active cell focus and empty/error cues.
- For `forced-colors: active`, rely on system colors and browser defaults when possible, preserve visible outlines and borders, and test instead of blindly opting out with `forced-color-adjust: none`.

## Test matrix and common failures
Dark first paint, light first paint, system flips, manual override persistence, dialogs over scrims, tooltips over images, data/empty/error states, forced-colors, 200% zoom and screenshot comparison. Avoid CSS `filter: invert(1)` as theming strategy; it corrupts photos/brands/meaning. Report browser support gaps and whether checks were manual or static.

Official: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/forced-colors and https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast
