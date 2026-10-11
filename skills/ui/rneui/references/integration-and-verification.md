# rneui — platform integration and verification

**Read when:** integrating rneui, upgrading its SDK, configuring styles/theme, navigation or platform-specific behavior. Not needed for a separate framework's static UI.

## Integration decisions

### Styling and upgrades
Use the supported RNEUI theme provider/overrides to maintain shared colors/spacing; understand which components use native elements and which use overlays. Check icon package versions and performance before importing a large icon subset.
For list rows use stable item IDs, avoid index keys for insert/remove and choose virtualization for large dynamic lists (FlatList).
Verify Android/iOS Overlay back, keyboard avoidance, accessibility labels, contrast and navigation integration. If migrating from older React Native Elements, audit change logs, renamed props, theme types and imports before updating.

Official documentation: https://reactnativeelements.com/docs . Always inspect lockfile/SDK constraints and the chosen platform/build runner before running build or installation commands.

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
