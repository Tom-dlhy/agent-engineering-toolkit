# Overlay, navigation and focus management

**Read when:** implementing Dialog, Sheet, Drawer, Modal, Popover, Tooltip, Menu, Tabs or mobile navigation.

## Overlay anatomy

Before writing code identify: Root/open state, Trigger, Portal/positioner, Content/Panel, Title/Description, Backdrop/Overlay, Close action, initial and return focus. The exact primitive may expose a different set and hierarchy. Do not mix Radix `asChild`, Base UI `render`, React Aria slots or native Flutter builders.

### Decision rules

- **Modal dialog** blocks background interaction; it needs an accessible name, correct focus placement/trap and safe focus restoration. Use provider modal semantics, not a plain `position:fixed` div.
- **Popover/combobox** usually remains related to an anchor; check viewport collision, scroll containers and keyboard/ARIA selection model.
- **Tooltip** is supplementary content, not a substitute for labeling an unlabeled icon button; touch devices may not offer hover.
- **Tabs/menu** distinguish focus from activation, arrow-key navigation, selected state, roving focus, route persistence and nested menus.
- **Mobile navigation** integrates back navigation, scroll retention, safe areas and platform-specific gesture semantics; Ionic, React Native and Flutter have different route stacks.

## React native HTML fallback where reasonable

If the installed toolkit lacks a suitable Dialog and the app can rely on native browsers, `<dialog>` with `showModal()` offers built-in modal behavior. Still provide a visible close button, appropriate accessible heading/label, focus policy and tests.

```tsx
import { useRef } from 'react'
export function NativeDialogExample() {
  const ref = useRef<HTMLDialogElement>(null)
  return <>
    <button type="button" onClick={() => ref.current?.showModal()}>Details</button>
    <dialog ref={ref} aria-labelledby="detail-heading">
      <h2 id="detail-heading">Details</h2>
      <p>Record information.</p>
      <form method="dialog"><button type="submit">Close</button></form>
    </dialog>
  </>
}
```

This is a *fallback*, not a recommendation to replace provider overlays blindly. Native and library dialogs have different styling/transition/backdrop/event contracts; test browser support and required UX.

## Nested behavior and verification

Test Escape vs backdrop dismissal, form submission while pending, focus after trigger unmount, nested menu inside dialog, viewport collision, body scroll lock, portal layering, RTL, screen-reader names and keyboard-only path. For routing overlays, exercise browser back/forward and direct deep-link loading without hydrating to a different open state.
