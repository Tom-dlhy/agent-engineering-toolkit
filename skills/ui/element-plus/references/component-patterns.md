# element-plus: component mechanisms and patterns

**Read when:** implementing or debugging ElForm, ElFormItem, ElTable, ElDialog, ElSelect. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://element-plus.org/en-US/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — element-plus

### Vue model contracts
Element Plus form validation uses Form/FormItem props, model object and explicit rules. Nested paths, array fields and FormItem `prop` names must match the underlying model. Dialog visibility is managed via `v-model`; define opening/closing state outside dialogs that unmount.
```vue
<script setup lang="ts">
import { reactive, ref } from 'vue'
const open = ref(false)
const form = reactive({ email: '' })
</script>
<template>
  <el-button @click="open = true">Edit</el-button>
  <el-dialog v-model="open" title="Edit">
    <el-form :model="form">
      <el-form-item label="Email" prop="email"><el-input v-model="form.email" /></el-form-item>
    </el-form>
  </el-dialog>
</template>
```
For ElTable use `row-key` whenever selection/tree expansion requires stable identity; preserve sort/filter and loading semantics for server data.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
