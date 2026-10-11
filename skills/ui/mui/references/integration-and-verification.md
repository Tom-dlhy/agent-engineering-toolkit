# mui — integration, theming and regression playbook

**Read when:** enabling mui in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Use MUI Material core for Material Design and enterprise React; advanced Data Grid/Pickers live in MUI X with separate packages and licensing.

Official reference: https://mui.com/material-ui/getting-started/ . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Forms, dialogs and tables
For TextField + Autocomplete, keep separate `value` and `inputValue` states when required; do not treat free-text search and selected option as the same state. With DataGrid, use stable `getRowId`, memoized column definitions and distinguish client/server sort/filter/pagination (real backend integration must own total row count). Check commercial MUI X tier **before** using premium features.
For Dialog, make `open` controlled, connect label/description and focus restoration. For DatePicker, configure LocalizationProvider and a supported date adapter; validate timezone and controlled value shape. Smoke-test under the actual SSR engine and styled engine version.

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
