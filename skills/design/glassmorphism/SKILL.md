---
name: glassmorphism
domain: design
version: "2.0.0"
description: >-
  Use when explicitly implementing or reviewing frosted-glass, translucent layered or glassmorphism surfaces in an existing brand. Do not activate for a routine button, dense forms, tables, or an unrequested visual trend.
---

# Glassmorphism — opt-in effect with reliable fallback

## Decision gate
1. Require an explicit design brief or an existing glass aesthetic; avoid default adoption. Identify the real content, background variants, overlays and interaction density.
2. Limit translucent surfaces to places where layering communicates depth or hierarchy. Use design-system color/blur/border tokens, not scattered opacities or a new visual language.
3. Compose from a readable opaque fallback first; progressive-enhance blur only with supported `backdrop-filter`. Keep focus rings, critical copy and actionable controls legible above dynamic backgrounds.
4. Check `prefers-reduced-transparency` as an optional enhancement (not supported everywhere), forced-colors and reduced-motion if animations exist. Never rely on blur/transparency for meaning.
5. Profile expensive large/nested blur only when necessary; check low-power devices and screenshots with multiple backgrounds. Avoid assuming a translucent layer satisfies contrast on every photograph.

## Deep branch
- [Progressive enhancement, fallback and visual acceptance](references/translucency-fallback-and-qa.md) — **read when** implementing CSS frosted surfaces, debugging contrast or motion/reduced-transparency/forced-color behavior.

## Boundaries
`frontend-design` sets art direction; `design-system` owns global tokens; `accessibility-wcag` evaluates conformance. A glass request does not authorize brand redesign or adding animation dependencies. Exit with readable fallback and verified representative backgrounds.
