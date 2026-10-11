# ionic: component mechanisms and patterns

**Read when:** implementing or debugging IonPage, IonRouterOutlet, IonTabs, IonModal, IonList. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://ionicframework.com/docs ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — ionic

### Mobile navigation is a stack, not regular links
Ionic's `IonPage`, `IonContent` and `IonRouterOutlet` coordinate animated navigation and lifecycle; missing `IonPage` can break transitions, scroll and caching. Inspect React/Angular/Vue binding and router major before composing views.
Prefer Ionic navigation and tabs consistent with native back gestures, safe areas and tab stacks. A modal is a routed/lifecycle-aware overlay; distinguish inline and controller-based modal creation for the binding.
Never use a browser-only DOM approach as a substitute for an Ionic component's lifecycle.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
