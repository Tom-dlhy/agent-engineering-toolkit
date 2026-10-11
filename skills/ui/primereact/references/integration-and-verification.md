# primereact — integration, theming and regression playbook

**Read when:** enabling primereact in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Choose PrimeReact for advanced data components; confirm legacy vs current theming and component naming before implementation.

Official reference: https://primereact.org/ . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Data, forms and accessibility
For complex tables, define `dataKey`, page/sort/filter state and loading/empty/error separately. Implement server-side total counts, cancellation and stale-response suppression for lazy mode. Validate keyboard navigation and interactive cells: adding `onRowClick` does not make a table accessible by itself.
Understand theme modes (styled, unstyled, pass-through props) for the actual major release; CSS and token organization differ. If PrimeFlex or Tailwind is used, check cascade ordering rather than blindly adding resets.
Validate Dialog overlays, focus restoration, list virtualization and selection. Compare tree/large data components against license/support constraints when relevant.

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
