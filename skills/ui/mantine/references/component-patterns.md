# mantine — component engineering and APIs

**Read when:** implementing Button, Modal, Drawer, Select, Combobox, DataTable alternatives or debugging a behavior/prop contract with mantine. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use Mantine for application dashboards/forms and utility hooks; evaluate its built-in components and optional packages before adding another library.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://mantine.dev/ . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Mantine provider and compound components
Mount `MantineProvider` and import its stylesheet as required by the installed major version. For forms, investigate `@mantine/form`, `useForm` and compatibility with existing validation conventions.
```tsx
import '@mantine/core/styles.css'
import { MantineProvider, Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
function Example() {
  const [opened, { open, close }] = useDisclosure(false)
  return <MantineProvider>
    <Button onClick={open}>Edit</Button>
    <Modal opened={opened} onClose={close} title="Edit profile">
      <Button onClick={close}>Close</Button>
    </Modal>
  </MantineProvider>
}
```
Verify packaging/provider placement for SSR framework. Do not install Mantine Datatable third-party extensions as if they were `@mantine/core` components.

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
