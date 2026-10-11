---
name: vuetify
domain: ui
version: "0.1.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Vuetify components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Vuetify — provider-specific UI engineering

**Best fit:** complete Material-style Vue applications.
**Target stack:** Vue, Nuxt, TypeScript.
**Official documentation:** https://vuetifyjs.com/en/

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** v-app, v-data-table, v-form, v-dialog, v-autocomplete, v-select, v-navigation-drawer.

**Provider-specific method:** Confirm Vue and Vuetify major versions. Set up createVuetify, application root, themes, icons, locale and tree-shaking according to the installed toolchain; use v-model and Vuetify validation conventions.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not mix Vue 2/Vuetify 2 patterns into Vue 3 projects. Check SSR/Nuxt integration and the license/status of advanced components.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.
