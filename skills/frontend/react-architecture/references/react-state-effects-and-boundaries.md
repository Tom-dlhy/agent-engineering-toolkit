# React state, effects and component identity

**Read when:** the task touches react state, effects and component identity, rather than unrelated framework concerns.

## Decision and implementation
**State selection:** Keep derived values in render (`const visible = items.filter(...)`), not mirrored through `useEffect(setVisible)`. Local useState handles UI toggles; reducer handles multi-event local transitions. URL search params own shareable filters, remote Query/server cache owns fetched data. Use context only when consumers truly need shared ambient values; don't use it to hide unowned mutable globals.

**Effect test:** If code doesn't synchronize with an external system, it probably does not need an effect. When an effect subscribes to socket/ResizeObserver, return an unsubscribe; for fetch racing, abort older request and guard stale resolutions. React Strict Mode intentionally stresses cleanup in development; never fix by suppressing dev effects or using module-scoped `hasMounted`.

**Component contracts:** Stable `key` equals domain identity, not array index during reordering. Controlled input receives a value and change handler; uncontrolled form fields use refs/form submission. Keep keyboard label/focus behavior in component. Avoid changing ownership by passing setters down many unrelated levels; extract a feature boundary if needed.

~~~tsx
// Derived state, no effect or extra state:
const [query, setQuery] = useState("");
const matches = products.filter((p) => p.name.toLowerCase().includes(query.toLowerCase()));
// Ensure the source array and sorting are immutable.
~~~


## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://react.dev/learn/you-might-not-need-an-effect
- https://react.dev/learn/preserving-and-resetting-state
