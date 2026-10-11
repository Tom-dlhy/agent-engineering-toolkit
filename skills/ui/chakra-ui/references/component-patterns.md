# chakra-ui — component engineering and APIs

**Read when:** implementing Button, Dialog, Menu, Select, Field, Table or debugging a behavior/prop contract with chakra-ui. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Build token-driven React UI with Chakra's slot recipes; version-check v2 vs v3 architecture.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://chakra-ui.com/docs . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Chakra's generational API break
Chakra v3 uses Ark-inspired **compound component namespaces**, slot recipes and a system/provider setup distinct from many Chakra v2 snippets. Detect major version; never paste older `isOpen`/`isLoading` examples without checking current API.
```tsx
import { ChakraProvider, defaultSystem, Button } from '@chakra-ui/react'
export function Root({ children }: { children: React.ReactNode }) {
  return <ChakraProvider value={defaultSystem}>
    <Button colorPalette="teal">Save</Button>
    {children}
  </ChakraProvider>
}
```
Use semantic tokens and recipes for variants; do not invent CSS variable names from another design system.

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
