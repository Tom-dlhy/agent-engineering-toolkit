# web-awesome: component mechanisms and patterns

**Read when:** implementing or debugging Custom elements, Button, Dialog, Select, Theme. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://webawesome.com/docs/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — web-awesome

### Web Components integration
Web Awesome exposes standards-based custom elements, which can be consumed across frameworks, but **properties are not interchangeable with string HTML attributes**. Confirm the exact custom-element tag names, package/version and registration strategy from vendor docs.
Web components may upgrade after initial markup; await `customElements.whenDefined` when imperative API use is required. For custom events, framework-specific synthetic event bindings may not be sufficient; use `addEventListener` and unsubscribe on unmount if needed.
Avoid inventing `<wa-*>` component names or methods from similar Shoelace libraries; verify current tag and method list. Shadow DOM styles require exposed CSS parts/custom properties rather than global descendant selectors.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
