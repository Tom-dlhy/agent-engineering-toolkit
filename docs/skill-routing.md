# Discovering skills without blowing the context window

This toolkit distinguishes **library size**, **installation profile size** and **activation size**.

1. The library holds 116 local `SKILL.md` files and may grow to hundreds.
2. A profile installs only a curated subset (5–20 skills).
3. The model sees a brief name/description, not a full skill body.
4. Only 1–3 directly relevant skill bodies should be read for ordinary tasks.
5. References/assets/scripts are read only if the task actually requires them.

The CLI uses deterministic word matching, not LLM calls. It reads local files as *program input*; it does not paste all their bodies into model context.

## Typical workflow

~~~bash
python scripts/skillctl.py profiles
python scripts/skillctl.py search "Design an accessible React dashboard" --profile web-app
python scripts/skillctl.py recommend "Migrate production IAM permissions" --profile cloud-engineering
python scripts/skillctl.py show glassmorphism

# Compare approximate metadata footprints
python scripts/context_budget.py --all
python scripts/context_budget.py --profile ui-ux-design --activated glassmorphism

# Profile installation without network access
python scripts/install_profile.py --profile ui-ux-design --agent claude --project /my/app
python scripts/install_profile.py --profile ui-ux-design --agent claude --project /my/app --apply
~~~

## Workflow policy

| Level | Purpose | Typical skill activation | Agent strategy |
| --- | --- | --- | --- |
| Light | Tiny docs/UI/bug fixes | 0–1 | Single agent, targeted tests |
| Standard | Normal features/refactors | 1–2 initially | Single implementer + review on demand |
| Deep | Security, auth, migrations, architecture, prod | 2–3 initially, additional by evidence | Explicit plan, risk checks, optional independent reviewers |

Use `workflows/<level>.md` for the full protocol. The selector is *advisory*. It cannot authorize destructive actions, deployment or privileged cloud operations.

## Token measurement caveats

`context_budget.py` uses `characters / 4`, a rough proxy for text size. Different models, languages and tools tokenize differently. Actual token consumption also includes conversation history, tool output, loaded references, subagent sessions and caching effects. The resulting number is not an exact charge or weekly quota estimate.

CI rejects profiles if this rough core + metadata estimate exceeds 2500 tokens or the installed count exceeds 20. This is a **guardrail**, not a guarantee about real consumption.

## Router failure modes

- A purely lexical query may miss synonymous technical terms.
- No match should yield **no recommendation**, not a fabricated match.
- The keyword registry is edited and reviewed alongside a new skill.
- Negative triggers in each skill description remain authoritative: a high lexical score alone should not force an invocation.
- The CLI is intentionally non-mutating. It never installs tools, executes skill scripts or makes network calls.

## Quality and selection

No skill maturity/rank metadata influences discovery. The registry's lexical scores indicate candidate relevance only and cannot assert competence or justify automatic installation. All skills use the same quality contract, while selected reference depth depends on the task. See [Core audit](core-refactor-audit.md).
