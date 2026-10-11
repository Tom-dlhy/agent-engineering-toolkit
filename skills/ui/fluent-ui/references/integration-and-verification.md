# fluent-ui — integration, theming and regression playbook

**Read when:** enabling fluent-ui in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Use Fluent UI v9 React when Microsoft design semantics and enterprise keyboard accessibility align with the product.

Official reference: https://react.fluentui.dev/ . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Grids and tokens
For Fluent DataGrid, read the installed hooks/columns/selection API; distinguish it from the HTML table or the older DetailsList v8. Implement stable row IDs and navigation semantics. For Combobox, test freeform vs option selection and keyboard announcements.
Use semantic Fluent tokens and theme palettes in a provider; avoid assuming global CSS overrides will reliably win over Griffel styles. Verify RTL, keyboard, focus and high-contrast OS settings.
For migration from v8, inventory old `Stack`, `DetailsList`, `CommandBar` and styling system before replacing with v9 components; mixing versions increases bundle size and maintenance cost.

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
