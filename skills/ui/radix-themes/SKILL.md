---
name: radix-themes
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Radix Themes components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Radix Themes — provider-specific UI engineering

**Best fit:** ready-styled Radix design language with consistent theme scales.
**Target stack:** React, TypeScript; applications adopting Radix’s cohesive visual system.
**Official documentation:** https://www.radix-ui.com/themes/docs/overview/getting-started

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** Theme, Button, Flex, Grid, Text, Dialog, Select, Table, Data List.

**Provider-specific method:** Check installed @radix-ui/themes version and global stylesheet. Work through Theme configuration (accent, gray, radius, scaling), component appearance and responsive prop conventions; reuse theme primitives rather than introducing ad hoc CSS.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not treat Themes as unstyled Primitives or fork its styling for trivial needs. Keep Theme provider and imported CSS consistent across SSR entry points.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.

## V2 local expertise — open only the applicable leaf

- [Theme, Button, Dialog, Flex, Grid, Text, Table — implementation patterns](references/component-patterns.md) — **read when** implementing or debugging Theme, Button, Dialog and component anatomy, behavior, controlled state.
- [Integration, theming and regression checks](references/integration-and-verification.md) — **read when** integrating radix-themes with SSR, forms, themes, upgrades, tests or app delivery.

For ordinary tasks, this `SKILL.md` is sufficient to choose the next action. **Do not bulk-load both leaves** unless the request genuinely spans implementation and integration. A skill available in the catalog is not permission to install its package.

## Current provider contract and visual identity

Distinguish styled Radix Themes from Radix Primitives; adjust Theme accent/gray/radius/scaling and test contrast, not stock demo palette. Official: https://www.radix-ui.com/themes/docs/theme/overview
For **art direction**, activate the existing `frontend-design` skill; this library skill owns exact props, composition, states, version compatibility and accessibility. Do not ship the stock demo skin or force visual novelty contrary to the product brief.
