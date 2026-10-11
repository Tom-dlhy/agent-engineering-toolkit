# heroui — component engineering and APIs

**Read when:** implementing Button, Modal, Select, Table, DatePicker, Autocomplete or debugging a behavior/prop contract with heroui. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use a styled React kit with integrated component styling; confirm installed package generation and styling engine before writing examples.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://www.heroui.com/docs . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Package generation matters
HeroUI APIs and packages have evolved; inspect `package.json` for `@heroui/react` and related packages before choosing imports. Do not assume old NextUI component contracts or newer HeroUI releases are interchangeable.
For selection/list components differentiate `selectedKeys` / key collections from simple scalar values; use official forms examples rather than mapping directly to HTML `select` props.
For modal and dropdown confirm provider/root setup, portal mount, focus recovery, animation settings and scroll behavior. For tables retain stable row keys and declared column keys; never derive identity from display index.
Theme and Tailwind configuration can change across major versions; inspect installed CSS and provider settings before applying a tutorial.

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
