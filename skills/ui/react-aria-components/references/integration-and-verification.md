# react-aria-components — integration, theming and regression playbook

**Read when:** enabling react-aria-components in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Favor rich accessibility, focus semantics, keyboard interactions and internationalization; styling remains the application's responsibility.

Official reference: https://react-spectrum.adobe.com/react-aria/components.html . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Keyboard and locale guarantees
Decide between native-looking/select behavior and custom collection navigation. Test Tab, arrow movement, Home/End, typing/typeahead, selected/disabled entries, focus restoration and screen-reader announcements. For overlays understand `OverlayArrow`, modality, portal and dismissal rules in current docs.
Use React Aria's localization hooks and locale-sensitive behavior for RTL, dates and number formatting; don't assume translating visible labels is enough.
When integrating form libraries, choose controlled value/key and preserve field error messages and label semantics. Test actual browser/device combinations for date/time inputs and virtualized collections.

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
