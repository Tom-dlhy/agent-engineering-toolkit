# bits-ui: component mechanisms and patterns

**Read when:** implementing or debugging Dialog, Select, Combobox, Dropdown Menu, Popover. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://bits-ui.com/docs/introduction ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — bits-ui

### Svelte 5 headless primitives
Bits UI is headless; visual styling and token consistency belong to the app. Newer versions target Svelte 5 and have changing snippet/bindable state contracts; inspect installed package before using older `<slot>` syntax.
For Dialog, Select and Combobox distinguish root/open state, portal/content parts, label and menu value. Preserve accessibility attributes when wrapping primitives; a wrapper that fails to pass event handlers or bindings can silently break keyboard behavior.
Use Svelte stores/runes consistently with the app's version; don't mix a Svelte 3 tutorial with Svelte 5 state patterns.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
