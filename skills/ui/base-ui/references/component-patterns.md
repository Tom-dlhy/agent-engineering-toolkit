# base-ui — component engineering and APIs

**Read when:** implementing Dialog, Menu, Select, Combobox, Popover, Tooltip, Field or debugging a behavior/prop contract with base-ui. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Choose unstyled React behavior; the application must own visual styling, state attributes and interaction composition.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://base-ui.com/react/overview/quick-start . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Composition uses `render`
Base UI parts expose a `render` prop. The rendered component must forward its ref and all behavior props; dropping them breaks focus, ARIA and pointer/keyboard interactions.
```tsx
import { Menu } from '@base-ui/react/menu'

function Example() {
  return <Menu.Root>
    <Menu.Trigger render={<button className="menu-trigger" />}>Open</Menu.Trigger>
    <Menu.Portal>
      <Menu.Positioner>
        <Menu.Popup>
          <Menu.Item>Account</Menu.Item>
        </Menu.Popup>
      </Menu.Positioner>
    </Menu.Portal>
  </Menu.Root>
}
```
When styling conditional states, read the documented `data-*` attributes on the actual part. Use `mergeProps` for merging event handlers/refs in custom render callbacks; naive prop spreading may overwrite internal handlers. Do **not** import Radix `asChild` code.

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
