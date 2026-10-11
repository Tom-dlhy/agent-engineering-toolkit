---
name: gluestack-ui
domain: ui
version: "0.1.0"
description: >-
  Use when implementing, integrating, debugging or reviewing gluestack-ui components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# gluestack-ui — provider-specific UI engineering

**Best fit:** open-code React Native/Expo components with NativeWind-style customization.
**Target stack:** Expo, React Native, TypeScript, NativeWind.
**Official documentation:** https://gluestack.io/ui/docs/home/overview/introduction

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** Button, Input, FormControl, Dialog/AlertDialog, Select, Actionsheet, Toast.

**Provider-specific method:** Identify installed gluestack generation, component CLI and NativeWind configuration. Review copied component source, accessibility and styling while keeping variants and tokens consistent across components.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not treat gluestack UI as an immutable npm-only black box or copy web shadcn DOM patterns. Confirm NativeWind, Expo and version compatibility.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.
