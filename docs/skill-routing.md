# Discovering skills without blowing the context window

This toolkit distinguishes **library size**, **installation profile size** and **activation size**.

1. The library holds 178 local `SKILL.md` files and may grow to hundreds.
2. A profile installs only a curated subset (5–20 skills).
3. The model sees a brief name/description, not a full skill body.
4. Only 1–3 directly relevant skill bodies should be read for ordinary tasks.
5. Technical references/assets/scripts are read only if the task actually requires them; the 15 opt-in persona skills instead carry their **entire method in one SKILL.md** without references.

The CLI uses deterministic word matching, not LLM calls. It reads local files as *program input*; it does not paste all their bodies into model context.

## Typical workflow

The managed Installer v2 is preferred; the legacy copy-only CLI is deprecated. See [Installer v2](installer-v2.md) for safe maintenance commands.


~~~bash
python scripts/skillctl.py profiles
python scripts/skillctl.py search "Design an accessible React dashboard" --profile web-app
# AET architecture + scoped metadata; agent decides skills, workflow and review
python scripts/skillctl.py routing-context --profile cloud-engineering
python scripts/skillctl.py routing-context --skill database-selection --skill task-routing
# Optional lexical candidates and uncertainty diagnostics, never automatic activation
python scripts/skillctl.py search "choisir une base de données pour mon SaaS" --json --explain
python scripts/skillctl.py show responsive-visual-qa

# Compare approximate metadata footprints
python scripts/context_budget.py --all
python scripts/context_budget.py --profile ui-ux-design --activated responsive-visual-qa

# Profile installation without network access
python scripts/manage_install.py install --profile ui-ux-design --agent claude --project /my/app
python scripts/manage_install.py install --profile ui-ux-design --agent claude --project /my/app --apply
~~~

Styles such as `bento-grid` and `glassmorphism` are **catalog opt-ins**, not part of the general `ui-ux-design` profile. Select them explicitly via `--skill` when a brief requires the technique; do not treat a design request as automatic permission to add effects.

## Persona activation versus workflow and technical knowledge

Personas are deliberate *operating modes*, not technical source-of-truth skills and not automatically launched subagents. A user can explicitly request `grill-master`, `test-adversary` or `learning-mentor` while a relevant technical skill supplies API knowledge. Use at most one primary persona in an ordinary task; compose another only if its **independent outcome** is requested, and apply the project's LIGHT/STANDARD/DEEP safety process separately. All 15 are **opt-in** and deliberately absent from general installation profiles. Installed availability varies by host; this repository's discovery does not imply native Claude/Codex invocation.

### Leadership-persona routing boundaries

- `head-of-engineering`: ongoing multi-team engineering delivery/ownership, not a single approved implementation plan (`execution-orchestrator`).
- `privacy-compliance-lead`: purpose-level privacy processing, DPIA screening, vendor transfers and data-subject rights, not a one-endpoint code security audit or qualified legal signoff.
- `branding-lead`: cross-medium brand identity, logo system and **promotional-video creative direction**; one-off logo concepts go to `brand-identity-visualization`, interactive UI motion to `interaction-motion`. An interactive web animation is **not** video mastering.

## Snowflake platform-specific selection

- `snowflake-query-performance` diagnoses Snowflake Query Profile, warehouses and credits, not PostgreSQL EXPLAIN or metric definitions.
- `snowflake-data-pipelines` owns Snowpipe, Dynamic Tables, Streams, Tasks and Snowflake replay; `data-pipeline-quality` still owns general source contracts.
- `snowflake-snowpark-ml` owns Snowflake ML Model Registry, LightGBM/Snowpark and feature store, not Cortex text-to-SQL.
- `snowflake-cortex-ai` owns Snowflake Agents/Analyst/Search/semantic views, not Bedrock Converse or generic RAG architecture.
- `snowflake-security-governance` owns Snowflake SQL grants, masking and row access policies, not cloud IAM, GDPR legal signoff or Cortex answer evaluation.

All five are opt-in and absent from existing installation profiles. Exact matching is still lexical; the local finder is not a semantic multilingual router. See [platform governance](snowflake-platform-audit.md).

## Databricks specialist selection (opt-in)

- `databricks-spark-delta` owns Spark query plans, AQE/Photon, Delta transactions and liquid clustering, not Snowflake warehouse profiling.
- `databricks-lakeflow-pipelines` owns Auto Loader, Lakeflow Jobs and AUTO CDC state/replay, not generic source Debezium or Snowpipe.
- `databricks-unity-catalog` owns asset RBAC, governed ABAC, workspace bindings and sharing, not Unity Gateway model request traffic.
- `databricks-mlflow-mlops` owns MLflow 3 training/registry/serving lifecycle, not Snowpark ML Model Registry.
- `databricks-automation-bundles` owns CI/CD config/state/CLI and deployments for Databricks assets, not generic Terraform providers.
- `databricks-ai-governance` owns Unity Gateway models/MCP/tool/service policies, not Cortex Agents or Bedrock Converse.

