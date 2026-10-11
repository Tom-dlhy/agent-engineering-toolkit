---
name: dark-mode-theming
domain: design
version: "2.0.0"
description: >-
  Use when implementing or auditing light/dark theme switching, system color preferences, semantic surfaces, high-contrast adaptations or theme hydration. Do not invert colors blindly or create parallel tokens for an established design system.
---

# Adaptive color themes — semantic contract, not color inversion

## Decision procedure
1. Inventory the existing theme provider, CSS variable naming, component library, brand constraints, supported browsers, SSR/hydration and persisted user settings. Reuse the owner of the tokens.
2. Resolve preference precedence deliberately: explicit user choice, otherwise system choice, otherwise a documented default. Use one authoritative theme state and avoid storing duplicate state in every component.
3. Define/extend **semantic** surface, content, border, interactive, focus, status and data-visualization roles in each supported theme. Audit real states, not a palette screenshot.
4. Align `color-scheme` with the resolved theme so built-in form controls, scrollbars and page chrome agree. Avoid first-paint flashes and React hydration mismatches; do not require JavaScript for a readable baseline.
5. Validate contrast, focus, error, disabled, selected, tables, SVGs, external logos, code, overlays, chart legends, dark images and forced colors. Preserve meaning independent of hue.
6. Check system theme changes, manual override persistence, cookies/SSR boundaries and browser back/forward restoration where relevant.

## Deep branches
- [Theme precedence, semantic tokens and SSR](references/theme-state-and-tokens.md) — **read when** designing token mappings, theme switching, system preferences or avoiding hydration flashes.
- [Contrast, assets and forced-color acceptance](references/theme-contrast-and-assets.md) — **read when** checking controls/charts/logos, overlays, contrast or forced-colors accessibility.

## Ownership and result
`design-system` owns core token architecture and provider source; this skill owns mode-specific behavior and verification. `accessibility-wcag` owns formal criteria. `frontend-design` owns intentional brand appearance. Output actual theme acceptance evidence and untested browsers, never universal compatibility claims.
