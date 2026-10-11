---
name: chakra-ui
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Chakra UI components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Chakra UI — provider-specific UI engineering

**Best fit:** token-based React design systems and composable recipes.
**Target stack:** React, TypeScript and supported server-rendered React frameworks.
**Official documentation:** https://chakra-ui.com/docs

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** Button, Dialog, Menu, Tabs, Table, Field, Select, Combobox, Toast.

**Provider-specific method:** Identify Chakra major version and the installed styling system. Use version-matched snippets, recipes, semantic tokens and provider setup. Verify compound component anatomy from docs, especially for Dialog, Select and Ark-based pieces.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Chakra v2 and v3 APIs are not interchangeable. Avoid layering incompatible Tailwind assumptions or copying deprecated prop names.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.

## V2 local expertise — open only the applicable leaf

- [Button, Dialog, Menu, Select, Field, Table — implementation patterns](references/component-patterns.md) — **read when** implementing or debugging Button, Dialog, Menu and component anatomy, behavior, controlled state.
- [Integration, theming and regression checks](references/integration-and-verification.md) — **read when** integrating chakra-ui with SSR, forms, themes, upgrades, tests or app delivery.

For ordinary tasks, this `SKILL.md` is sufficient to choose the next action. **Do not bulk-load both leaves** unless the request genuinely spans implementation and integration. A skill available in the catalog is not permission to install its package.

## Current provider contract and visual identity

Chakra v3 replaces several v2 props and component shapes with compound parts/recipes; provider and theme changed. Check v2-v3 before applying CLI snippets or migrating. Official: https://chakra-ui.com/docs/get-started/migration
For **art direction**, activate the existing `frontend-design` skill; this library skill owns exact props, composition, states, version compatibility and accessibility. Do not ship the stock demo skin or force visual novelty contrary to the product brief.
