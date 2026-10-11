# react-native-paper — platform integration and verification

**Read when:** integrating react-native-paper, upgrading its SDK, configuring styles/theme, navigation or platform-specific behavior. Not needed for a separate framework's static UI.

## Integration decisions

### Material 3 and native services
Inspect major version and Paper theme variant (MD3), default fonts, colors, ripple and icon dependencies. Do not translate a web MUI `ThemeProvider` object into Paper unchanged.
For dialogs/snackbars, verify portal host placement and back button dismissal on Android. Avoid using modal for every keyboard overlay; test with native keyboard and safe areas.
Check React Native version, Expo managed/bare workflow, Hermes/new architecture and React Navigation coexistence. Measure touch target sizes, accessibility via TalkBack/VoiceOver, dark system scheme, low-end Android performance and offline network errors.

Official documentation: https://callstack.github.io/react-native-paper/ . Always inspect lockfile/SDK constraints and the chosen platform/build runner before running build or installation commands.

## Target-specific quality matrix

| Area | Expected behavior | Negative scenario |
|---|---|---|
| Form and input | Correct native keyboard, field label, validation and submit | Keyboard hides field, async error, double submit |
| Dialog/modal/sheet | Dismiss policy, backdrop, focus and accessible announcement | Android hardware back, nested modal, interrupted transition |
| Navigation | Correct route/stack, safe area and system gesture | Deep link, app resume, back gesture/gesture conflict |
| Theme | Platform theme, light/dark, reduced motion | Large text/contrast and OS preference changes |
| Data | Stable row IDs, efficient list virtualization | 10k entries, slow fetch, empty/timeout/offline |
| Runtime | Compatible SDK, release build and no missing assets | Cold launch, background/resume and production bundle |

## Migration and rollout

Run a versioned migration guide in a separate branch, inspect dependency pins, adapt provider/theme setup, and validate unit/widget tests plus at least one production-like build. Native bugs often require actual hardware/emulator checks. Never claim device verification without executing it.

Report platform matrix, versions, tests and manual QA completed, unresolved OS-specific risks and rollback notes.
