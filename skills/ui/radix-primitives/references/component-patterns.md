# radix-primitives — component engineering and APIs

**Read when:** implementing Dialog, Dropdown Menu, Popover, Tooltip, Select, Tabs, Slot or debugging a behavior/prop contract with radix-primitives. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use Radix headless accessible primitives when you own CSS/theme and need composable React interaction patterns.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://www.radix-ui.com/primitives/docs/overview/introduction . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Radix parts and `asChild`
Radix primitives separate state/behavior (`Root`) from individual DOM parts; portals create overlay stacking contexts. The `asChild` composition mechanism clones its child and injects props; it **must** receive one ref-forwarding, prop-spreading child.
```tsx
import * as Dialog from '@radix-ui/react-dialog'
function EditDialog() {
  return <Dialog.Root>
    <Dialog.Trigger asChild><button>Edit</button></Dialog.Trigger>
    <Dialog.Portal>
      <Dialog.Overlay className="overlay" />
      <Dialog.Content>
        <Dialog.Title>Edit profile</Dialog.Title>
        <Dialog.Description>Update your public details.</Dialog.Description>
        <Dialog.Close asChild><button type="button">Close</button></Dialog.Close>
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
}
```
Do not place a button inside a button or override the focus handlers delivered by Radix.

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
