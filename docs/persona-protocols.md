# Operational personas — design, activation and evaluation

**Scope:** independent behavioral operating modes, not new framework APIs, infrastructure services or mandatory personalities. **15 persona skills**, separate `personas` domain, **no skill-local references**, no new profile and no auto-activation. Each is a self-contained `SKILL.md`, read in full **only if explicitly selected**.

## Architectural contract

The toolkit has three independent axes:
1. **Technical expertise** — technical skills such as `fastapi-service`, `database-selection` and `secure-code-review` define domain mechanisms, APIs and safe technical implementation.
2. **Operating mode** — one explicitly selected persona controls the *how*: interview, critique, archaeology, decision, collaboration, incident or learning. Persona instructions **cannot overrule** factual technical skills, user/project instructions, permissions or approval gates.
3. **Workflow rigor** — LIGHT / STANDARD / DEEP governs verification, review and risk. A persona does **not** force DEEP on an otherwise trivial user request, and is not a new execution engine.

Personas differ from `agents/*.md`: those are short optional role briefs (planner/implementer/reviewer/security-reviewer), whereas a persona is a full opt-in **behavioral methodology** that can run inline with a single agent. It never assumes Claude/Codex subagent tools exist.

### Key design decisions (governance v2)

- **CREATE category `personas`:** 15 coherent skills (12 initial and 3 independent leadership roles) with nontechnical, independently requested behavioral outcomes. Folding them into `core` would confuse foundational always-available procedures with long opt-in modes. No new category just for one decorative persona.
- **CREATE 15, not import:** use concept-level inspiration, write all instructions from scratch. No upstream scripts, prompts, hooks, assets or tool-specific AskUserQuestion assumptions were copied.
- **REUSE technical skills:** all authoritative implementation knowledge remains in the original 12 technical domains.
- **EXPLICIT activation:** none of the fifteen is added to one of the 20 existing profiles by default, keeping metadata/context budgets unchanged. Native agent auto-routing depends on host installation; local `skillctl` provides only lexical suggestions.
- **SELF-CONTAINED:** no references folder, docs fetch or network call is needed to execute these methodologies. Length is justified by operational procedure; no arbitrary token-minimum imposed on normal technical skills.
- **HUMAN OWNERSHIP:** no persona may silently authorize credentials, user messages, live incident changes, merges, deployments, deletion, paid actions or publication.

## Persona/overlap decision matrix

| Persona | Only when needed | Owns distinct deliverable | Existing expert / boundary |
|---|---|---|---|
| `grill-master` | User explicitly wants sustained interrogation | Confirmed decision tree and open-decision register | `requirements-discovery` only asks *blocking* questions for ordinary work |
| `devils-advocate` | User asks to contest a concrete proposal | Steelman, falsifiers and conditional verdict | Architecture/review skills provide verified technical facts, not adversarial stance |
| `codebase-archeologist` | Need extensive understanding *before change* | Trace-backed architecture map and change blast radius | `systematic-debugging` isolates an observed defect |
| `scope-guardian` | User wants active YAGNI/scope patrol | Scope ledger (in/defer/out/escalate) | `requirements-discovery` establishes requirements, not drift tracking |
| `test-adversary` | User requests failure-seeking challenge | Invariant threat matrix, executable negative evidence or clear blocked status | `test-strategy` designs suite; `secure-code-review` assesses vulnerabilities |
| `execution-orchestrator` | Approved *multi-step execution* benefits from coordination | Task graph, worker packets, integration ledger | `agent-orchestration` designs agent products; `agents/planner` is short role brief |
| `product-sparring-partner` | Want product/SaaS/business viability critique | Problem/assumption tests and decision memo | Growth marketing owns messaging; `devils-advocate` critiques broader proposals |
| `review-feedback-arbiter` | Already have reviewer comments to adjudicate | Accept/modify/reject evidence-by-comment | `agents/reviewer` generates feedback; `git-pr-workflow` performs PR operations |
| `context-curator` | Prepare handoff/cross-session recovery | Resume packet with evidence/supersession | `codebase-archeologist` investigates repo, does not own context provenance |
| `incident-commander` | Time-sensitive active/simulated incident | Timeline, containment decisions, recovery/communications gates | `systematic-debugging` diagnoses root cause, SRE executes provider procedures |
| `decision-arbiter` | Need clear conditional winner from alternatives | Hard-veto tradeoff decision record | `technology-tradeoffs` researches technology facts |
| `learning-mentor` | User specifically wants guided mastery | Predict/act/explain/transfer practice and skill-specific evidence | Technical skill supplies mechanics; don't withhold direct requested implementation |

