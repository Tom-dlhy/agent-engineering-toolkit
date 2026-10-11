# primevue: component mechanisms and patterns

**Read when:** implementing or debugging DataTable, Column, Dialog, Select, AutoComplete. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://primevue.org/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — primevue

### PrimeVue plugin and DataTable
PrimeVue has a plugin/configuration model and major-version differences (e.g. v3 → v4 styling and component naming). Inspect the installed version before choosing `Dropdown` versus `Select`. Keep `DataTable` row identity through `dataKey`; pagers can be client-mode or lazy remote mode.
```vue
<script setup lang="ts">
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
defineProps<{ rows: { id: string; amount: number }[] }>()
</script>
<template>
  <DataTable :value="rows" dataKey="id" paginator :rows="10">
    <Column field="id" header="ID" />
    <Column field="amount" header="Amount" />
  </DataTable>
</template>
```
With server-backed tables, wire lazy pagination/filter/sort events to backend queries and cancellation instead of slicing an incomplete page of data.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
