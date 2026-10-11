---
name: flutter-material
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Flutter Material components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Flutter Material — provider-specific UI engineering

**Best fit:** Flutter Material Design across mobile, web and desktop.
**Target stack:** Flutter, Dart, Android, iOS, desktop, web.
**Official documentation:** https://docs.flutter.dev/ui/widgets/material

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** MaterialApp, ThemeData, Scaffold, AppBar, FilledButton, TextField, NavigationBar, DataTable, Dialog.

**Provider-specific method:** Inspect Flutter/Dart SDK channel and Material 2 versus Material 3 settings. Compose widgets using theme extensions and state management already chosen by the project; honor constraints and adaptive layouts.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not create side effects in build(), duplicate global theme tokens or assume web-only gestures are native-friendly. Test semantics, text scaling and platform back navigation.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.
 
## Progressive expertise V2

- [Native widget and component patterns](references/component-patterns.md) — **read when** implementing MaterialApp, ThemeData, Scaffold, Form, TextFormField, ListView or troubleshooting native interaction.
- [Runtime integration and validation](references/integration-and-verification.md) — **read when** configuring theme, SDK/build, native platform, accessibility, performance or upgrades.

Use only the relevant local leaf. Native and web APIs must **not** be assumed interchangeable; run actual device checks when possible.

## Current provider contract and visual identity

Flutter Material design version and Flutter SDK/ThemeData useMaterial3 selection must be verified; honor native semantics, adaptive navigation and text scaling. A default color-scheme widget gallery is not a finished branded app. https://docs.flutter.dev/ui/widgets/material
For product visual direction route to `frontend-design`; this skill owns toolkit composition, version matching, native accessibility and controlled states. Verify on intended devices, not only web-like demos.
