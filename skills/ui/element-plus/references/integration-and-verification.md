# element-plus: integration, styling and verification

**Read when:** wiring element-plus to the application build, themes, SSR/native runtime, state, i18n or deployment. Not needed for an unrelated component library.

## Stack and setup

The installed version and the project's lockfile determine actual APIs, dependencies and theming. Official docs: https://element-plus.org/en-US/ . Check runtime and framework versions together; confirm packages are supported rather than assuming backward compatibility. Document any extra icon, CSS, plugin, form or animation dependencies before installation.

## Provider-specific integration decisions

### Component registration and CSS
Check global registration vs on-demand auto-import with resolver; do not both register everything and individually bundle without a reason. Load Element Plus CSS and icon dependencies in the correct order. For Nuxt, determine the compatible integration approach and avoid duplicate plugin providers.
Configure `ElConfigProvider` for locale, size, namespace and z-index where needed. Check date/time locale, timezone, pagination total, Select value types and popper teleport target. Test dialog forms with validation errors, keyboard Escape, status announcements and SSR-only hydration. Avoid targeting internal class names without checking theme variables and component APIs.

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
