---
name: react-native-paper
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing React Native Paper components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# React Native Paper — provider-specific UI engineering

**Best fit:** Material-aligned React Native and Expo applications.
**Target stack:** React Native, Expo, TypeScript.
**Official documentation:** https://callstack.github.io/react-native-paper/

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** PaperProvider, Button, TextInput, Dialog, Portal, Menu, DataTable, Snackbar.

**Provider-specific method:** Check Paper major version and required peer dependencies. Initialize PaperProvider with Material theme; prefer components’ mode/variant and accessibility props and RN-safe layout rather than web CSS.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not introduce DOM elements or Tailwind web-only classes. Test iOS/Android keyboard, safe areas, portals and dark-mode theme.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.
 
## Progressive expertise V2

- [Native widget and component patterns](references/component-patterns.md) — **read when** implementing PaperProvider, Button, TextInput, Dialog, Snackbar, DataTable or troubleshooting native interaction.
- [Runtime integration and validation](references/integration-and-verification.md) — **read when** configuring theme, SDK/build, native platform, accessibility, performance or upgrades.

Use only the relevant local leaf. Native and web APIs must **not** be assumed interchangeable; run actual device checks when possible.

## Current provider contract and visual identity

React Native Paper version, peer dependencies and PaperProvider Material 3 theme must align; touch targets, screen-reader labels and Text scaling are native, not browser CSS. Preserve product palette and safe areas. https://callstack.github.io/react-native-paper/
For product visual direction route to `frontend-design`; this skill owns toolkit composition, version matching, native accessibility and controlled states. Verify on intended devices, not only web-like demos.
