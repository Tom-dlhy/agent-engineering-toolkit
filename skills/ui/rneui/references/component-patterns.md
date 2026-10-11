# rneui — widget patterns

**Read when:** implementing ThemeProvider, Button, Input, ListItem, Overlay, SearchBar. Not required for unrelated web UI.

## Compatibility and anatomy

Check installed SDK/framework/library versions, actual imports, app provider and app's navigation/state management. Official docs: https://reactnativeelements.com/docs . Confirm against versioned API for changed props and runtime.

## Technical implementation

### RNEUI package split and theming
React Native Elements/RNEUI commonly separates `@rneui/base` and `@rneui/themed` packages. Inspect installed major versions and imports; legacy `react-native-elements` examples need migration, not blind copy-paste.
```tsx
import { Button, ThemeProvider } from '@rneui/themed'
export function Example() {
  return <ThemeProvider><Button title="Submit" onPress={() => {}} /></ThemeProvider>
}
```
Check the component's actual event/value contract: RNEUI `Input` may wrap TextInput differently from Paper; don't assume identical props.

## Contract for real components

1. Identify root provider/theme and the enclosing navigation/modal/portal context.
2. Define state lifecycle: controlled values, focus, async updates, keyboard, selected options and disabled/error states.
3. Separate UI form validation from authorization and server persistence.
4. Handle platform-specific behavior intentionally: safe area, keyboard, Android back, iOS navigation, large accessibility text and touch.
5. Reuse existing widgets and conventions; avoid importing a second design system for a single missing component.

## Proof

Typecheck/build, component/widget tests and negative event paths; device checks for platform integration. Document what was verified and what remains untested.
