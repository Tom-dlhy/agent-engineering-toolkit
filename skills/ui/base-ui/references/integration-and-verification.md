# base-ui — integration, theming and regression playbook

**Read when:** enabling base-ui in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Choose unstyled React behavior; the application must own visual styling, state attributes and interaction composition.

Official reference: https://base-ui.com/react/overview/quick-start . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Deep interaction contract
For Dialog/Menu/Select inspect parts `Root`, `Trigger`, `Portal`, `Positioner`, `Popup` and closing behavior in the version's official page. Decide whether state is controlled by URL, parent state or primitive. Check when focus moves into overlay and returns; test escape/outside interaction in nested overlays.
For custom field components, preserve `aria-describedby`, error state, label association, ref forwarding and focus-visible styles. Portals and virtualized lists can require SSR/hydration checks.
Track Base UI React version independently from shadcn/ui generated components; do not assume the current docs match an older installed copy.

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

### Verified package and composition contract
The current official package is `@base-ui/react`, including deep imports such as `@base-ui/react/menu`. The custom `render` element must **forward ref and spread props**; in function form, preserve handlers, roles, ids, aria attrs and state-specific data attributes. Nested triggers and custom buttons need a test that no nested native `<button>` results. Base UI is headless: accessible behavior comes from library, art direction from owned CSS/tokens. The design must visibly distinguish focus, selected, disabled, invalid, expanded and destructive operations. Run tab/arrow/Escape, focus return and screen-reader tests in a real browser after changing render anatomy. Docs: https://base-ui.com/react/handbook/composition .

**Evidence boundary:** documentation is not a real app build; verify against the pinned installed release and record browser/device tests run. Distinctiveness is evaluated against real brand/content, not automated detection of AI authorship.
