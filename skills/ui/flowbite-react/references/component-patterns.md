# flowbite-react — component engineering and APIs

**Read when:** implementing Button, Modal, Dropdown, Tabs, Navbar, Table or debugging a behavior/prop contract with flowbite-react. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use ready-styled React controls aligned with Tailwind; inspect Flowbite plugin/config and version before composing templates.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://flowbite-react.com/docs/getting-started/introduction . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Tailwind and component semantics
Flowbite React is styled, not a Radix or Base UI headless primitives package. Inspect Tailwind version, PostCSS/Vite integration, component class generation and theme configuration. Ensure content extraction sees component classes and any generated theme rules.
For Modal, Dropdown and Tabs, inspect installed controlled event API and avoid inventing `asChild` conventions. For Table, decide whether it is merely presentational or needs a separate data-state layer for sorting/pagination.
Use existing design tokens to customize Flowbite's theme slots; don't override every Tailwind class inline.

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
