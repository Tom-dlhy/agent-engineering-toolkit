# ionic: integration, styling and verification

**Read when:** wiring ionic to the application build, themes, SSR/native runtime, state, i18n or deployment. Not needed for an unrelated component library.

## Stack and setup

The installed version and the project's lockfile determine actual APIs, dependencies and theming. Official docs: https://ionicframework.com/docs . Check runtime and framework versions together; confirm packages are supported rather than assuming backward compatibility. Document any extra icon, CSS, plugin, form or animation dependencies before installation.

## Provider-specific integration decisions

### Capacitor and platform delivery
Decide browser/PWA vs iOS/Android Capacitor build before choosing permissions, camera/files and authentication flows. Native plugins require platform entitlements and real-device testing; a desktop browser passing a mock is insufficient.
Check Ionic CSS core imports, platform mode (md/ios), theme variables, safe-area insets and dark mode. For navigation, test Android back button, iOS swipe back, nested tabs, deep links and resume. For forms check virtual keyboard avoidance and focus handling; for modals test backdrop dismissal and hardware back.
Use platform-specific security and permission prompts only after explicit user intent; do not assume Capacitor provides authentication/secure storage automatically.

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
