# primevue: integration, styling and verification

**Read when:** wiring primevue to the application build, themes, SSR/native runtime, state, i18n or deployment. Not needed for an unrelated component library.

## Stack and setup

The installed version and the project's lockfile determine actual APIs, dependencies and theming. Official docs: https://primevue.org/ . Check runtime and framework versions together; confirm packages are supported rather than assuming backward compatibility. Document any extra icon, CSS, plugin, form or animation dependencies before installation.

## Provider-specific integration decisions

### Theme and forms
Determine styled vs unstyled mode and PrimeVue theme presets **for the version actually installed**. Global theme changes can affect CSS layer ordering and conflict with Tailwind; inspect pass-through (PT) API for slot customization rather than relying on DOM structure.
For forms, decide native `v-model`, `@primevue/forms` if present, or existing application validation; field error display needs association with input. For Dialog check focus restoration and responsive breakpoints. For DatePicker and Select, test model values, locale, timezone and disabled options. Different PrimeVue releases expose different imports/options—do not use v4 patterns against v3.

## Mandatory acceptance matrix

| Behavior | What to verify |
|---|---|
| Static rendering | Typecheck/build, CSS loaded, no duplicate providers, no blank controls |
| Interactive | pointer/touch/keyboard, disabled state, Escape/outside focus and return |
| Async and validation | pending state, cancellation/stale response, form error and duplicate submit |
| Accessibility | labels, semantic structure, status announcement, focus ring, contrast and screen reader |
| Responsive/i18n | narrow overflow, translated labels, RTL where supported, safe-area/mobile if relevant |
| Platform/version | SSR hydration or native runtime, major upgrade compatibility and documented rollback |

## Safe migration workflow

Inventory installed components and public props/slots; read versioned changelog; migrate one representative form, dialog and data view first. Run typecheck, unit/integration tests and a real browser/device audit. Treat accessibility and runtime verification as **not performed** unless explicitly exercised. Do not execute installation or production deployment merely because this document lists a recipe.

## Release notes to report

Version inspected; configuration/files touched; docs checked; tests actually executed; unsupported behavior and next verification needed. External vendor docs are for version freshness, not the only technical substance of this leaf.

## 2026 provider-specific release and visual-fidelity addendum

### PrimeVue 4 styling architecture
PrimeVue 4 styled mode separates component CSS base and preset tokens. The preset has primitive/semantic/component token tiers. Unstyled mode omits the supplied CSS rules/tokens and expects the application styling system; do not install styled mode and then assume Tailwind-only slots or copy v3 SASS theme instructions. For DataTable confirm lazy pagination/filter callback and loading/selection with stable identifiers. Product art direction should be expressed by a coherent preset and component overrides, not one-off colored cards copied from samples. Validate dark contrast, overlay portal, keyboard/ARIA, SSR CSS output. Docs: https://v4.primevue.org/theming/styled/ ; https://v4.primevue.org/theming/unstyled/ .

**Evidence boundary:** documentation is not a real app build; verify against the pinned installed release and record browser/device tests run. Distinctiveness is evaluated against real brand/content, not automated detection of AI authorship.
