# primeng: component mechanisms and patterns

**Read when:** implementing or debugging p-table, p-dialog, p-select, p-form. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://primeng.org/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — primeng

### PrimeNG API and lazy data
The installed PrimeNG major version controls whether components are imported standalone, how themes are provided and whether newer names like `Select` apply. Examine current imports rather than adapting a PrimeReact example.
```ts
import { TableModule } from 'primeng/table';
// Register TableModule in the component's imports for the installed Angular version.
```
For `p-table`, wire lazy paging/sorting/filtering to backend using configured event and stable `dataKey`. Manage loading and total record counts explicitly. For forms, use Angular Reactive Forms and appropriate value accessor integration; field templates do not imply server validation.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
