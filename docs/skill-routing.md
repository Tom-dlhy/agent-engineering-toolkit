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
python scripts/skillctl.py recommend "Migrate production IAM permissions" --profile cloud-engineering
# Evidence, exclusions and uncertainty; never an activation/authorization decision
python scripts/skillctl.py recommend "choisir une base de données pour mon SaaS" --json --explain
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

## Candidate evidence and uncertainty

The finder retains deterministic weights for names, keywords, domains and **positive**
description text. Description text starting at `Do not`, `Don't`, `Not for`,
`Avoid using` or `Ne pas utiliser` is separated and never adds positive score.
Only activation-scope markers (`Do not use`, `Do not apply`, `Do not substitute`, etc.)
can suppress a candidate; procedural warnings such as `Do not assume` cannot.
Fully matched exclusion clauses with at least two meaningful terms suppress a
candidate; partial matches become an unfavorable scope check. This conservative
parser does not understand every conditional/negative construction. Metadata
exclusions still need human/agent review.

A small, reviewed alias set handles database compounds (`base de données`,
`bases de données`, `data base`) and selected FR/EN choice/diagnosis/action terms.
It is **not general translation**. Database compounds no longer contribute `base`
to Base UI. Debugging favors diagnostic keywords; `*-selection` candidates require
explicit choice/comparison and technical-domain evidence; `selection` alone
cannot recommend every choice specialist. Simple documentation spelling edits can
return zero skills. Negative query clauses introduced by `do not use`, `without`,
`sans`, etc. are removed from positive scoring until punctuation or `but`/`mais`/`and`/`et`.
Clause scope remains heuristic; rephrase complex mixed intentions or inspect them
manually.

`discover(query, catalog, allowed=..., limit=...)` returns:

- `candidates`: scores and favorable `reasons`, plus `unfavorable` checks.
- `excluded`: named candidates and matched exclusion reasons.
- `uncertainty`: `lexical`, `ambiguous` (tied leaders or unfavorable evidence for
  the leader), or `insufficient` (no candidates). These are labels, not probabilities.
- `required_checks`: inspect actual task/stack before activation; **zero skills is valid**.

An unidentified component library remains a stack check; installed visibility is
not evidence that the user selected it. A higher score does not settle conflicting
stacks, competence or permission. `allowed` still restricts discovery to a profile;
`limit < 1`, empty requests and noise yield no candidates.

Compatibility: `Skill` construction is unchanged; `Match` adds a defaulted
`unfavorable` field. `search(...)` still returns a list of matches and
`suggest_workflow(query)` still returns `(workflow, reason)`. `search --json` retains
its list/row shape. Opt-in `search --json --explain` returns a diagnostic object.
New `recommend --json` returns that object with `workflow`; text `--explain`
prints the same exclusions, uncertainty and required checks. No discovery command
activates/installs a skill, executes its scripts or makes network/model calls.

## Workflow evidence, not authorization

`workflow_advice(query)` inspects requested actions and consequences together.
An authentication-documentation typo is LIGHT; restricting a tenant lookup or
removing an ownership filter suggests DEEP; a database choice suggests STANDARD.
An explanation about irreversible migration is not migration execution. Compound
requests retain the strongest indicated consequence per clause: updating docs
alongside an authorization fix cannot downgrade the fix. Coordinated objects
inherit the preceding action when they have no action of their own. A
localized reversible refactor may be LIGHT; unverified scope remains explicit.

Text-derived suggestions always have `source=request_heuristic`, with `risk=potential`
or `insufficient`, even for DEEP. They cannot confirm a boundary change, determine
real rollback safety or authorize execution. Inspect the diff, data and permissions.
This is a bounded lexical heuristic, not a reliable security assessment. Unknown
impact can yield a tentative LIGHT default marked insufficient; it must **not** be
read as a safety verdict.

For actual observed facts, callers can use
`workflow_advice(query, observed=ChangeSignals(...))`, which delegates to
`adaptive_policy.assess` without fabricating observations from the text.
It sets `source=observed_change_signals`, `risk=confirmed` for observed DEEP risks
or `observed` for other observed outcomes, and exposes unmet gates as required
checks. This reports caller-supplied facts, not independently verified code and
not authorization. The structured policy's review/execution rules are unchanged.

## Router failure modes and validation

- Accents and selected FR/EN aliases are supported; unconstrained French/English
  syntax, other languages, polysemy and compound negations can still misroute.
- Generic overlaps and description syntax can hide ambiguity. Inspect metadata,
  user-selected stack and exclusions before applying any recommendation.
- Scores/uncertainty are not confidence percentages, expertise certificates or
  evidence of actual native invocation.
- Maintain positive, negative, ambiguity and natural-language cases alongside
  registry changes. Do not bulk-add synonyms without measuring false positives.
- [Regression fixtures](../evals/routing-regressions.yaml) test the five audited
  failures, FR/EN variants and candidate inclusion/exclusion properties. Existing
  domain routing suites remain required. These deterministic checks do not measure
  Codex/Claude behavior or performance gains.
- Paired native evaluation records use the separate
  [activation evidence contract](skill-evaluation-records.md); missing telemetry is
  unknown, not an observed activation failure.

## Quality and selection

No skill maturity/rank metadata influences discovery. The registry's lexical scores indicate candidate relevance only and cannot assert competence or justify automatic installation. All skills use the same quality contract, while selected reference depth depends on the task. See [Core audit](core-refactor-audit.md).
