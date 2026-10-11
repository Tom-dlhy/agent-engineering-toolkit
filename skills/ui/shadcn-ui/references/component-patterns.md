# shadcn-ui — component engineering and APIs

**Read when:** implementing Button, Field, Dialog, Sheet, Combobox, Data Table or debugging a behavior/prop contract with shadcn-ui. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Treat shadcn as source-owned code, not a sealed package: inspect components.json, aliases, Tailwind setup, styles and the installed component files before using registry examples.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://ui.shadcn.com/docs . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Source ownership and composition
Check whether the configured primitives are **Base UI or Radix**. Radix triggers commonly use `asChild`; Base UI composition uses `render`, which forwards attributes and refs. Do not interchange them. A local `components/ui/button.tsx` can be heavily customized; CLI updates can replace such changes.
Use semantic design tokens (`background`, `foreground`, `border`, `ring`) instead of scattered raw hex values. For forms inspect the actual installed `Field`, `InputGroup`, `Select` and form integration, because generated component shapes vary by registry base and release.
```bash
# Run under the project's package manager, inspect before changing sources
pnpm dlx shadcn@latest info --json
pnpm dlx shadcn@latest docs dialog field
pnpm dlx shadcn@latest add dialog --dry-run
pnpm dlx shadcn@latest add dialog --diff
```
For reproducibility pin the CLI in automation; the latest command is for interactive documentation, not unreviewed installation.

## Component decision / execution playbook

1. **Choose component anatomy:** consult the exact package's current part/slot composition; make no substitution across primitive vendors.
2. **Model state:** document value, input/selected/open distinction; controlled vs uncontrolled; keyboard/disabled/error/loading; how async data changes state.
3. **Implement inside existing system:** reuse installed wrappers, tokens, typography, form validation and router, avoiding a new package where supported primitives suffice.
4. **Validate behavior:** test mouse, keyboard, screen reader, narrow screen, non-English strings and pending network state; record incorrect semantics and fix.
5. **Inspect negative paths:** empty/no-results, invalid selection, two quick submits, close while pending, focus after unmount and hydration.

## Anti-patterns

- Copying snippets across different major versions or framework bindings.
- Treating a visual state as adequate accessibility; missing keyboard/focus or label semantics.
- Mixing primitive systems and their slot conventions without reviewing refs/events.
- Changing the global theme merely to fix a single component; choose nearest coherent scope.

## Exit evidence

Identify inspected package version and source file, positive and negative tests run, unsupported scenarios and documentation source. Do not assert official API details from memory when the installed version is unknown.
