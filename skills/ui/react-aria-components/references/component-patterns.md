# react-aria-components — component engineering and APIs

**Read when:** implementing Button, Dialog, Popover, ComboBox, Select, Table, ListBox or debugging a behavior/prop contract with react-aria-components. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Favor rich accessibility, focus semantics, keyboard interactions and internationalization; styling remains the application's responsibility.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://react-spectrum.adobe.com/react-aria/components.html . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Collections, render props and accessible parts
React Aria Components offers accessible state semantics, internationalization and compositional pieces. Many parts expose **render props or state attributes** rather than a flat style API.
```tsx
import { Button, Dialog, DialogTrigger, Modal, ModalOverlay, Heading } from 'react-aria-components'
export function Example() {
  return <DialogTrigger>
    <Button>Open settings</Button>
    <ModalOverlay>
      <Modal>
        <Dialog>
          <Heading slot="title">Settings</Heading>
          <Button slot="close">Close</Button>
        </Dialog>
      </Modal>
    </ModalOverlay>
  </DialogTrigger>
}
```
Use the documented `slot` contract; do not substitute shadcn or Radix part names. For complex collections, define stable keys independent of row indices.

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
