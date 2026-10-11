# daisyui: component mechanisms and patterns

**Read when:** implementing or debugging Button, Card, Modal, Dropdown, Theme. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://daisyui.com/docs/install/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — daisyui

### Class-driven Tailwind components
daisyUI offers Tailwind utility/component classes, not a React state/behavior library. Markup and state controls remain your responsibility; HTML dialog/menu semantics differ from framework-specific overlay primitives.
```html
<button class="btn btn-primary" type="button">Save</button>
<div class="card bg-base-100 shadow-md">
  <div class="card-body"><h2 class="card-title">Summary</h2></div>
</div>
```
For modals, evaluate native `<dialog>` behavior, `showModal()` and focus management instead of presuming CSS classes implement interaction. Follow official daisyUI version-specific patterns.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
