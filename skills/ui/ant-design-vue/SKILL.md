---
name: ant-design-vue
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Ant Design Vue components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Ant Design Vue — provider-specific UI engineering

**Best fit:** Ant Design conventions in enterprise Vue apps.
**Target stack:** Vue 3, TypeScript, Nuxt or Vite.
**Official documentation:** https://www.antdv.com/components/overview

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** a-form, a-table, a-select, a-tree, a-date-picker, a-modal, a-upload.

**Provider-specific method:** Check ant-design-vue major version and Vue 3 support. Follow Vue template slots, v-model bindings, locale, design tokens and table pagination conventions from Vue-specific docs.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not import React Ant Design Form APIs or assume identical component props. Verify SSR styles and server-driven table state.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.
 
## Progressive expertise V2 — route instead of bulk-loading

- [Component mechanisms and patterns](references/component-patterns.md) — **read when** implementing a-form, a-form-item, a-table, a-select, a-modal, props/bindings, focus, state or interaction.
- [Integration, styling and verification](references/integration-and-verification.md) — **read when** configuring the library, SSR/native platform, themes, upgrades or testing.

Read only the needed leaf, in addition to the activated SKILL.md. Do not infer API compatibility from similar React/Vue/Angular/Svelte packages. A provider is opt-in and not automatically installed.
