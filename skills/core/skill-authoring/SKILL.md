---
name: skill-authoring
domain: core
version: "0.3.0"
description: >-
  Use when creating, changing, splitting, importing or governing an Agent Skill,
  its activation rules, local references or profiles. Do not use for routine
  source-code edits or silently import third-party skills.
---

# Skill authoring — governance and a single quality standard

## Choose REUSE before CREATE

1. **Audit intent:** identify the target context and read available governance
   and catalog sources. In an AET checkout use `registry/skills.yaml`; in a
   global bundle use the gateway's Markdown indexes. The full AET charter is
   maintained externally: use a supplied copy or location, never invent its
   path. If unavailable, name the evidence gap rather than blocking authorized
   analysis or silently assuming compliance. See intake-and-decomposition for
   the boundary. Specify the behavior to improve, with positive, negative
   and ambiguous tasks.
2. **Compare existing skills and references:** apply REUSE → EXTEND → REFERENCE →
   CREATE only if responsibility and activation are truly independent; REJECT unsafe
   or duplicative suggestions. Do not equate a new technology noun with a new skill.
3. **Structure progressive expertise:** concise/discriminating name + description
   for discovery, operational SKILL.md for common decisions, scoped deep references
   for substantial know-how, examples/scripts/evals only when justified.
4. **Write execution-grade content:** explicit prerequisites, decision table,
   tested/illustrative methods, failure paths, limits, version/provenance where
   relevant and honest completion evidence. Empty checklists and link directories
   do not constitute specialist expertise.
5. **Keep host portability:** local registry/search doesn't guarantee native
   activation. No implicit installation, hook, network or privileged tool action.
6. **Validate universally:** apply one quality contract to every skill; run
   reference-link security, trigger collision, negative routing, context budgets,
   relevant executable tests and manual content review. **Do not use any maturity
   tier to select, trust or exempt a skill**.
7. **Submit a reviewable change:** document impact/rollback, update only relevant
   profiles and request explicit approval before merges/production actions.

## Required distinctions

- **Light/Standard/Deep** are workflow rigor modes, not skill quality levels.
- **Discovery/Activation/Reference** are knowledge access stages, not quality ranks.
- A semantic `version` on a SKILL.md identifies content revision only.
- Structural CI pass does not equal expert behavioral evaluation or production proof.
- `external-skill-audit` owns the provenance/license/security gate for external material.

## Selective references

- [Intake checklist, overlap and scope decisions](references/intake-and-decomposition.md) —
  **read when** evaluating a new skill, collision, category or requested import.
- [Uniform quality contract, test and lifecycle](references/quality-and-evaluation.md) —
  **read when** authoring references, constructing evaluations, evolving registry
  or reviewing skill release/maintenance.

## Done

Decision recorded (REUSE/EXTEND/REFERENCE/CREATE/REJECT/DEFER), boundaries
preserved, no uncontrolled imports, references accessible, regression tests
and known gaps reported; no invented "expert" certification.