No new default profile contents and no automatic activation. Exact selection is lexical and must be tested against UI, Data, Cloud and Snowflake negative requests. See [Databricks audit](databricks-platform-audit.md).

## Workflow policy

| Level | Purpose | Typical skill activation | Agent strategy |
| --- | --- | --- | --- |
| Light | Tiny docs/UI/bug fixes | 0–1 | Single agent, targeted tests |
| Standard | Normal features/refactors | 1–2 initially | Single implementer + review on demand |
| Deep | Changed trust/data boundary, irreversible writes or unsafe rollback | 2–3 initially, additional by evidence | Explicit plan, risk checks, optional independent reviewers |

Use `workflows/<level>.md` for the full protocol. The selector is *advisory*. It cannot authorize destructive actions, deployment or privileged cloud operations.

## Token measurement caveats

`context_budget.py` uses `characters / 4`, a rough proxy for text size. Different models, languages and tools tokenize differently. Actual token consumption also includes conversation history, tool output, loaded references, subagent sessions and caching effects. The resulting number is not an exact charge or weekly quota estimate.

CI rejects profiles if this rough core + metadata estimate exceeds 2500 tokens or the installed count exceeds 20. This is a **guardrail**, not a guarantee about real consumption.

## Routing ownership — agent decision, deterministic discovery

**`task-routing` is the existing decision skill.** Do not add a duplicate
`choose_skill`. When selection is ambiguous or consequential, the agent must
inspect the user request, actual repository, affected contracts, side effects,
reversibility, available tools and explicit permissions. It then decides:

1. Zero or one primary specialist and only genuinely independent helpers.
2. LIGHT / STANDARD / DEEP as *execution rigor*.
3. R0 / R1 / R2 as *review assurance*, separately from skill count.

A tiny authorization change may need DEEP/R2; a documentation typo mentioning
authentication does not. No keyword or model decision grants merge/deploy/
destructive permission. If facts are missing, ask for context or state that
classification is pending; do not silently assume safety.

### Machine-readable architecture and available skills

```bash
python scripts/skillctl.py routing-context --profile minimal
python scripts/skillctl.py routing-context --profile python-backend --json
python scripts/skillctl.py routing-context --skill database-selection --skill task-routing
```

The **YAML by default** is generated from the existing registry and each
skill's frontmatter description. There is no second copy of the 178 skill
definitions to keep synchronized. Output includes the contract and workflow
paths, review levels, the scoped skills' paths, positive activation scopes,
exclusions and safety cautions. The command requires an explicit profile or
skill list and is capped at 20 entries; it does not bulk-load bodies or
references. Profiles describe AET catalog membership, **not proof that a
specific host installed or activated the skills**. The host's installed skill
metadata should be preferred when already available.

### CLI discovery remains a fallback, not a workflow engine

`search` and `discover` provide explainable **lexical candidates** with
exclusions, checks and uncertainty. They cannot understand arbitrary French,
negation or nuanced intent. `search --json` retains its legacy list shape;
`--explain` exposes additional diagnostics.

`recommend` still prints candidates for compatibility, but its workflow
output now explicitly abstains. `workflow_advice(query)` returns
`workflow=unclassified`, `risk=unknown`,
`source=agent_decision_required` for free text.
The legacy `suggest_workflow(query)` tuple also returns `unclassified`
rather than misrepresenting a keyword guess as a risk assessment.

If a caller supplies actual nonempty structured impact/scope observations,
`workflow_advice(query, observed=ChangeSignals(...))` delegates to the existing
`adaptive_policy.assess`. Those observations are caller-reported, not
independently verified. Empty/default `ChangeSignals` or flags reporting only
tool/reviewer availability **do not establish low risk**: the API abstains.
Neither output is authorization.

The PR #38 routing regression fixtures remain **negative/positive discovery
tests**, not a claim that offline code can measure model judgment. Evaluating
the agent's choice of skills, workflow and cost requires real host traces and
held-out tasks.

See [activation evidence records](skill-evaluation-records.md) for separately
tracked correct, missed, unwanted, unknown and not-run activation states.

## Quality and selection

No skill maturity/rank metadata influences discovery. The registry's lexical scores indicate candidate relevance only and cannot assert competence or justify automatic installation. All skills use the same quality contract, while selected reference depth depends on the task. See [Core audit](core-refactor-audit.md).
