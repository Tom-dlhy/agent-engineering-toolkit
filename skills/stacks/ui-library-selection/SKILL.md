---
name: ui-library-selection
domain: stacks
version: "0.1.0"
description: >-
  Use when selecting accessible component libraries and design systems across React, Vue, Angular, Svelte or other UI stacks. Do not replace a healthy existing component library for aesthetic novelty.
---

# ui-library-selection

## Criteria
Assess framework compatibility, accessibility primitives, theming API, visual customization, CSS strategy, maintenance cadence, bundle impact, license and team expertise.
## Categories
Distinguish headless primitives from styled component libraries and copy-into-repo component collections. For example, a design system can be built with accessible headless primitives and local tokens, or with a stable styled library for delivery speed.
## Proof of fit
Prototype a form, dialog, keyboard navigation, responsive table and theming variant. Test with keyboard and a screen reader when possible; do not treat an accessibility claim as a substitute for testing.
## Decision
Prefer consistency and operational simplicity over mixing five overlapping packages. Record upgrade and migration costs.
