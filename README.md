# Agent Engineering Toolkit

Modular, vendor-neutral AI engineering toolkit: reusable Agent Skills, lightweight workflows, quality gates, cloud and architecture guidance, and small installation profiles.

**Status: bootstrap.** This repo provides guidance and safe local tooling, NOT a full agent runtime, external marketplace, automatic importer or LLM token meter.

## Principles

1. Tiny permanent instructions; only load relevant skill bodies and referenced files on demand.
2. Prefer deterministic tools, evidence-based verification and simple designs over agent proliferation.
3. Scale process to risk: light, standard or deep.
4. Keep business logic testable and independent of provider SDKs when it has practical value.
5. Treat external skills as untrusted code; pin revisions, review scripts and preserve licenses.
6. Avoid blanket "always trigger" rules and benchmark usefulness before expanding.

## Layout

- AGENTS.md: concise shared operating contract
- CLAUDE.md: Claude Code-specific entry point
- skills/: portable SKILL.md guides, grouped by domain
- registry/skills.yaml: local skills catalog
- registry/sources.lock.yaml: future third-party provenance lock
- profiles/: curated subsets for different kinds of projects
- workflows/: light, standard and deep coordination recipes
- agents/: optional role briefs, not automatically spawned
- scripts/: validate, estimate context cost and safely install selected skills
- tests/: deterministic regression tests
- docs/: architecture and roadmap

## Quick start

Requires Python 3.12+.

~~~bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/context_budget.py --profile minimal

# Preview: does NOT write files
python scripts/install_profile.py --profile python-backend --agent codex --project /path/to/project

# Apply a profile only when you want to install the skills
python scripts/install_profile.py --profile python-backend --agent codex --project /path/to/project --apply
~~~

Codex installs to .agents/skills; Claude Code installs to .claude/skills. Never overwrites existing skills. Copy/adapt AGENTS.md separately if you want the shared rules in a target project. The installer does not execute skill scripts or access the internet.

Profiles: minimal, web-app, python-backend, cloud-engineering, fullstack. Installation is only a curated set; it does not imply every installed skill must run.

## UI library and component intelligence

The toolkit provides `ui-library-selection`, `ui-component-research` and 35 opt-in library specialists across React, Vue, Angular, Svelte, framework-agnostic UI, mobile and Flutter. Use `--skill <name>` to install one library skill on demand rather than installing them all.

See [docs/ui-skills.md](docs/ui-skills.md) for routing, component research and installation examples.

## Contribution and security

Open a feature/fix/docs branch, submit a PR, and merge only after CI checks pass. Never commit directly to main. See CONTRIBUTING.md, SECURITY.md and docs/roadmap.md.

Original work licensed under MIT. Future third-party imports must retain compatible licenses and attribution.