| `head-of-engineering` | Engineering leadership across initiatives, not one task | Engineering mandate, capacity/ownership, delivery health, 30/60/90-day operating improvements | `execution-orchestrator` runs one approved plan; architecture and SRE skills handle implementation |
| `privacy-compliance-lead` | Product/organization privacy governance, processing risks, rights and release gates | Purpose-level inventory, DPIA screen, vendor/rights controls and qualified legal approvals | `secure-code-review` owns code defects; DPO/lawyer owns formal conclusions |
| `branding-lead` | Brand identity **across** logos, campaign media and promotional video | Creative north star, logo system, storyboard/treatment, asset ledger, cross-channel QA | `brand-identity-visualization` owns concept renders; `interaction-motion` owns UI motion **not video editing**; design-system owns tokens |

### Why no additional "senior reviewer", "security reviewer", "debugger", "verification gatekeeper" personas?

Their primary responsibilities already exist as `agents/reviewer.md`, `agents/security-reviewer.md`, `systematic-debugging`, `secure-code-review`, `verification-before-done` and `release-readiness`. Do not duplicate them under a flashy identity label. The 15 created here are **opt-in behaviors**, and their descriptions explicitly exclude adjacent routine tasks.

## Invocation and portability

~~~bash
# Read the entire selected persona locally (no third-party request)
python scripts/skillctl.py show grill-master
python scripts/skillctl.py search "grill design decision tree"
python scripts/skillctl.py search "test adversary negative invariant"
python scripts/skillctl.py search "decision arbiter options tradeoffs"

# Preview exact single-skill installation (no write)
python scripts/install_profile.py --skill grill-master --agent codex --project /path/to/project
# Explicitly apply only if the operator approves the installation
python scripts/install_profile.py --skill grill-master --agent codex --project /path/to/project --apply
# Equivalent target adapter supported for Claude Code
python scripts/install_profile.py --skill test-adversary --agent claude --project /path/to/project
~~~

A user can also explicitly name a persona in their agent prompt, but host behavior varies. **Do not assume a GitHub registry entry automatically becomes available to an installed agent.** When combining persona with a technical skill, start with **one primary persona** and add technical expertise independently. A secondary persona is allowed only when independently relevant; the primary persona's stop/permission rules remain binding.

### Worked composites

- "Grill my SaaS design, especially client access" -> **grill-master** (one consequential question at a time) with opt-in `authentication-solution-selection` for factual provider/security tradeoffs *after identity requirements are known*.
- "Try to break the order API" -> **test-adversary** + `fastapi-service`/`python-persistence` as needed, never automatic external penetration testing.
- "Inspect this legacy project before rewriting auth" -> **codebase-archeologist**. Only after understanding the contracts should `authentication-solution-selection` propose an alternative.
- "Arbitrate comments from two PR reviewers" -> **review-feedback-arbiter**; reproduce claims before edits, enforce owner merge approval.
- "Teach me SQL transactions rather than just doing my homework" -> **learning-mentor** + the DB specialist appropriate to installed engine.
- "Lead the engineering team's release quality and capacity over the quarter" -> **head-of-engineering**, not orchestration of one task.
- "Evaluate privacy risks of marketing cookies and AI-provider support transcripts" -> **privacy-compliance-lead**, with review by applicable DPO/legal authority.
- "Direct our logo refresh and a 30-second promotional video across web/social" -> **branding-lead**, with production delegated to relevant visual and media tools.
- "Fix one header typo" -> **no persona**; direct LIGHT execution.

## Behavioral evaluation contract

Static metadata and content checks prove **format, coverage and intended routing**, not model adherence. `evals/persona-routing.yaml` specifies held-out *unexecuted* positive, negative and protocol-quality scenarios. During future real-agent evaluation, compare baseline and persona-enabled runs **under controlled task, repo, tools and model configuration**, ideally with independent/blinded rubric scoring where feasible. Report:
- Persona activation precision / false positives and negative routing;
- Protocol adherence (one-question drill, approval gates, evidence labels, state transitions);
- Outcome quality (genuinely resolved decisions, verified bugs, correctly rejected feedback, reconstructable handoff);
- Harm/inefficiency (unnecessary questions, invented facts, hallucinated tests, excess changes, context/latency);
- Real token counts only when surfaced by host; local chars/4 is just a proxy.

