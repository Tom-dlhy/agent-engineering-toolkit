# chakra-ui — integration, theming and regression playbook

**Read when:** enabling chakra-ui in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Build token-driven React UI with Chakra's slot recipes; version-check v2 vs v3 architecture.

Official reference: https://chakra-ui.com/docs . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Components and accessibility
For `Dialog` inspect current `Dialog.Root`, `Dialog.Trigger`, `Dialog.Content` and portal patterns; confirm `asChild` and slot behavior in installed release. For `Field` wire label, helper/error text and invalid state.
For `Select` distinguish native select from collection-based primitives; assess form integration and keyboard controls before replacing a native `<select>`.
Review providers, SSR color mode and token layering. Test focus trapping, field invalid announcements, disabled state, responsive prop behavior and system dark mode. Document any migration from v2 explicitly rather than relying on codemods blindly.

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

## 2026 provider-specific release and visual-fidelity addendum

### Migration gate for v2 → v3
Do not copy Chakra v2 `isOpen`, `isDisabled`, `colorScheme` and flat component anatomy into Chakra v3. Official migration guidance uses `open`, `disabled`, `colorPalette`, compound component parts, recipes and new `ChakraProvider value={system}` conventions. The docs suggest codemod `--dry` before mutation; a codemod is not permission to rewrite a production project. Snippets copied by the CLI are source-owned and should be reviewed for design tokens, keyboard/ARIA, dialog portals and hydration under existing color-mode provider. Verify theme semantic pairs under both modes and a complex form before deploying. Docs: https://chakra-ui.com/docs/get-started/migration .

**Evidence boundary:** documentation is not a real app build; verify against the pinned installed release and record browser/device tests run. Distinctiveness is evaluated against real brand/content, not automated detection of AI authorship.
