# fluent-ui — component engineering and APIs

**Read when:** implementing Button, Dialog, Field, Combobox, DataGrid or debugging a behavior/prop contract with fluent-ui. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use Fluent UI v9 React when Microsoft design semantics and enterprise keyboard accessibility align with the product.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://react.fluentui.dev/ . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Fluent UI v9 is slot-oriented
Use `@fluentui/react-components` and `FluentProvider`; the old `@fluentui/react` v8 control contracts are **not** interchangeable.
```tsx
import { FluentProvider, webLightTheme, Button, Field, Input } from '@fluentui/react-components'
export function Example() {
  return <FluentProvider theme={webLightTheme}>
    <Field label="Email" required>
      <Input type="email" />
    </Field>
    <Button appearance="primary">Save</Button>
  </FluentProvider>
}
```
Styles use Griffel and slots; custom wrappers must preserve component props/refs.

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
