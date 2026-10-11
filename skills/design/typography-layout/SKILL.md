---
name: typography-layout
domain: design
version: "2.0.0"
description: >-
  Use when selecting or reviewing type systems, readable line lengths, editorial grids, spacing, responsive typography or text-heavy page hierarchy. Do not override approved brand typography for aesthetic novelty.
---

# Typography and layout

## Decision procedure

1. Inventory installed fonts, design tokens, content types, brand constraints, localization and font licenses. Define reading requirements before font selection.
2. Choose an explicit hierarchy for display, headings, body, captions, labels and data; the number of different families should be justified.
3. Establish responsive type scale, line lengths, line-height and spacing; handle long labels, tables, dates and untranslated strings.
4. Use semantic heading order and reading direction. Grid/asymmetry should reflect content relationships rather than random card placement.
5. Validate with actual body copy, errors, empty/loading states, 200% zoom and narrow viewports.
6. Check font loading and layout shift; no license-incompatible font redistribution.

## Targeted references

- [Type scale and font pairing decisions](references/type-scale-and-pairing.md) — **read when** choosing font families, display/body pairing, type scale, rhythm and content readability.
- [Grid, composition and responsive text QA](references/editorial-grids-and-qa.md) — **read when** structuring long-form content, responsive layouts, data density and typography regressions.

## Coordination

Design-system owns token storage, frontend-design owns overall visual direction, and accessibility-wcag owns conformance evaluation.

## Completion

The type system works with actual content, multilingual/mobile states, stable rendering and documented font licensing.
