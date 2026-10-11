---
name: ui-component-research
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, debugging or reviewing nontrivial UI components and their exact documented APIs, states, accessibility and integration across component libraries. Do not use for simple CSS copy changes or generic visual design.
---

# UI component research and implementation

This complements one selected provider skill and `frontend-design`. It does **not** pretend that Button, Dialog, Table or other names share an API across libraries.

## Research contract (per component)

1. Identify the exact runtime and **installed** library/primitive package versions, design token system and component implementation (local source, npm package, native widget, Web Component). Do not invent undocumented props.
2. Look up **that version's official page** for the requested component, its composition/anatomy, API reference, runnable example and upgrade notes. Third-party snippets may inspire but are not authoritative; check licenses before copying.
3. Enumerate supported primitives and parts, props/events, controlled/uncontrolled state, slots/render props, selected/disabled/read-only states, loading, errors, empty content, portal/overlay and SSR/native lifecycle. Record only relevant details.
4. Inspect present project usage and adapt the official pattern to local theme tokens, icons, routing, forms and state management. Favor standard component semantics and built-in capabilities over hand-written substitutes.
5. Implement or review with the **smallest correct abstraction**, then test positive/negative interactions, keyboard/screen reader use, mobile, dark mode, i18n/RTL where relevant and error paths.
6. If current docs cannot be accessed, clearly state that the API is unverified and avoid speculative usage.

## Family references (open only what is needed)

- [Inputs and forms](references/inputs-and-forms.md) — validation, field wiring, picker semantics.
- [Overlays and navigation](references/overlays-and-navigation.md) — focus, portals, menus, dialogs and routing.
- [Data display](references/data-display.md) — tables, grids, async and virtualization.
- [Feedback and theme](references/feedback-and-theme.md) — loading, toasts, accessibility and tokens.

## Boundary

A component is not a new skill merely because it has a unique name. Create a **specialized subskill** only if it adds a distinct reusable workflow (e.g. a complex table engineering/testing methodology), validated against existing skills. Otherwise use small references and the provider’s official docs.
