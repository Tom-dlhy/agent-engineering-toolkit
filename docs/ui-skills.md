# UI library and component skill system

## Goal

Choose the right UI library for the existing stack and exercise its **actual documented component APIs**, with sufficient depth for complex product work without mounting dozens of library docs into every agent context.

## Layers

1. `skills/stacks/ui-library-selection` makes technology decisions from a catalog and evaluates existing project dependencies.
2. **35 opt-in provider skills** represent the library-specific architecture, advanced component families, documentation, theme and integration pitfalls.
3. `ui-component-research` provides per-component deep research and four focused references for forms, overlays, data and feedback. Open **only relevant** material and consult version-matched provider documentation; do not assume all component names share implementation rules.

Existing `frontend-design` remains responsible for creative direction, composition, responsive and visual QA. The UI skills should not duplicate it.

## Decision procedure

1. If the UI library is already established and matches requirements, **REUSE** it.
2. If selecting from scratch, activate `ui-library-selection` and read only its compact library map; shortlist compatible candidates.
3. Activate or install **one** provider skill after selection. Components such as Button/Dialog/DataTable are handled by that skill plus `ui-component-research` when nontrivial.
4. When researching a component, inspect installed dependencies and read its **exact** official docs, including slots, event names, accessibility, states, theme and examples. Persist component-specific lessons as optional references only if they are reusable, versioned and valuable.
5. Only create a standalone component skill when it represents a distinct complex workflow, not just a separate button/widget. Apply the repository governance checklist before doing so.

## Installation examples

All commands default to preview; `--apply` is opt-in.

```bash
# React + Tailwind + shadcn complete curated setup
python scripts/install_profile.py --profile ui-shadcn --agent codex --project /path/to/project

# Existing web-app profile, plus one chosen vendor
python scripts/install_profile.py --profile web-app --skill mantine --agent claude --project /path/to/project

# Lightweight standalone UI specialist selection
python scripts/install_profile.py --skill shadcn-ui --skill ui-component-research --agent codex --project /path/to/project
```

After inspecting output add `--apply` to execute. The installer will not overwrite existing skills. No external installer or third-party script is executed; provider docs are linked, not vendored.

## V2 integration policy

The existing selector remains at `skills/stacks/ui-library-selection`, with no duplicate. Provider skills under `skills/ui/` are opt-in and use targeted local leaves. Each must meet the common quality contract, with version-specific API claims checked against actual installed packages. No maturity labels determine routing or trust.

## External source and maintenance

The shadcn adapter points to the official shadcn Agent Skill at an identified GitHub revision. It is **not an import** of its scripts, hooks or assets. Follow `external-skill-audit` before vendoring. No provider-specific command should run just because a linked upstream skill contains it.

Keep the catalog useful but its claims modest: compatibility, props, licenses and availability must be rechecked with currently installed package versions. A docs-only component reference should not be promoted to a `SKILL.md` without measurable benefits.

## Testing and context cost

Use `python scripts/validate_skills.py`, `python -m unittest discover -s tests -v`, and `python scripts/context_budget.py --profile minimal --budget 2500`; also inspect `--profile web-app` estimates and validate the target installation in dry-run mode. Context-budget estimates are character heuristics, not measured model tokens.

## Verification and remaining evidence

The existing deterministic suite covers 35 local provider leaf pairs, four shared component-research leaves, safe installation, context budgets and routing. These checks do not establish that every provider API or accessibility behavior has been validated in a live app; keep the missing evidence as a QA backlog rather than a maturity tier. See `docs/expertise-audit.md`.
