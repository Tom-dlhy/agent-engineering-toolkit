# UI library replacement and representative component proof

Read when: explicitly requested to migrate component provider, when library version becomes unsupported, or when evaluating a candidate against an installed, functioning library.

## Default is preserve, then prove
List actual installed provider components, theme tokens, app layout/layout shift behavior, forms/validation libraries and current modified vendor files. Do not recommend a migration solely because the upstream default or aesthetic trend changed. Clarify what functionality or maintenance/security problem motivates it.

### Representative proof-of-concept
~~~yaml
app: real framework and pinned version
components:
  - form with async validation and recovery
  - dialog/popover with escape, outside click and focus restore
  - navigation menu usable with keyboard and screen reader
  - data view with sorting/empty/loading or accessible basic table
  - light/dark/high-contrast surfaces with brand tokens
environments: [narrow-screen, desktop, SSR-hydration]
must_fail: [missing_label, invalid_submit, duplicate_submit, inaccessible_focus]
~~~
A small proof in sandbox is better than copying the full library catalog into a project. Tests must use the selected actual library and installed version; don't invent providers' prop contracts from memory.

## Migration cost inventory
- Source and imports: wrappers, JSX slots, trigger APIs, events, controlled state.
- Theme: CSS variable semantics, type scales, dark and forced colors.
- Interaction: keyboard focus, overlays, portals, aria, screen reader.
- Data: DataGrid model, virtualization, pagination, selection/row IDs, license tiers.
- Runtime: RSC/SSR, CSS extraction, tree shaking, bundle size on production build.
- Testing: snapshots/browser flows, visual regressions and localization/RTL.
- Exit: ability to roll back safely, coexistence boundaries if temporary and approved.

## Risk mitigation
Incrementally change a single component family in a feature branch, preserve existing tokens unless redesign separately approved, test real mobile/tablet and assistive technology where available, then budget follow-up migration. Never blindly run a CLI `add --overwrite` on source-owned customized files. Provider selection is advisory; installation requires explicit authorization.

References: https://ui.shadcn.com/docs/changelog/2026-01-base-ui and https://mui.com/x/react-data-grid/ and https://www.w3.org/WAI/test-evaluate/
