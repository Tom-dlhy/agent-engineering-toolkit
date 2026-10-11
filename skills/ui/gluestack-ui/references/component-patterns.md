# gluestack-ui — widget patterns

**Read when:** implementing Button, Input, AlertDialog, Menu, Select, FormControl. Not required for unrelated web UI.

## Compatibility and anatomy

Check installed SDK/framework/library versions, actual imports, app provider and app's navigation/state management. Official docs: https://gluestack.io/ui/docs/home/overview/introduction . Confirm against versioned API for changed props and runtime.

## Technical implementation

### Open-code React Native component ownership
gluestack-ui may generate/copy components into your project, so the local component implementation is part of your design system. Inspect `components/ui` source and generator setup rather than treating it as a sealed dependency.
Depending on generation, styling may rely on NativeWind/Tailwind tokens and context providers; confirm the installed release's utilities and dependency stack before applying examples.
For composed controls (Select, Menu, Dialog), preserve trigger, backdrop, content/portal and animation mechanics. Never overwrite locally edited source-owned files blindly.

## Contract for real components

1. Identify root provider/theme and the enclosing navigation/modal/portal context.
2. Define state lifecycle: controlled values, focus, async updates, keyboard, selected options and disabled/error states.
3. Separate UI form validation from authorization and server persistence.
4. Handle platform-specific behavior intentionally: safe area, keyboard, Android back, iOS navigation, large accessibility text and touch.
5. Reuse existing widgets and conventions; avoid importing a second design system for a single missing component.

## Proof

Typecheck/build, component/widget tests and negative event paths; device checks for platform integration. Document what was verified and what remains untested.
