# bootstrap: component mechanisms and patterns

**Read when:** implementing or debugging Grid, Modal, Offcanvas, Accordion, Form. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://getbootstrap.com/docs/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — bootstrap

### CSS utilities are not component behavior
Bootstrap provides responsive grid, utilities, components and JS plugins. Decide whether using purely CSS or the Bootstrap JS bundle; adding both framework wrappers and Bootstrap JS can cause duplicate state ownership.
```html
<button type="button" class="btn btn-primary">Save</button>
<div class="container"><div class="row g-3">
  <div class="col-12 col-md-6">Column A</div>
  <div class="col-12 col-md-6">Column B</div>
</div></div>
```
For Modal/Dropdown/Tooltip confirm Popper dependency and required data attributes or explicit JS initialization for installed major release. Don't make an interactive div only because it has `btn` styling.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
