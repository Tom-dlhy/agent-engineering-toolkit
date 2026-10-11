# radix-primitives — integration, theming and regression playbook

**Read when:** enabling radix-primitives in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Use Radix headless accessible primitives when you own CSS/theme and need composable React interaction patterns.

Official reference: https://www.radix-ui.com/primitives/docs/overview/introduction . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Overlay and navigation correctness
For Dialog, test modal vs nonmodal behavior, focus containment, escape, outside click, scroll locking and focus restoration. For Dropdown Menu and Select, keep correct `Item` IDs and keyboard roving navigation; never implement only hover interactions. CSS selectors often use `data-state`, `data-side` and `data-disabled`; these are library-specific. Controlled vs uncontrolled `open` / `defaultOpen` affects hydration and URL synchronization.
Inspect whether project uses consolidated `radix-ui` exports or per-primitive packages; copy imports only for the installed version. In shadcn-generated code the public component API may add wrappers or differ from raw Radix.

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
