# react-native-paper — widget patterns

**Read when:** implementing PaperProvider, Button, TextInput, Dialog, Snackbar, DataTable. Not required for unrelated web UI.

## Compatibility and anatomy

Check installed SDK/framework/library versions, actual imports, app provider and app's navigation/state management. Official docs: https://callstack.github.io/react-native-paper/ . Confirm against versioned API for changed props and runtime.

## Technical implementation

### React Native Paper provider and theme
Wrap the root app with `PaperProvider`, respecting React Navigation and Expo provider order. Paper uses React Native components and Material Design semantics; CSS/Tailwind classes from web do not directly apply.
```tsx
import * as React from 'react'
import { PaperProvider, Button, TextInput } from 'react-native-paper'
export default function App() {
  const [email, setEmail] = React.useState('')
  return <PaperProvider>
    <TextInput label="Email" keyboardType="email-address" value={email} onChangeText={setEmail} />
    <Button mode="contained" onPress={() => {}}>Continue</Button>
  </PaperProvider>
}
```
Paper TextInput value uses `onChangeText`, not web `onChange` DOM events. Use controlled state with proper keyboard and accessibility labels.

## Contract for real components

1. Identify root provider/theme and the enclosing navigation/modal/portal context.
2. Define state lifecycle: controlled values, focus, async updates, keyboard, selected options and disabled/error states.
3. Separate UI form validation from authorization and server persistence.
4. Handle platform-specific behavior intentionally: safe area, keyboard, Android back, iOS navigation, large accessibility text and touch.
5. Reuse existing widgets and conventions; avoid importing a second design system for a single missing component.

## Proof

Typecheck/build, component/widget tests and negative event paths; device checks for platform integration. Document what was verified and what remains untested.
