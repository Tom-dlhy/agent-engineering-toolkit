# bits-ui: integration, styling and verification

**Read when:** wiring bits-ui to the application build, themes, SSR/native runtime, state, i18n or deployment. Not needed for an unrelated component library.

## Stack and setup

The installed version and the project's lockfile determine actual APIs, dependencies and theming. Official docs: https://bits-ui.com/docs/introduction . Check runtime and framework versions together; confirm packages are supported rather than assuming backward compatibility. Document any extra icon, CSS, plugin, form or animation dependencies before installation.

## Provider-specific integration decisions

### SSR and focused interaction
In SvelteKit, component DOM/portal work must respect server rendering and hydration; do not read `window` at module import. Style documented data-state attributes for open/checked/disabled, avoiding brittle DOM descendants.
For combobox remote search, separate query and selected value, debounce/cancel requests and handle empty results. For Dialog test focus scope, return, escape and mobile scroll locking. Check disabled state is truly noninteractive.
Audit TypeScript prop contracts, SSR build and keyboard with actual browser/AT; standard project CSS stays the source of truth.

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

### Svelte 5 binding and headless contract
Bits UI official documentation targets Svelte 5; example `Accordion.Root` uses component-root/parts and Svelte-specific state semantics, not Radix React `asChild` or Svelte 4-only props. Confirm Svelte version and Bits generation before using snippets, validate the controlled/bindable state and keyboard behavior in the actual built SvelteKit app. Since primitives are unstyled, deliberate brand choices (semantic foreground, focus/invalid states, typography, dense/sparse layout) are required. Reusing Bits as a component layer must not alter app-owned actions/authorization on server. Docs: https://bits-ui.com/docs/getting-started .

**Evidence boundary:** documentation is not a real app build; verify against the pinned installed release and record browser/device tests run. Distinctiveness is evaluated against real brand/content, not automated detection of AI authorship.
