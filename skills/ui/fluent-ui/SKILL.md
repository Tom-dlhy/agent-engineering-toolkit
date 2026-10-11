---
name: fluent-ui
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Fluent UI React components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Fluent UI React — provider-specific UI engineering

**Best fit:** Microsoft-inspired enterprise UI and accessibility conventions.
**Target stack:** React, TypeScript; Microsoft 365 and enterprise products.
**Official documentation:** https://react.fluentui.dev/

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** FluentProvider, Button, Dialog, Combobox, DataGrid, Menu, Tooltip, TabList.

**Provider-specific method:** Identify @fluentui/react-components version and v9 vs legacy packages. Configure FluentProvider and Griffel styling; follow Fluent slot patterns and controlled state for complex components.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not mix v8 and v9 APIs without an explicit compatibility plan. Keep Microsoft accessibility and density conventions consistent.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.

## V2 local expertise — open only the applicable leaf

- [Button, Dialog, Field, Combobox, DataGrid — implementation patterns](references/component-patterns.md) — **read when** implementing or debugging Button, Dialog, Field and component anatomy, behavior, controlled state.
- [Integration, theming and regression checks](references/integration-and-verification.md) — **read when** integrating fluent-ui with SSR, forms, themes, upgrades, tests or app delivery.

For ordinary tasks, this `SKILL.md` is sufficient to choose the next action. **Do not bulk-load both leaves** unless the request genuinely spans implementation and integration. A skill available in the catalog is not permission to install its package.
