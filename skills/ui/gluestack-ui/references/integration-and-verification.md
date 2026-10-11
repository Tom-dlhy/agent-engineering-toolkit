# gluestack-ui — platform integration and verification

**Read when:** integrating gluestack-ui, upgrading its SDK, configuring styles/theme, navigation or platform-specific behavior. Not needed for a separate framework's static UI.

## Integration decisions

### NativeWind, tokens and platform variants
Inspect Expo/React Native, NativeWind, Tailwind major, Babel/Metro and gluestack provider configuration. Styles that work on web may not be supported in native; evaluate platform-specific pseudo states and safe-area/keyboard interaction.
Treat the generator or registry as a source importer: review files and dependencies before applying updates. Prefer semantic tokens and slot patterns already used by local components.
Test scrollable Select in keyboard-up state, AlertDialog dismissal, native announcements, large text accessibility, RTL, portal host and Android hardware back. Maintain source files like application code with unit tests and local conventions.

Official documentation: https://gluestack.io/ui/docs/home/overview/introduction . Always inspect lockfile/SDK constraints and the chosen platform/build runner before running build or installation commands.

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
