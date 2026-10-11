# shadcn-ui — integration, theming and regression playbook

**Read when:** enabling shadcn-ui in an application, migrating its major version, configuring styling, SSR/native lifecycle or validating completed UI. Not required for a static, unrelated change.

## Setup and boundaries

Treat shadcn as source-owned code, not a sealed package: inspect components.json, aliases, Tailwind setup, styles and the installed component files before using registry examples.

Official reference: https://ui.shadcn.com/docs . Inspect package lockfile, framework build plugin, root providers, CSS entrypoints, user-selected design tokens and installed wrapper components. Avoid installing dependencies or upgrading the framework as a side effect of a component change.

## Integration and operational details

### Component construction workflow
1. Inspect and reuse local UI implementation; inspect installed utility `cn()`/class variance variant conventions.
2. Decide controlled state for Dialog/Select when external navigation, form resets or URL state matter.
3. Compare registry base and installed component source before choosing composition props; avoid duplicate `DialogTrigger` or nested interactive elements.
4. Add only missing component files after reviewing dry-run and diff; preserve local overrides, CSS vars and icons.
5. Test focus restoration/escape, form error association, dark tokens, mobile Sheet overflow and hydration.

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

### Source-owned registry upgrade and brand QA
The maintained upstream shadcn skill is an appropriate **reference**, not an executable dependency. Use local `components.json`, component source and CLI diff to decide between Radix `asChild` and Base UI `render`. Never apply code examples from the wrong base. Semantic `--primary` / `--primary-foreground` and other pairs in `:root`/`.dark` drive consistent foreground/background contrast, not an arbitrary radial gradient layer for every card. Before accepting a visually generic generated screen, identify product content and layout hierarchy, adjust typography and spacing without compromising Button/Dialog/Select refs, and inspect one long form plus table and modal with keyboard. Docs: https://ui.shadcn.com/docs/theming ; https://github.com/shadcn-ui/ui/blob/main/skills/shadcn/rules/base-vs-radix.md .

**Evidence boundary:** documentation is not a real app build; verify against the pinned installed release and record browser/device tests run. Distinctiveness is evaluated against real brand/content, not automated detection of AI authorship.
