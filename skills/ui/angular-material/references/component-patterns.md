# angular-material: component mechanisms and patterns

**Read when:** implementing or debugging MatFormField, MatDialog, MatTable, MatSelect, CDK. Do not open for unrelated visual edits or another provider.

## Version and technical scope

Identify the exact package name and major version, framework runtime, local wrappers, app's state/form architecture and layout/theme setup. The correct vendor documentation is https://material.angular.dev/ ; confirm the version currently installed before relying on a prop or event.

## Implementation guide — angular-material

### Angular reactive forms and DI
Prefer framework-native reactive forms for business forms. Angular Material supplies widgets and accessibility primitives; it does not replace form validation or the Angular CDK's overlays.
```ts
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-email',
  standalone: true,
  imports: [ReactiveFormsModule, MatFormFieldModule, MatInputModule],
  template: `<mat-form-field>
    <mat-label>Email</mat-label>
    <input matInput [formControl]="email" type="email" />
    @if (email.hasError('email')) { <mat-error>Invalid email</mat-error> }
  </mat-form-field>`
})
export class EmailComponent {
  email = new FormControl('', { nonNullable: true, validators: [Validators.email] });
}
```
Verify Angular template control-flow syntax against project version. Don't replace CDK's focus management with ad hoc event handlers.

## Component construction checklist

1. Identify the component's complete public anatomy (root, trigger, portal, panel/items or framework equivalents); preserve required props, refs and bindings.
2. Decide controlled state, default state, and state reset behavior; do not let model and application state compete.
3. Handle events as typed integration boundaries; validate inputs on the server for persistence and irreversible actions.
4. Use labels, descriptions, visible focus, active/disabled state and keyboard movement appropriate to the exact component.
5. Test loading, no data, remote data arriving out of order, invalid form submission, double click, and close/reopen after a mutation.

## Anti-patterns and proof

Do not copy a near-identical component name from a **different framework**. Avoid direct DOM manipulation of framework-owned components or internal library markup. Check installed API, typecheck/build, representative interaction and a negative case. If official docs differ from the local version, record the discrepancy and do not invent migration compatibility.
