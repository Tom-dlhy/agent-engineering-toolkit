# flutter-material — widget patterns

**Read when:** implementing MaterialApp, ThemeData, Scaffold, Form, TextFormField, ListView. Not required for unrelated web UI.

## Compatibility and anatomy

Check installed SDK/framework/library versions, actual imports, app provider and app's navigation/state management. Official docs: https://docs.flutter.dev/ui/widgets/material . Confirm against versioned API for changed props and runtime.

## Technical implementation

### Flutter Material's widget/state contracts
Use `MaterialApp` and `ThemeData` as the app-level Material theme context; compose `Scaffold`, `AppBar`, responsive layout and stateful widgets according to the existing state management.
```dart
import 'package:flutter/material.dart';

class EmailScreen extends StatefulWidget {
  const EmailScreen({super.key});
  @override
  State<EmailScreen> createState() => _EmailScreenState();
}
class _EmailScreenState extends State<EmailScreen> {
  final controller = TextEditingController();
  @override
  void dispose() { controller.dispose(); super.dispose(); }
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Account')),
    body: Padding(padding: const EdgeInsets.all(16), child: Column(children: [
      TextField(controller: controller, decoration: const InputDecoration(labelText: 'Email')),
      FilledButton(onPressed: () {}, child: const Text('Save'))
    ])),
  );
}
```
Dispose controllers/focus nodes owned by State. Use proper Form/TextFormField validation for persisted submissions; TextField alone doesn't implement business validation.

## Contract for real components

1. Identify root provider/theme and the enclosing navigation/modal/portal context.
2. Define state lifecycle: controlled values, focus, async updates, keyboard, selected options and disabled/error states.
3. Separate UI form validation from authorization and server persistence.
4. Handle platform-specific behavior intentionally: safe area, keyboard, Android back, iOS navigation, large accessibility text and touch.
5. Reuse existing widgets and conventions; avoid importing a second design system for a single missing component.

## Proof

Typecheck/build, component/widget tests and negative event paths; device checks for platform integration. Document what was verified and what remains untested.
