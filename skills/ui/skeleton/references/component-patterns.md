# skeleton: component mechanisms and patterns

**Read when:** implementing or debugging AppShell, Theme, Drawer, Modal, Navigation, Forms. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://www.skeleton.dev/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — skeleton

### Skeleton is a design system plus components
Skeleton library generations and supported frameworks have changed significantly. Detect `@skeletonlabs/*` package generation, Tailwind major and Svelte/React adapter before copying markup. A Skeleton class/primitive from a previous major release may not exist in the installed one.
Inspect app-shell and theme setup first, then adopt components consistent with that theme and styling API. Do not depend on incidental internal CSS classes; choose public token/recipe entry points.
For modal/drawer, validate focus and scroll behavior from the selected component package; older framework-level modal-store APIs must not be presumed current.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
