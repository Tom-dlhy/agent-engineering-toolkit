# heroui — integration, theming and regression playbook

**Read when:** enabling heroui in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Use a styled React kit with integrated component styling; confirm installed package generation and styling engine before writing examples.

Official reference: https://www.heroui.com/docs . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Production component workflows
1. Identify the exact HeroUI package family and major version; inspect provider requirements, CSS/Tailwind plugin or theme configuration.
2. For `Select`/`Autocomplete`, decide controlled selection collection and async list loading/empty state.
3. For `Table`, decide server pagination vs client collections, sorting state and keyboard row selection; ensure accessible headings.
4. For `Modal` document dismissal and submit state while network requests are pending; prevent accidental double writes.
Test focus, data-disabled, overflow on small viewports, dark theme, and translations. Validate components against the installed docs; the name HeroUI does not guarantee API equivalence between major versions.

## Regression contract by family

| Family | Positive behavior | Failure/edge that must be checked |
|---|---|---|
| Form fields / selection | Correct label, value, validation and submission | Invalid input, blur/touched, async options, long localized labels |
| Dialog / popover / menu | Trigger opens; Escape/dismiss; focus restored; stacking correct | Nested overlay, scroll, mobile viewport, disabled trigger |
| Table / grid | Stable row identity and pagination/sorting | Empty/loading/error, slow query, stale result, keyboard navigation |
| Theme / styling | Tokens, focus ring, light/dark and disabled contrast | SSR style flash, missing CSS, global reset conflict, forced-colors |
| Dynamic import / SSR | Hydration/portal uses the documented client boundary | Server render mismatch, mounted/unmounted focus and event leaks |

## Upgrade and release strategy

1. Inspect changelog and versioned migration guide **before** changing a major version.
2. Inventory currently used component names and wrappers; identify renamed slots/props, styling engine or CSS integration.
3. Reproduce representative views in an isolated branch; upgrade and use official codemods only after reviewing diff.
4. Validate typecheck/build, integration tests, accessibility keyboard paths and visual comparisons under light/dark/mobile.
5. If no browser or target runtime is available, explicitly report what was not exercised; do not claim full accessibility verification.

## Verification output

Record: package version and relevant official page, configuration change, screenshots/tests actually run, residual compatibility risk and rollback path.
