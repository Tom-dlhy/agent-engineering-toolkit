# primereact — component engineering and APIs

**Read when:** implementing DataTable, Column, Dialog, Dropdown/Select, TreeTable or debugging a behavior/prop contract with primereact. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Choose PrimeReact for advanced data components; confirm legacy vs current theming and component naming before implementation.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://primereact.org/ . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### DataTable is a state machine
Define row identity via `dataKey` (when supported), selection state, server lazy loading and sort/filter contracts. In lazy mode, `onPage`, `onSort` and `onFilter` must query backend; a visual paginator does not paginate remote data automatically.
```tsx
import { DataTable } from 'primereact/datatable'
import { Column } from 'primereact/column'
function Orders({ rows }: { rows: { id: string; total: number }[] }) {
  return <DataTable value={rows} dataKey="id" paginator rows={10}>
    <Column field="id" header="Order" />
    <Column field="total" header="Total" />
  </DataTable>
}
```
Check API/current package: PrimeReact has evolving styled/unstyled and v10/v11 patterns.

## Component decision / execution playbook

1. **Choose component anatomy:** consult the exact package's current part/slot composition; make no substitution across primitive vendors.
2. **Model state:** document value, input/selected/open distinction; controlled vs uncontrolled; keyboard/disabled/error/loading; how async data changes state.
3. **Implement inside existing system:** reuse installed wrappers, tokens, typography, form validation and router, avoiding a new package where supported primitives suffice.
4. **Validate behavior:** test mouse, keyboard, screen reader, narrow screen, non-English strings and pending network state; record incorrect semantics and fix.
5. **Inspect negative paths:** empty/no-results, invalid selection, two quick submits, close while pending, focus after unmount and hydration.

## Anti-patterns

- Copying snippets across different major versions or framework bindings.
- Treating a visual state as adequate accessibility; missing keyboard/focus or label semantics.
- Mixing primitive systems and their slot conventions without reviewing refs/events.
- Changing the global theme merely to fix a single component; choose nearest coherent scope.

## Exit evidence

Identify inspected package version and source file, positive and negative tests run, unsupported scenarios and documentation source. Do not assert official API details from memory when the installed version is unknown.
