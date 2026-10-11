# Agent Engineering Toolkit

**Vendor-neutral AI engineering skills, workflows and quality gates — modular by design, economical in context.**

A growing library of **101 first-party skills across 11 domains**, with **13 small installation profiles**, lightweight `light / standard / deep` workflows, optional agent role briefs, and a **deterministic local skill finder**. Designed for Claude Code, Codex and other compatible environments without requiring an LLM API call to discover skills.

 > Status: progressive expertise refactor underway. Seven AWS skills are deep V2; the other 58 entries retain their original scope and are scheduled for content review. This is not an autonomous agent runtime, model-independent execution engine, third-party skill marketplace or exact token meter.

## Why

The number of skills in a repository should not determine the cost of every agent session:

- **101 skills stored** in the library; only **5–20 installed** in a project profile.
- **Names, descriptions and task keywords** enable local discovery; only 1–3 relevant skill bodies should be read in a typical task.
- **Risk-aware workflows** prevent costly multi-agent review loops on trivial edits.
- **Validation and tests** run without using any LLM tokens.
- **No automatic third-party downloads or execution**; security and licensing come before convenience.

## Quick start

Requirements: Python 3.12+ and PyYAML.

~~~bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v

# Find focused skills and an advisory workflow mode
python scripts/skillctl.py search "Python DDD clean architecture" --profile python-backend
python scripts/skillctl.py recommend "AWS IAM migration" --profile cloud-engineering
python scripts/skillctl.py profiles
python scripts/skillctl.py show python-ddd
python scripts/skillctl.py references aws-bedrock
python scripts/skillctl.py read-ref aws-bedrock references/converse-api.md

# Measure only the reference that is explicitly opened
python scripts/context_budget.py --profile aws-platform --activated aws-bedrock --reference aws-bedrock:references/converse-api.md

# Compare approximate always-on context sizes
python scripts/context_budget.py --all

# Safe local installation: preview first, then copy
python scripts/install_profile.py --agent codex --profile python-backend --project /path/to/project
python scripts/install_profile.py --agent codex --profile python-backend --project /path/to/project --apply

# For Claude Code use --agent claude; no overwrite of existing installed skills
~~~

The installer writes only when `--apply` is provided. It copies selected skills to `.agents/skills` (Codex) or `.claude/skills` (Claude Code). Copy/adapt `AGENTS.md` into a target project separately to adopt shared conventions. Never install every profile indiscriminately.

## UI library expertise

35 optional provider skills across web, native and Flutter; plus one `ui-component-research` skill. The original `ui-library-selection` is **extended** in `skills/stacks`, never duplicated. See [UI skills](docs/ui-skills.md). Install only the chosen provider using `--skill` and read its optional references when needed.

## Explore

- [Progressive expertise refactor and quality standard](docs/progressive-expertise.md)
- [Expertise depth audit / migration backlog](docs/expertise-audit.md)
- [Catalog and authoring conventions](docs/catalog.md)
- [Progressive disclosure and token budgets](docs/skill-routing.md)
- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security and third-party intake](SECURITY.md)

The library covers Python DDD and hexagonal architecture, API design, modern Python and TypeScript, AWS/GCP/Azure/Cloudflare and IaC, data engineering, LLM applications, UI/UX and glassmorphism, testing, security and release workflows.

## Development policy

Open a focused feature branch and PR. CI validates all skill metadata/profile references, runs unit tests and enforces a **rough** context-budget guardrail. Never push directly to main. Merge only after required checks pass.

Original content is MIT licensed. Third-party sources such as [ECC](https://github.com/affaan-m/ECC), [Superpowers](https://github.com/obra/superpowers), [Anthropic Cybersecurity Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) and [Brag](https://github.com/latent-spaces/brag) inspired the architecture; **none of their skills are copied into the project at this stage**.
