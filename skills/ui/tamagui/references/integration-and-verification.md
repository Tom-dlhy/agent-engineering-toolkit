# tamagui — platform integration and verification

**Read when:** integrating tamagui, upgrading its SDK, configuring styles/theme, navigation or platform-specific behavior. Not needed for a separate framework's static UI.

## Integration decisions

### Compiler and build integration
Inspect `tamagui.config`, compiler plugin and app bundler: Vite/Next/Metro/Expo may require different setup. Ensure static style extraction actually runs and production builds work; a working dev screen does not prove optimized bundles.
Define tokens, fonts, themes and media queries as shared public contracts. Use variants for predictable components; override platform-specific behavior only when needed (hover/web vs press/native, keyboard, safe area).
For Sheet/overlay verify native animation driver, screen navigation and portal placement. Test iOS/Android/web in release configuration; check hydration, animations reduced motion and accessibility semantics, not only screenshots.

Official documentation: https://tamagui.dev/docs/intro/introduction . Always inspect lockfile/SDK constraints and the chosen platform/build runner before running build or installation commands.

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
