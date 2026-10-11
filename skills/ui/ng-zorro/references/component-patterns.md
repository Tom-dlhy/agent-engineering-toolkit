# ng-zorro: component mechanisms and patterns

**Read when:** implementing or debugging nz-table, nz-form, nz-modal, nz-select, nz-tree. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://ng.ant.design/docs/introduce/en ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — ng-zorro

### Ant Design for Angular
NG-ZORRO uses Angular DI, reactive forms and `nz-*` directives/modules. Its controls are not `antd` React controls or Ant Design Vue wrappers.
```ts
import { NzTableModule } from 'ng-zorro-antd/table';
import { NzButtonModule } from 'ng-zorro-antd/button';
// Put modules in the Angular component imports or the owning module.
```
For `nz-table`, make client/server paging explicit; current component API defines front-end vs server-side flags/events. For forms, use `FormGroup` and corresponding nz-form directives, and show validation errors from Angular control state.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
