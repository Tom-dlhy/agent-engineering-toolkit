---
name: react-aria-components
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing React Aria Components components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# React Aria Components — provider-specific UI engineering

**Best fit:** complex accessible interactions, keyboard use, internationalization and custom styling.
**Target stack:** React, TypeScript; enterprise, international or accessibility-sensitive web apps.
**Official documentation:** https://react-spectrum.adobe.com/react-aria/components.html

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** ComboBox, Select, ListBox, DatePicker, Calendar, Table, GridList, Dialog, Form.

**Provider-specific method:** Pin the installed react-aria-components version; consult each component’s accessibility and composition docs. Use documented slots and render props, collection APIs, validation behavior and locale/date handling. Prefer higher-level components before dropping to hooks.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not replace its collection and selection state with ad hoc click handlers. Test keyboard navigation, screen reader labels, RTL, timezone/date and controlled state as applicable.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.

## V2 local expertise — open only the applicable leaf

- [Button, Dialog, Popover, ComboBox, Select, Table, ListBox — implementation patterns](references/component-patterns.md) — **read when** implementing or debugging Button, Dialog, Popover and component anatomy, behavior, controlled state.
- [Integration, theming and regression checks](references/integration-and-verification.md) — **read when** integrating react-aria-components with SSR, forms, themes, upgrades, tests or app delivery.

For ordinary tasks, this `SKILL.md` is sufficient to choose the next action. **Do not bulk-load both leaves** unless the request genuinely spans implementation and integration. A skill available in the catalog is not permission to install its package.

## Current provider contract and visual identity

React Aria Slots/collections/render props and locale-aware date/key semantics are not Radix/Base anatomy. Preserve keyboard/focus/error styling when applying brand tokens. Official: https://react-spectrum.adobe.com/react-aria/components.html
For **art direction**, activate the existing `frontend-design` skill; this library skill owns exact props, composition, states, version compatibility and accessibility. Do not ship the stock demo skin or force visual novelty contrary to the product brief.
