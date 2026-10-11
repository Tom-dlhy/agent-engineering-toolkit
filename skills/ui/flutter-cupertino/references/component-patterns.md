# flutter-cupertino — widget patterns

**Read when:** implementing CupertinoApp, CupertinoPageScaffold, CupertinoNavigationBar, CupertinoTextField, CupertinoAlertDialog. Not required for unrelated web UI.

## Compatibility and anatomy

Check installed SDK/framework/library versions, actual imports, app provider and app's navigation/state management. Official docs: https://docs.flutter.dev/ui/widgets/cupertino . Confirm against versioned API for changed props and runtime.

## Technical implementation

### Apple idioms with Flutter widgets
Cupertino components implement Apple-style visual/navigation conventions, but do not make an app automatically native. Decide if the product follows Cupertino throughout or uses explicit adaptive Material/Cupertino views.
```dart
import 'package:flutter/cupertino.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});
  @override
  Widget build(BuildContext context) => CupertinoPageScaffold(
    navigationBar: const CupertinoNavigationBar(middle: Text('Profile')),
    child: SafeArea(child: Center(child:
      CupertinoButton(onPressed: () {}, child: const Text('Continue'))
    )),
  );
}
```
Use CupertinoPageRoute/dialog navigation appropriate to the chosen architecture; widget names are distinct from Material's Scaffold/AlertDialog.

## Contract for real components

1. Identify root provider/theme and the enclosing navigation/modal/portal context.
2. Define state lifecycle: controlled values, focus, async updates, keyboard, selected options and disabled/error states.
3. Separate UI form validation from authorization and server persistence.
4. Handle platform-specific behavior intentionally: safe area, keyboard, Android back, iOS navigation, large accessibility text and touch.
5. Reuse existing widgets and conventions; avoid importing a second design system for a single missing component.

## Proof

Typecheck/build, component/widget tests and negative event paths; device checks for platform integration. Document what was verified and what remains untested.
