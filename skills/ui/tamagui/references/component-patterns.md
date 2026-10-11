# tamagui — widget patterns

**Read when:** implementing TamaguiProvider, Stack, XStack, YStack, Button, Sheet, Input. Not required for unrelated web UI.

## Compatibility and anatomy

Check installed SDK/framework/library versions, actual imports, app provider and app's navigation/state management. Official docs: https://tamagui.dev/docs/intro/introduction . Confirm against versioned API for changed props and runtime.

## Technical implementation

### Cross-platform tokens and styled primitives
Tamagui targets React Native and web with a compile-time extraction/optimization story. A shared token/variant contract is only useful if both platform builds resolve the same design intent.
```tsx
import { Button, XStack, YStack } from 'tamagui'
export function Actions() {
  return <YStack gap="$3">
    <XStack gap="$2"><Button>Save</Button><Button theme="red">Cancel</Button></XStack>
  </YStack>
}
```
Check the installed version for supported tokens and `TamaguiProvider` setup; examples from older Tamagui releases may differ. Avoid mixing uncontrolled DOM CSS and native style objects in shared component logic.

## Contract for real components

1. Identify root provider/theme and the enclosing navigation/modal/portal context.
2. Define state lifecycle: controlled values, focus, async updates, keyboard, selected options and disabled/error states.
3. Separate UI form validation from authorization and server persistence.
4. Handle platform-specific behavior intentionally: safe area, keyboard, Android back, iOS navigation, large accessibility text and touch.
5. Reuse existing widgets and conventions; avoid importing a second design system for a single missing component.

## Proof

Typecheck/build, component/widget tests and negative event paths; device checks for platform integration. Document what was verified and what remains untested.