Score each case with 0/1 for **explicit safety/permission gates** and a task-specific 0–3 scale for decision quality and usefulness. Run ablations and report confidence/limitations; never promote unrun scenario YAML into "evaluated expert" status.

## Source and provenance audit (conceptual synthesis, not import)

Reviewed upstream as of 2026-10-12:
- **obra/superpowers**, commit `bb92a77741419a4ab5f06e711a283343f1ada0c3`: interactive brainstorming, writing plans, subagent-driven execution, independent review and verification before completion. Repository license MIT. Concepts that informed methodology: **decision-first clarification, bounded tasks, adversarial review and evidence before success claims**. None of its files, scripts or verbatim prompts are included in persona SKILL.md.
- **robmitt/grill-me-skill**, commit `31d61d68fc406f8cc2a944b4b10e6f23877720f1`: focused one-question-at-a-time interview and dependent-branch resolution. No LICENSE file found in the inspected repo root, so this implementation **does not copy/adapt its SKILL.md**. The idea is re-authored independently and tool-agnostically; no AskUserQuestion tool dependency.

Any future *actual copying* requires file-level license and provenance review (governance v2). The persona SKILL.md files intentionally contain **no external documentation links or reference leaves**. External citations are here only as authorship/provenance metadata.

## Future maintenance

For each persona change, require one expected activation, one negative activation, at least one adversarial behavioral fixture, explicit stop condition, no unsupported claims of actual tool behavior and merge approval. If repeated real-agent evaluations reveal indistinguishable outcomes between two personas, **EXTEND/MERGE/REJECT** appropriately rather than preserving catalog size.

## Leadership-persona source check and domain separation (2026-10-12)

The three newly requested methods are independently authored and
self-contained in their own SKILL.md, without external references, imported
prompts, plugins, tools or production assets. They cover **organizational
or cross-media operating decisions**, not repeatable framework implementation.

- **Engineering leadership:** delivery throughput must be evaluated together
  with stability, rework and sustainable team experience. Team/system-level
  DORA measurement is useful, but individual developer ranking by commits,
  story points or deployment count is not responsible engineering governance.
  Official background: https://dora.dev/guides/dora-metrics/.
- **Privacy compliance:** processing purpose, accountability, minimization,
  default protection, rights and DPIA screening are distinct from a code
  security audit. An AIPD can be required for high-risk processing; assessment
  and legal signoff remain context-dependent. Official background:
  https://www.edpb.europa.eu/documents/guideline/guidelines-42019-on-article-25-data-protection-by-design-and-by-default_en
  and https://www.cnil.fr/fr/RGPD-analyse-impact-protection-des-donnees-aipd.
- **Brand and video:** the leadership persona owns a unified identity and
  campaign creative system, including timed video treatments, licensed assets,
  captions, alternate formats, QA and honest delivery status. Existing
  `interaction-motion` documents **interactive web animation**, not the
  creation/export of promotional videos. W3C web motion guidance:
  https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.

**Negative routing:** a simple logo concept render belongs to
`brand-identity-visualization`; implementing an animated button uses
`interaction-motion`; fixing a single IAM/auth bug uses the technical
security skill; coordinating a single agreed coding plan uses
`execution-orchestrator`. No persona can claim that it has rendered a
video, obtained licensed assets, certified GDPR compliance, measured an
engineering team's performance or merged code without direct evidence.

Future held-out real-agent testing should verify these exclusions, source
integrity, decision output quality, stop gates and real token impact. Static
catalog and CI tests are not proof of behavioral improvement.

## Adaptive implementation and code-review handoff

execution-orchestrator now distinguishes INLINE, SUBAGENT-DRIVEN and proven independent PARALLEL execution without turning subagent count into a quality metric. Its R0/R1/R2 selection comes from task-routing and the risk of the actual diff. review-feedback-arbiter handles comments against current code with ACCEPT/MODIFY/REQUEST EVIDENCE/REJECT/DEFER/ALREADY RESOLVED, bounded re-review and test evidence. Both remain opt-in personas with no local reference leaves or mandatory profile addition. The independent Core implementation-planning skill provides executable task contracts; see [adaptive methodology](adaptive-engineering-methodology.md). No model-run evidence or automatic native activation is implied by these definitions.
