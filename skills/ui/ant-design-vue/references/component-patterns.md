# ant-design-vue: component mechanisms and patterns

**Read when:** implementing or debugging a-form, a-form-item, a-table, a-select, a-modal. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://www.antdv.com/components/overview ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — ant-design-vue

### Vue binding differs from React Ant Design
Ant Design Vue uses Vue `v-model:value` or equivalent component-specific contract—not React's `Form.useForm()` exactly. Confirm current Vue/package major version and the exact v-model prop/event pair per component.
```vue
<script setup lang="ts">
import { reactive } from 'vue'
const values = reactive({ email: '' })
</script>
<template>
  <a-form :model="values" layout="vertical">
    <a-form-item label="Email" name="email" :rules="[{ required: true, type: 'email' }]">
      <a-input v-model:value="values.email" />
    </a-form-item>
  </a-form>
</template>
```
For Table, `rowKey`, remote sorting/pagination and selection update contracts must be explicit. Do not assume form reset reacts to initial model mutations automatically.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
