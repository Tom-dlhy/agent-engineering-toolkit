# angular-material: integration, styling and verification

**Read when:** wiring angular-material to the application build, themes, SSR/native runtime, state, i18n or deployment. Not needed for an unrelated component library.

## Stack and setup

The installed version and the project's lockfile determine actual APIs, dependencies and theming. Official docs: https://material.angular.dev/ . Check runtime and framework versions together; confirm packages are supported rather than assuming backward compatibility. Document any extra icon, CSS, plugin, form or animation dependencies before installation.

## Provider-specific integration decisions

### Angular CDK and data
Inspect Angular, Material, CDK and animation/theme versions together. For MatDialog, use injection/config for open/close and result handling; verify focus trap and route navigation cleanup. MatTable requires a deliberate data source; MatTableDataSource is not a universal server-pagination engine. Use MatSort/MatPaginator and an Observable/data source for remote paging.
Respect Angular's theme tooling for the installed M2/M3 generation, including typography/density and CSS style encapsulation. Test validators, async cancellation, role-based actions, focus after dialogs, screen readers and SSR/hydration support. Avoid mixing unrelated Angular component kits without an integration plan.

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
