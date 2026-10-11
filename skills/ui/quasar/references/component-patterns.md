# quasar: component mechanisms and patterns

**Read when:** implementing or debugging QLayout, QPage, QDialog, QTable, QForm. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://quasar.dev/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — quasar

### Quasar is more than a component pack
Choose Quasar as an application framework when you want its build, platform, routing, plugin and UI conventions. Detect Quasar CLI mode and app extensions; don't install it beside an unrelated Vue/Nuxt architecture without reason.
```vue
<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated><q-toolbar><q-toolbar-title>Dashboard</q-toolbar-title></q-toolbar></q-header>
    <q-page-container><q-page padding><q-btn color="primary" label="Save" @click="save" /></q-page></q-page-container>
  </q-layout>
</template>
<script setup lang="ts">
function save() { /* perform authorized action */ }
</script>
```
For QTable, choose pagination request mode if data is server-side; stable `row-key` and `@request` behavior matter. For forms use `QForm` validation explicitly.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
