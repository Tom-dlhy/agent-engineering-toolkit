<div align="center">

# Agent Engineering Toolkit

**Better engineering decisions for coding agents. Without the heavyweight workflow on every change.**

A modular, vendor-neutral library of engineering skills, practical playbooks and verification methods for **Codex**, **Claude Code** and compatible Agent Skills environments.

[![CI](https://github.com/Tom-dlhy/agent-engineering-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tom-dlhy/agent-engineering-toolkit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776ab.svg)](https://www.python.org/)

**178 skills** · **14 domains** · **423 expert references** · **20 curated profiles**

[Get started](#quick-start) · [Install for Codex](#codex) · [Install for Claude Code](#claude-code) · [Architecture](#architecture) · [Documentation](#documentation)

</div>

---

## The idea

Coding agents can write code quickly. Getting them to consistently **choose an appropriate approach, understand a project's constraints, test the right things and know when to stop** is a different problem.

Agent Engineering Toolkit (AET) is a collection of reusable engineering knowledge and operating methods designed around that problem.

It is **not** a new coding agent, a model wrapper, or a prompt that asks an assistant to "follow best practices." It supplies concrete methods and specialized references that an existing agent can consult when they actually matter.

The goal is simple:

> **Broad knowledge on disk. Focused expertise in context. Rigor proportional to risk.**

### What makes it different

| Principle | In practice |
| --- | --- |
| **Progressive disclosure** | Discover a skill through short metadata, load its `SKILL.md` when useful, then open only the relevant `references/`. |
| **Right-sized execution** | LIGHT, STANDARD and DEEP workflows adapt planning, tests and review to the real change—not just its size or keywords. |
| **Review with a purpose** | R0 self-review, R1 focused independent review, R2 risk-led review. Extra agents are optional, not a default tax. |
| **Knowledge before duplication** | Extend an existing skill or add a reference before introducing another overlapping skill. |
| **Provider independence** | The same engineering method can serve different agent hosts; provider-specific APIs belong to clearly scoped specialists. |
| **Evidence over claims** | Deterministic checks, tests, explicit limitations and repeatable evaluation scenarios. A green CI job is not proof of better model performance. |
| **Safe by default** | No automatic external skill execution, no unapproved merge/deploy, and no implicit overwrite of user-owned files. |

## How it works

AET separates **what an agent needs to know** from **how much process a task warrants**.

```text
                              YOUR TASK
                                  |
                     discover relevant metadata
                                  |
                 registry/skills.yaml + profiles/
                                  |
                     select a focused SKILL.md
                                  |
              +-------------------+-------------------+
              |                                       |
        methods & decisions                      references/
       in the selected skill                 only when necessary
              |                                       |
              +-------------------+-------------------+
                                  |
                         implement & verify
                                  |
             LIGHT / STANDARD / DEEP  +  R0 / R1 / R2
```

The two axes are deliberately independent:

- **Knowledge depth:** metadata → skill → targeted technical reference.
- **Execution rigor:** LIGHT for a narrow reversible edit; STANDARD for ordinary implementation; DEEP for consequential security, persistence or operational risk.

For example, fixing a label should not dispatch three reviewers. A one-line change to a tenant authorization rule may warrant negative security tests and an independent review.

These are **instructions and decision protocols**, not an autonomous enforcement engine. AET's CLI provides deterministic local discovery; actual skill loading and agent behavior depend on the host.

## What's included

| Area | Examples |
| --- | --- |
| **Core & quality** | Task routing, requirements discovery, implementation planning, debugging, testing, secure code review, Git/PR workflows, release readiness |
| **Architecture & backend** | DDD, hexagonal design, API contracts, event-driven systems, FastAPI, Python, TypeScript, persistence, observability |
| **Frontend, UI & design** | React, TanStack Start, Next.js, Vue, accessibility, visual QA, design systems and provider-specific component guidance |
| **Cloud & DevOps** | AWS, GCP, Azure, Cloudflare, Terraform, Kubernetes, CI/CD, IAM, infrastructure operations |
| **Data & AI** | PostgreSQL, Snowflake, Databricks, pipelines, LLM integrations, RAG, MCP, agent orchestration and evaluations |
| **Optional personas** | Execution orchestration, codebase archaeology, adversarial testing, review feedback, incident response and more |

The catalog includes **15 opt-in personas**. Personas are operating modes, not automatically running subagents. A typical installation contains only **5–20 selected skills**, not the entire catalog.

Explore the [catalog](docs/catalog.md), [skill routing](docs/skill-routing.md), [adaptive engineering methodology](docs/adaptive-engineering-methodology.md) and [roadmap](docs/roadmap.md).

## Quick start

**Requirements:** Git, Python **3.12+**, and a working installation of Codex and/or Claude Code if you want to use the skills there. AET's local utilities require PyYAML; ordinary discovery and managed copying do **not** require an LLM API key.

```bash
git clone https://github.com/Tom-dlhy/agent-engineering-toolkit.git
cd agent-engineering-toolkit

python3 -m venv .venv
source .venv/bin/activate             # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt

python scripts/skillctl.py profiles
python scripts/skillctl.py search "FastAPI Pydantic API" --profile python-backend
python scripts/skillctl.py routing-context --profile minimal
python scripts/skillctl.py search "add a protected API endpoint" --json --explain
```

The **existing `task-routing` skill** guides the agent's decisions about technical skills, LIGHT/STANDARD/DEEP and R0/R1/R2 using real task evidence. `routing-context` exports bounded YAML/JSON describing AET's architecture and a selected profile's skills; `search` remains optional lexical discovery. `recommend` abstains from classifying workflow based on prompt keywords. See [routing ownership](docs/skill-routing.md#routing-ownership--agent-decision-deterministic-discovery) and [activation metrics](docs/skill-evaluation-records.md).

### Choose an installation method

| Method | Best for | Who manages updates? |
| --- | --- | --- |
| **A. Managed skills (recommended)** | Adding a focused skill set to an existing project | AET's `manage_install.py` |
| **B. Native local plugin marketplace** | Packaging a reusable curated plugin for supported host plugin workflows | Codex / Claude Code plugin tooling |

**Use one method per host/scope for overlapping skills** to avoid duplicate copies with unclear precedence.

## Install for your coding agent

The examples below run **from the AET repository** after completing Quick start. Replace `/absolute/path/to/your-project` with the repository where you actually code.

### Codex

**Option A — managed project skills (recommended)**

```bash
PROJECT=/absolute/path/to/your-project

# Preview first: no files changed
python scripts/manage_install.py plan \
  --agent codex --project "$PROJECT" --profile web-app

# Install only the selected profile
python scripts/manage_install.py install \
  --agent codex --project "$PROJECT" --profile web-app --apply

# Inspect ownership and drift
python scripts/manage_install.py doctor --agent codex --project "$PROJECT"
```

The installer manages `<project>/.agents/skills/<skill-name>/`. Open the target project with Codex and start a fresh session so its available skills can be discovered. You can explicitly mention a skill when testing, for example: *"Use the fastapi-service skill to review this endpoint."*

To add a **single specialist** without changing your existing selection:

```bash
python scripts/manage_install.py install \
  --agent codex --project "$PROJECT" --skill aws-bedrock --apply
```

**Option B — local Codex plugin marketplace**

If your Codex host supports local plugin marketplaces, build a curated distribution:

```bash
python scripts/package_plugins.py build \
  --profile web-app --name aet-web-app --version 0.1.0 \
  --output dist/aet-web-app --apply --zip

python scripts/package_plugins.py verify --output dist/aet-web-app
codex plugin marketplace add ./dist/aet-web-app
codex plugin marketplace list
```

Adding a marketplace registers a **source**; it does not itself prove that the plugin is enabled. Install/enable `aet-web-app@aet-web-app-local` using your host's plugin browser or supported configuration, then verify it in a new Codex session. Local plugin availability varies by Codex surface and version.

See [OpenAI's official plugin documentation](https://developers.openai.com/plugins/build/plugins).

### Claude Code

**Option A — managed project skills (recommended)**

```bash
PROJECT=/absolute/path/to/your-project

# Preview first
python scripts/manage_install.py plan \
  --agent claude --project "$PROJECT" --profile web-app

# Install to the target project
python scripts/manage_install.py install \
  --agent claude --project "$PROJECT" --profile web-app --apply

# Verify the managed installation
python scripts/manage_install.py doctor --agent claude --project "$PROJECT"
```

The installer manages `<project>/.claude/skills/<skill-name>/`. Start Claude Code inside your target project. Claude can select a relevant installed skill, or you can invoke one explicitly, such as `/fastapi-service`, to confirm it is available.

**Option B — Claude Code local plugin marketplace**

Build the same curated distribution shown above (once), then:

```bash
claude plugin validate ./dist/aet-web-app
claude plugin marketplace add ./dist/aet-web-app
claude plugin install aet-web-app@aet-web-app-local
claude plugin list
```

Restart the Claude Code session and inspect the installed plugin's skills. The example's plugin ID and marketplace name come from `--name aet-web-app`; a different `--name` changes both identifiers. If you use project-scope managed skills, **do not also install an overlapping plugin into that same scope**.

See [Claude Code's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) and [skills documentation](https://code.claude.com/docs/en/skills).

### Updating, repairing and removing managed skills

AET's managed installer records per-file hashes and ownership so it can detect local edits rather than overwriting them silently. The commands below work for **both** hosts—replace `codex` with `claude` as needed.

```bash
# Inspect first
python scripts/manage_install.py doctor --agent codex --project "$PROJECT"
python scripts/manage_install.py update --agent codex --project "$PROJECT"

# Apply reviewed updates
python scripts/manage_install.py update --agent codex --project "$PROJECT" --apply

# Remove only this managed skill (preview, then apply)
python scripts/manage_install.py uninstall --agent codex --project "$PROJECT" --skill aws-bedrock
python scripts/manage_install.py uninstall --agent codex --project "$PROJECT" --skill aws-bedrock --apply
```

`repair` is also available for missing managed files when the original source bytes are present. Additional support for user-level scope, frozen lockfiles, recovery and legacy-ledger adoption is documented in the [managed installer guide](docs/installer-v2.md) and [security runbook](docs/installer-v2-security.md). Existing unmanaged skills are **not** adopted automatically.

## Repository architecture

```text
agent-engineering-toolkit/
├── skills/
│   ├── core/                    # discovery, planning, verification
│   ├── quality/                 # tests, security, reviews, releases
│   ├── architecture/
│   ├── backend/  frontend/  ui/  design/
│   ├── cloud/    data/      data-platforms/
│   ├── ai/       stacks/    growth/
│   └── personas/                # opt-in, self-contained operating modes
│       ...
├── registry/                    # skill inventory, metadata, provenance
├── profiles/                    # curated selections; not monolithic bundles
├── workflows/                   # light.md, standard.md, deep.md
├── agents/                      # optional implementation/review role briefs
├── toolkit/                     # routing, reference loading, safe installer
├── scripts/                     # discovery, packaging, verification CLIs
├── evals/                       # selection and behavioral test specifications
├── tests/                       # deterministic contract and security tests
├── examples/                    # runnable, scoped integration fixtures
└── docs/                        # architecture, audits, maintenance guidance
```

A typical technical skill contains:

```text
skills/backend/fastapi-service/
├── SKILL.md                     # when to use, procedure, decision points
└── references/                  # deeper material loaded selectively
    ├── schemas-and-errors.md
    ├── security-and-trust-boundaries.md
    └── testing-and-deployment.md
```

The full library stays on disk. Installed profiles expose a selected subset. The model should read only the relevant skill body and the technical references required for the task. **Library size is not the same as session context size.**

Read the [architecture](docs/architecture.md) and [progressive expertise design](docs/progressive-expertise.md) for the full contract.

## Measuring whether skills actually help

AET includes an **opt-in A/B/C engineering benchmark harness** comparing a clean agent, focused technical skills, and full methodology on identical test fixtures. Its local analyzer checks paired evidence and blocks automatic promotion. The benchmark now preserves before/after source snapshots and diffs for independent review, with offline SHA-256 verification before promotion. Native model runs are never triggered by CI and require explicit budget and disposable-host approval. See [Evidence-driven evaluations](docs/evidence-driven-evaluations.md) for the experimental contract and limitations.

## Verification and security

This repository includes catalog checks, tests for several executable examples, context-budget guardrails and cross-platform installer tests.

```bash
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/context_budget.py --all --budget 2500
```

The context budget is a **characters ÷ 4 proxy**, not an exact token bill. The project also includes evaluation fixtures, but most native agent behavior tests still require actual Codex/Claude sessions and observed outputs.

AET does **not** claim measured token savings, universal model compatibility, guaranteed code correctness, or production security certification. Native plugin manifests and packaged files are tested structurally; verify actual loading on your host before treating a distribution as accepted.

External skills must pass review for overlap, licensing, scripts, dependencies and prompt-injection risk before inclusion. There is no automatic external skill execution, credential access or unapproved production action.

See [security](SECURITY.md), [contributing](CONTRIBUTING.md) and the [roadmap](docs/roadmap.md).

## Contributing

Useful contributions improve an existing skill's **behavior, technical depth, activation precision or test coverage**. New skills should solve an independent problem—not rename an existing responsibility.

Changes are developed through focused PRs and validated in CI. **Passing CI or being mergeable never authorizes an automatic merge.**

## License

[MIT](LICENSE). Original first-party material; external projects may inform the methodology without their executables or skills being silently imported.

---

<div align="center">

**A large engineering library should make an agent more capable—not every task more expensive.**

</div>
