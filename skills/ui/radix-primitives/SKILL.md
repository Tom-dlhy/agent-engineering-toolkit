---
name: radix-primitives
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Radix Primitives components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Radix Primitives — provider-specific UI engineering

**Best fit:** unstyled React interaction primitives for accessible custom interfaces.
**Target stack:** React, TypeScript; custom styling and design systems.
**Official documentation:** https://www.radix-ui.com/primitives/docs/overview/introduction

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** Dialog, Dropdown Menu, Select, Tooltip, Popover, Tabs, Accordion, Navigation Menu.

**Provider-specific method:** Check which @radix-ui/* packages and versions are installed. Compose Root, Trigger, Portal, Content and Item as specified by the component documentation; handle asChild only where supported. Style via data-state and semantic theme tokens.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not substitute Radix Themes component props for primitives. Verify focus management, accessible names, portal stacking and SSR/hydration around overlays.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.

## V2 local expertise — open only the applicable leaf

- [Dialog, Dropdown Menu, Popover, Tooltip, Select, Tabs, Slot — implementation patterns](references/component-patterns.md) — **read when** implementing or debugging Dialog, Dropdown Menu, Popover and component anatomy, behavior, controlled state.
- [Integration, theming and regression checks](references/integration-and-verification.md) — **read when** integrating radix-primitives with SSR, forms, themes, upgrades, tests or app delivery.

For ordinary tasks, this `SKILL.md` is sufficient to choose the next action. **Do not bulk-load both leaves** unless the request genuinely spans implementation and integration. A skill available in the catalog is not permission to install its package.
