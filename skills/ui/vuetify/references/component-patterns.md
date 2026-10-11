# vuetify: component mechanisms and patterns

**Read when:** implementing or debugging VApp, VMain, VForm, VDialog, VDataTable. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://vuetifyjs.com/en/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — vuetify

### Vue application anatomy
Vuetify relies on an application plugin and a layout hierarchy. The `v-app` root establishes layout context; `v-main` manages space against app bars/drawers. Dropping these wrappers can produce overlaps even if the component itself renders.
In Vue SFCs use explicit `v-model` for Dialog and controlled inputs; `v-form` rules and `validate()` are not identical to external Zod/Yup validation. For `v-data-table`, decide local vs server-backed pagination and stable item keys, and verify the correct component variant for your installed version.
```vue
<template>
  <v-app><v-main>
    <v-dialog v-model="open" max-width="480">
      <v-card title="Edit record">
        <v-card-actions><v-btn @click="open = false">Close</v-btn></v-card-actions>
      </v-card>
    </v-dialog>
    <v-btn @click="open = true">Edit</v-btn>
  </v-main></v-app>
</template>
<script setup lang="ts">
import { ref } from 'vue'
const open = ref(false)
</script>
```
Check auto-import/plugin conventions before using global tags.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
