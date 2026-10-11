---
name: interaction-motion
domain: design
version: "0.1.0"
description: >-
  Use when adding animations, micro-interactions, transitions or motion storytelling to product interfaces. Do not use motion for decoration that harms comprehension or accessibility.
---

# interaction-motion

## Intent
State what motion communicates: feedback, hierarchy, continuity, progress or delight. Prefer easing/duration tokens shared across the product.
## Technical implementation
Use CSS transitions for simple interactions; add animation dependencies only where sequence complexity justifies them. Favor transform/opacity for performance; avoid continuous heavy shadows/filters and layout-thrashing properties.
## Accessibility
Respect prefers-reduced-motion with meaningful non-animated states. Never gate crucial information behind animation. Ensure keyboard and pointer interaction produce consistent feedback.
## Verify
Test low-power mobile, slow CPU, transitions between routes, dialogs and loading states; guard against double-submits, focus loss and motion-triggered nausea.
