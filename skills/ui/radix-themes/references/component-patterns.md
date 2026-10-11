# radix-themes — component engineering and APIs

**Read when:** implementing Theme, Button, Dialog, Flex, Grid, Text, Table or debugging a behavior/prop contract with radix-themes. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Choose ready-styled components and theme scales; unlike Radix Primitives, this is an opinionated visual system.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://www.radix-ui.com/themes/docs/overview/getting-started . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Theme owns a cohesive visual language
Import the package stylesheet and render the supported `Theme` context at the correct application boundary. Configure appearance, accent and gray scales consistently. Use theme components and props for density, typography and spacing instead of duplicating token values throughout custom CSS.
```tsx
import '@radix-ui/themes/styles.css'
import { Theme, Button, Flex, Text } from '@radix-ui/themes'
export function Application() {
  return <Theme accentColor="indigo" appearance="light">
    <Flex direction="column" gap="3">
      <Text>Account</Text>
      <Button>Continue</Button>
    </Flex>
  </Theme>
}
```
Verify supported `accentColor` names and theme props for installed package. Do not apply headless `asChild` assumptions to themed component APIs.

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
