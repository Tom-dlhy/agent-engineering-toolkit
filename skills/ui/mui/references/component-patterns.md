# mui — component engineering and APIs

**Read when:** implementing TextField, Dialog, Autocomplete, DataGrid, DatePicker, ThemeProvider or debugging a behavior/prop contract with mui. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use MUI Material core for Material Design and enterprise React; advanced Data Grid/Pickers live in MUI X with separate packages and licensing.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://mui.com/material-ui/getting-started/ . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Themed core vs MUI X
`@mui/material`, `@mui/system`, `@mui/x-data-grid` and pickers have separate versions/licensing constraints. Keep ThemeProvider and styling integration consistent; use `sx`, CSS variables or theme overrides rather than copy-pasting unrelated CSS utility classes.
```tsx
import { ThemeProvider, createTheme, Button, Stack } from '@mui/material'
const theme = createTheme({ palette: { primary: { main: '#2255aa' } } })
export function Example() {
  return <ThemeProvider theme={theme}>
    <Stack direction="row" spacing={2}><Button variant="contained">Save</Button></Stack>
  </ThemeProvider>
}
```
Review `slotProps`, `slots` and current `Grid` API: migration between major versions can change behavior. <Cite> not relevant in repo docs.

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
