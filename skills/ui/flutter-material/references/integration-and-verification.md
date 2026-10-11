# flutter-material — platform integration and verification

**Read when:** integrating flutter-material, upgrading its SDK, configuring styles/theme, navigation or platform-specific behavior. Not needed for a separate framework's static UI.

## Integration decisions

### Material 3, navigation and responsive behavior
Check Flutter SDK, Material 3 choice (`useMaterial3` semantics according to installed SDK), theme extensions, ColorScheme, typography and stateful/scoped theme. Widgets should read Theme.of(context) rather than hardcoded colors.
Use Navigator/Router architecture consistent with existing routes; avoid keeping BuildContext across async gaps without checking `mounted`. Preserve keyboard insets, safe area, screen reader semantics and minimum touch areas.
Use `ListView.builder`/slivers for long data rather than a huge Column. Test widget states with `flutter test`, golden tests when stable, actual iOS/Android platforms, text scale, RTL and landscape. Treat platform adaptations as explicit design choices.

Official documentation: https://docs.flutter.dev/ui/widgets/material . Always inspect lockfile/SDK constraints and the chosen platform/build runner before running build or installation commands.

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
