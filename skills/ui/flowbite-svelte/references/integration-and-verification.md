# flowbite-svelte: integration, styling and verification

**Read when:** wiring flowbite-svelte to the application build, themes, SSR/native runtime, state, i18n or deployment. Not needed for an unrelated component library.

## Stack and setup

The installed version and the project's lockfile determine actual APIs, dependencies and theming. Official docs: https://flowbite-svelte.com/ . Check runtime and framework versions together; confirm packages are supported rather than assuming backward compatibility. Document any extra icon, CSS, plugin, form or animation dependencies before installation.

## Provider-specific integration decisions

### Tailwind and SvelteKit
Check Tailwind 3 vs 4 configuration and Flowbite Svelte plugin styles/content scanning. Avoid installing plain Flowbite JS runtime for Svelte components without need. For themes, use supported customization or tokens so focus/hover/error styles stay coherent across components.
For navigation, ensure SvelteKit link semantics and keyboard dropdown support; use native anchors for navigation and buttons for actions. SSR must render compatible DOM before hydration; browser globals belong in `onMount` as appropriate.
Test mobile navbar collapse, dialog Escape/focus, long translated strings and form error announcements. Confirm all relevant CSS is present in production build.

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
