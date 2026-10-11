---
name: ui-library-selection
domain: stacks
version: "2.0.0"
description: >-
  Use when choosing or comparing UI component libraries or design systems across React, Vue, Angular, Svelte, mobile and Flutter. Do not use for a component implementation when the project's library is already fixed.
---

# UI library selection — decision, not implementation

## Inspect first
1. Read package manifests, lockfile and source imports: an established, healthy UI library wins by default. Do not migrate because another kit looks fashionable.
2. Identify target framework, SSR/native environment, styling system, accessibility goals, locale/RTL, team expertise, custom theme needs, license and production constraints.
3. Distinguish **headless primitives** (own styling), **styled systems** (theming/layout constraints) and **source-owned components** (local maintenance responsibilities).
4. Shortlist at most three credible candidates; compare a real Form, Dialog, navigation pattern, data view and dark-mode/RTL behavior, including their accessibility and upgrade paths.
5. Select one primary library unless integration reality demands multiple, document tradeoffs in a short ADR.

## Branch selection

- [Provider comparison and official docs map](references/library-map.md) — **read only** for library choice, migration or cross-stack evaluation; this is an index, not a technical implementation manual.
- When the provider is selected, activate the corresponding `skills/ui/<provider>/SKILL.md` installed in the project. The provider skill has authoritative instructions and targeted deep references.
- Activate `ui-component-research` only when the task requires complicated component anatomy, lifecycle or accessibility; avoid activating all 35 providers.
- Existing `frontend-design` owns visual direction; `design-system` owns global tokens.

## Verification
Decision must identify a real compatible version, license limitations, accessibility behavior, integration risk, API migration cost and the minimal safe installation plan. A comparison does not authorize installing packages or changing the design system.
