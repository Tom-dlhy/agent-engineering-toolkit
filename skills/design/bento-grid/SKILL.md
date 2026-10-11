---
name: bento-grid
domain: design
version: "2.0.0"
description: >-
  Use when specifically requested to implement or repair a bento-style composition with mixed-size content tiles and responsive reading order. Do not activate for an ordinary grid, dashboard cards, or simply because bento is fashionable.
---

# Bento grid — opt-in composition specialist

## Before coding
1. Verify the user really asked for a bento-like layout; otherwise use `frontend-design` or `typography-layout` without activating this niche skill.
2. Rank **real content** by importance, determine the few hero tiles and choose the DOM reading/focus order before configuring spans. Bento is a layout, not a component library.
3. Start from an intrinsic responsive grid, use explicit spans only when space and reading order permit, and avoid `grid-auto-flow: dense` when interactive tiles can be visually reordered from DOM order.
4. Limit tile variety, depth effects and mobile nesting. Every tile must convey a distinct task, feature or proof; avoid decorative icon placeholders and meaningless KPI cards.
5. Verify keyboard sequence, mobile stacking, long labels/translations, 200% zoom and narrow widths, touch targets, contrast, loading/empty/error and image cropping.

## Deep branch
- [CSS Grid spans, source order and responsive fallback](references/semantic-responsive-bento.md) — **read when** implementing mixed-size tile placement or debugging focus/reading-order and responsive bento problems.

## Contract
`frontend-design` chooses the visual direction; `typography-layout` owns the overall type/grid system; `ui/<provider>` owns exact card APIs. No automatic application of bento to a product page. Deliver a verified information hierarchy and CSS/layout behavior, not a stylistic trend recommendation.
