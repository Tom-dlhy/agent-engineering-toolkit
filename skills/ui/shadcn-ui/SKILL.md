---
name: shadcn-ui
domain: ui
version: "0.1.0"
description: >-
  Use when implementing, integrating, debugging or reviewing shadcn/ui components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# shadcn/ui — provider-specific UI engineering

**Best fit:** source-owned components, Tailwind-first product UI and customizable design systems.
**Target stack:** React, TypeScript, Tailwind; TanStack Start, Next.js, Vite, React Router and other supported integrations.
**Official documentation:** https://ui.shadcn.com/docs

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** Button, Field, InputGroup, Select, Dialog, Sheet, Table, Sidebar, Chart, Tabs.

**Provider-specific method:** Inspect components.json and run the project package runner with shadcn info --json. Inspect installed UI files before selecting registries. Use shadcn docs <component> to resolve current APIs; add --dry-run and --diff before changes to existing components. Distinguish Base UI from Radix before composing triggers.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Never blindly overwrite locally customized components, mix Base UI and Radix trigger conventions, or invent a registry; verify Tailwind tokens, CSS aliases and icon library.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.

## Official upstream reference

Official shadcn Agent Skill: https://github.com/shadcn-ui/ui/blob/c2a67849be260701852b0977ba15eb5f3a0ce2a4/skills/shadcn/SKILL.md . This is a **reference**, not a vendored copy or authorization to execute upstream scripts. Consult its component-level rule pages (styling, forms, composition, icons, Base UI versus Radix) when necessary; inspect every upstream command before use. Source repository MIT license; review all files and NOTICE obligations before any future import.

## Project-aware CLI

Choose npm/pnpm/bun based on packageManager. For pnpm:
```bash
pnpm dlx shadcn@latest info --json
pnpm dlx shadcn@latest docs button dialog
pnpm dlx shadcn@latest add button --dry-run
```
Avoid `@latest` for reproducible automated builds; pin the approved CLI version in repeatable CI. For updates inspect `--diff` before editing existing source-owned components. Use component variants and semantic colors; use `FieldGroup` / `Field` for forms when supported by the detected component generation. Do not blindly apply Radix `asChild` to Base UI, which can require a `render` prop.
