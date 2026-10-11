---
name: primevue
domain: ui
version: "0.1.0"
description: >-
  Use when implementing, integrating, debugging or reviewing PrimeVue components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# PrimeVue — provider-specific UI engineering

**Best fit:** data-heavy Vue applications with theme and unstyled support.
**Target stack:** Vue, Nuxt, TypeScript.
**Official documentation:** https://primevue.org/

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** DataTable, TreeTable, Dialog, Form, Select, DatePicker, FileUpload, VirtualScroller.

**Provider-specific method:** Inspect PrimeVue major version and plugin registration. Select styled or unstyled mode intentionally; use component templates, pass-through props and lazy/virtualized table facilities where appropriate.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

PrimeVue component naming and theme configuration have changed across majors. Do not copy PrimeReact examples directly into Vue.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.
