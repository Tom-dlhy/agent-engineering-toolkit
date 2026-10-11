---
name: dark-mode-theming
domain: design
version: "0.1.0"
description: >-
  Use when creating or auditing dark mode, adaptive color themes or high-contrast UI variants. Do not invert colors blindly or force dark mode against product requirements.
---

# dark-mode-theming

## Tokens
Define semantic foreground/surface/muted/border/interactive tokens with light and dark values. Avoid raw color literals scattered through components.
## Accessibility
Measure actual contrast in both themes including hover, disabled, focus, selected, errors and overlays. Treat photos, charts and translucent surfaces separately. Honor user/system preference and prevent flashing the wrong theme on hydration.
## Components
Test code blocks, forms, dialogs, navigation, skeleton loaders, charts and SVG logos under all themes. Keep brand identity coherent without sacrificing legibility.
## Performance
Prefer CSS variables and native color schemes over runtime re-rendering where reasonable.
