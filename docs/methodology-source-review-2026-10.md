# Methodology deepening — upstream source review (2026-10-12)

## Intent and governance decision

Decision: **EXTEND and REFERENCE**, not CREATE. Fourteen existing skills
cover six responsibilities and their existing reference trees already
provide progressive disclosure. No imported hooks, external execution
scripts, extra personas or new skills are necessary. The AET charter
requires responsibility ownership, bounded context, model neutrality,
positive and negative activation examples and verifiable behavior.

This is an original operational adaptation of ideas found in public
GitHub repositories. It is NOT a claim of reproducing all upstream
methods, their tests or their practical performance. Repository links
below identify upstream code at immutable revisions.

| Upstream repository and pinned revision | Examined material | Transferable method | Explicit non-transfer |
|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3) | systematic-debugging, test-driven-development, brainstorming | Observe -> isolate -> falsify -> fix; meaningful RED/GREEN; bounded discovery | Mandatory TDD/interviews for trivial edits; platform-specific hooks |
| [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator) | skill-creator and evaluation guidance | Compare frozen old/new skill on paired cases, blind output grading, verify trigger selection | Claude-specific scripts, agent tools and claims without actual runs |
| [trailofbits/skills](https://github.com/trailofbits/skills/tree/442fc9d6c89b1e937e6f7a477e7071ea75fcbea4) | differential-review, audit-context-building | Understand assumptions/guarantees, diff blast radius, exploitable-path hypotheses and false-positive checks | Mandatory full audits for cosmetic diffs; executing external audit scripts |
| [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/70ddff7fab9d4d49743d221b56d761cff58048d0) | devops-rollout-plan, agent-governance and agent-architecture catalog | Preflight, rollback, verifiable go/no-go, design-to-contract | Forced release process on docs-only edits, autonomous production deployment |

The reviewed methods are **concepts**, not verbatim source copies.
Upstream licenses vary by repository and component. Future verbatim
reuse requires separate path-specific license inspection and preserved
attribution/NOTICE as applicable; this PR does not vendor external code.

## Impact by domain and skill

| Domain | Skills improved | What changed |
|---|---|---|
| P0 Routing and eval | task-routing, llm-evaluation | shortlist/disambiguation, dynamic selection, frozen old-skill baseline, paired native run/negative activation, cost-per-success |
| P1 Diagnosis & testing | systematic-debugging, test-strategy, test-adversary | causal first-invalid-boundary, falsifiable hypotheses, correct RED assertions, realistic failure injection, mutation oracle |
| P1 Discovery and architecture | requirements-discovery, architecture-decision | brief high-information questions, approved acceptance, hard constraints, status quo and measurable revisit triggers |
| P1 Security | secure-code-review, agent-tool-safety | source/guard/sink paths, history/consumers, untrusted tool instructions, bound approval and false-positive checking |
| P1 CI/CD & release | ci-cd-engineering, release-readiness, incident-commander | fork/trigger trust matrices, artifact identity, preflight, migration compatibility, reconciliation and rollback |
| P2 Code continuity | codebase-archeologist, context-curator | bounded assumption/guarantee dossiers, consumer radius, SHA reconciliation, safe resumability |

Each skill's SKILL.md has an operational method and LIGHT/STANDARD/DEEP
decision guidance; existing leaf references deepen evidence procedures
only when selectively loaded. Personas remain self-contained with no
local reference leaves or profile growth. Existing routing keywords,
profiles, registry and skill count are deliberately unchanged.

## Measurable evaluation contract (not yet executed against native agents)

1. Offline: repository structural and role/candidate metadata tests,
   plus pure Python external-run report pairing validation.
2. Host: use evals/methodology-depth.yaml with an *actual* Codex/Claude
   environment, skill-loading and tool traces, before/after artifacts,
   accepted test oracles, exact baseline/candidate revisions and model IDs.
3. Report: candidate and baseline task PASS counts, false activations,
   critical regressions, reviewer cost, latency and host-reported tokens
   only when all compared records have real measurements.
4. Gate: no improvement claim from scenario text alone; no production
   release from a model's confidence. Treat missing independent R2 or
   missing approval as blocked, even when offline tests pass.

The helper scripts/summarize_skill_evals.py reads a JSON array of
*externally collected* observations and checks pair comparability.
It neither spawns agents nor verifies the authenticity of run IDs or
test transcripts. Source evidence must be checked separately.

Example inputs (two records, one task):

~~~json
[
  {
    "task_id":"case-1", "variant":"baseline", "run_id":"run-old",
    "input_sha":"fixture-sha", "host":"codex", "model":"pinned-model",
    "tool_config":"sandbox-read", "skill_sha":"old-skill-sha",
    "status":"PASS", "expected_skill":"systematic-debugging",
    "activated_skill":"systematic-debugging", "critical_violation":false,
    "review_calls":1, "tokens":1400, "latency_ms":20000
  },
  {
    "task_id":"case-1", "variant":"candidate", "run_id":"run-new",
    "input_sha":"fixture-sha", "host":"codex", "model":"pinned-model",
    "tool_config":"sandbox-read", "skill_sha":"new-skill-sha",
    "status":"PASS", "expected_skill":"systematic-debugging",
    "activated_skill":"systematic-debugging", "critical_violation":false,
    "review_calls":0, "tokens":1100, "latency_ms":16000
  }
]
~~~

The numbers are **illustrative schema values only**, not measured
results. To compare real runs, substitute verified transcript-backed
records, then:

~~~bash
python scripts/summarize_skill_evals.py --records path/to/observed-runs.json
~~~

Do not use this output as stand-alone proof of a skill's actual
activation or of authorization. It is an audit-friendly summary,
not a host evaluation runner.

## Limits / next evidence

The source review verifies method existence in public repos, and
repo CI verifies content/contracts, but neither establishes behavioral
parity with upstream tools. Test the methods with held-out tasks, real
native installer/activation, intentionally conflicting inputs,
run-to-run variance and actual token telemetry. The lexical routing
engine remains advisory and is NOT automatically made semantic by
longer skill documentation. Additional retrieval improvements require
their own observed evaluation and separate code review.
