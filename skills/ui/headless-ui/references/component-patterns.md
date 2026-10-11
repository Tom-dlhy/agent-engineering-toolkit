# headless-ui — component engineering and APIs

**Read when:** implementing Dialog, Listbox, Combobox, Menu, Disclosure, Tabs or debugging a behavior/prop contract with headless-ui. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use Headless UI for accessible unstyled React or Vue components; follow framework-specific docs, not swapped prop conventions.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://headlessui.com/ . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Compound composition
Headless UI manages focus and state; you own appearance. React and Vue exports have different declarative syntax. For React:
```tsx
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
function AccountDialog({ open, close }: { open: boolean; close(): void }) {
  return <Dialog open={open} onClose={close}>
    <div className="fixed inset-0 bg-black/40" aria-hidden="true" />
    <DialogPanel>
      <DialogTitle>Account</DialogTitle>
      <button onClick={close}>Close</button>
    </DialogPanel>
  </Dialog>
}
```
Verify current Dialog portal/backdrop instructions: a simplified example needs correct visual positioning/z-index and Tailwind classes.

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
