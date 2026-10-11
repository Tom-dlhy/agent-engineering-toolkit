---
name: design-system
domain: design
version: "0.1.0"
description: >-
  Use when establishing reusable UI design tokens, components, patterns and governance for a growing product. Do not create a new system for a one-page site with fixed branding.
---

# design-system

## Foundations
Inventory existing colors, typography, spacing, radii, elevation, focus outlines, density and motion. Define semantic tokens (surface/foreground/accent/error) distinct from raw palette values.
## Components
Build a small set of accessible primitives (button, input, dialog, navigation), then compose product-specific patterns. Define variants and interaction states, not just screenshot-perfect default states.
## Documentation
Include usage rules, do/don't examples, content guidance, a11y criteria and change ownership. Keep tokens integrated with the actual UI stack and avoid duplicate theme configuration.
## Verification
Test light/dark/high-contrast modes where supported, browser responsiveness, keyboard flows, screen-reader semantics and automated visual regressions.
