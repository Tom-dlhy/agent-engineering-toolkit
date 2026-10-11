# flutter-cupertino — platform integration and verification

**Read when:** integrating flutter-cupertino, upgrading its SDK, configuring styles/theme, navigation or platform-specific behavior. Not needed for a separate framework's static UI.

## Integration decisions

### iOS behavior and adaptive APIs
Inspect Flutter/iOS/macOS SDK support; Cupertino dynamic colors/theme brightness, navigation transition and back gesture semantics are version dependent. Build labels and dynamic text scale with system accessibility settings; maintain platform form keyboards and dismissal.
Avoid mixing Material and Cupertino theme contexts without an intentional adaptive boundary. `CupertinoTheme` can be nested for distinct scope; test dialogs, scroll physics, form interaction, keyboard and navigation routes.
Verify VoiceOver semantics, large text, dark system appearance, reduced motion and RTL (where relevant). Run `flutter test` and device testing; no screenshot alone proves Apple platform conformity.

Official documentation: https://docs.flutter.dev/ui/widgets/cupertino . Always inspect lockfile/SDK constraints and the chosen platform/build runner before running build or installation commands.

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
