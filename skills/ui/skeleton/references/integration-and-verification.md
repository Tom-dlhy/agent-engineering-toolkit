# skeleton: integration, styling and verification

**Read when:** wiring skeleton to the application build, themes, SSR/native runtime, state, i18n or deployment. Not needed for an unrelated component library.

## Stack and setup

The installed version and the project's lockfile determine actual APIs, dependencies and theming. Official docs: https://www.skeleton.dev/ . Check runtime and framework versions together; confirm packages are supported rather than assuming backward compatibility. Document any extra icon, CSS, plugin, form or animation dependencies before installation.

## Provider-specific integration decisions

### Theme configuration and compatibility
Record installed Skeleton generation, framework plugin, component import paths and chosen theme. Decide whether styling is implemented through CSS custom properties, Tailwind layers or generated theme files for that version; theme tokens must align with product branding.
For SvelteKit, verify SSR/hydration and platform/browser-only code. For dark mode, prevent initial appearance flash and respect system preference with explicit persistence rules. Inspect overlay stacking, drawers, accessibility and responsive app-shell behavior.
Test two representative forms, navigation, modal and dense screen in both light and dark. Document migration from legacy `@skeletonlabs/skeleton` separately rather than assuming drop-in compatibility.

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
