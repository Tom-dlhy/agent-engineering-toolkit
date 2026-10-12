# Evidence-driven engineering — A/B/C evaluation framework

> Status: **implemented as an opt-in local runner and deterministic analyzer**.
> Benchmark outcomes on Codex/Claude have **NOT** been collected or validated
> by this pull request. The fixture, tests and comparisons only prove that the
> experimental infrastructure follows its documented contracts.

AET should be evaluated as an engineering tool, not by counting Markdown
skills or trusting the model's claim to have followed an instruction.

## Why three arms?

| Arm | What's exposed | Question |
| --- | --- | --- |
| **A / baseline** | Clean trusted fixture, no project AET skills | What can the host model already do? |
| **B / knowledge** | Same fixture + selected technical `SKILL.md` and references | Does focused engineering knowledge help? |
| **C / full** | Technical skills + task-routing, verification-before-done, implementation-planning, test-strategy + AET operating contract | Does our *methodology* add value beyond knowledge? |

These are **project-level skills**. Existing user-global skills, config, MCP,
memory and providers may influence runs; native host configuration must be
isolated *externally* for a genuinely controlled experiment. The runner does
not claim that simply copying a skill proves that the host read or activated
it. Its records deliberately leave `observed_skill_activation` null.

All arms receive the same task prompt and fixture bytes, pinned host and
model; order is shuffled by a recorded seed to reduce but not eliminate
time/order effects. Each arm/trial gets a fresh temporary workspace.

## Small, reproducible start

Requirements: a local toolkit checkout, Python 3.12+ and PyYAML. The
`plan` and `analyze` commands need **no model account**.

```bash
python scripts/benchmark_aet.py plan \
  --manifest evals/benchmark/example.json --host codex \
  --model YOUR_PINNED_MODEL --trials 2
```

The example is **intentionally not runnable as a paid experiment yet**:
`fixture_sha256` is null. Inspect its source, `check_argv`, scope
and expected behavior. Copy the suite to a new versioned JSON manifest and
pin the `fixture_sha256` value from plan output. The runner then
rejects fixture changes or a different digest.

The demonstration task contains an intentionally failing string
normalization assertion. It is a *debugging exercise*, not a validation
of production integrations or security.

## Native runs — expensive, privileged and explicitly opted in

**Use a separate disposable VM/container with only test credentials**,
no production cloud roles, unrelated repositories, personal SSH keys,
browser sessions or valuable data. Configure the host CLI and pin the
model/version in that disposable environment. A temporary directory by
itself does **not** stop host plugins, credentials, filesystem access or
network calls. Inspect all fixture code before running tests. CLI hosts
and authorization semantics can change; validate commands against your
installed versions.

```bash
# After you have reviewed and pinned your own benchmark suite:
python scripts/benchmark_aet.py run \
  --manifest evals/benchmark/your-pinned-suite.json \
  --host codex --model YOUR_PINNED_MODEL --trials 2 \
  --output .tmp/aet-benchmark-01 \
  --max-runs 6 --timeout 120 --max-total-seconds 900 \
  --allow-paid-agent-run \
  --allow-test-execution \
  --trusted-disposable-host
```

Replace `codex` with `claude` to use Claude Code. Only one host
is compared per report; compare hosts separately rather than pooling their
results. `--max-runs` limits the number of model invocations but is NOT
a provider billing limit; the runtime's CLI may impose its own metering,
rate limits or additional model/tool calls. AET does not run model
calls from CI.

Host invocation policies:
- Codex: `exec --sandbox workspace-write --json` with pinned model;
  no sandbox-bypass flag. Actual host/plugin access still needs independent
  containment.
- Claude Code: `-p --output-format json --permission-mode dontAsk`
  with a narrow Read/Edit/Write/Glob/Grep allowlist and a turn limit.
  No `--dangerously-skip-permissions` and no Bash allowed in the
  agent's toolset. The **harness** separately executes the trusted test
  command after the agent stops, under its own explicit authorization.

Each completed trial is checkpointed to `records.json` alongside a
bounded private evidence bundle containing before/after task source and
unified diffs, in addition to result metadata and recognized host token
counters. Raw conversation logs are not persisted by default. A timeout or interruption may leave a
**partial** report which must never be padded with invented successes.
Never commit benchmark records or private model output to the repository.


## Preserved results and independent verification (artifact patch)

Each native run now snapshots **the actual agent-produced task tree
before the test command runs**. The runner writes a private local evidence
bundle under `<output>/artifacts/<run_id>/`:

- `before/` — original task files, before the agent;
- `after/` — task files as left by the agent, before acceptance checks;
- `changes.patch` — unified UTF-8 diff (binary modifications use the
  two original snapshots for manual comparison);
- `manifest.json` — SHA-256 hashes, changed paths, file counts and run ID.

The runner checkpoints `records.json` atomically with a pointer to the
bundle's manifest digest. It does not overwrite pre-existing report
directories. Failed agent calls retain their safe evidence; on symlink,
sensitive path/content, oversized artifact or capture failure, the
trial is marked **BLOCKED** and its acceptance command is not executed.
Files and directories are created with restrictive permissions
(`0600`/`0700` where supported). Raw model output is not archived.

**Important:** these are bounded privacy precautions, **not** a
general-purpose secret detector, tamper-proof storage or OS sandbox.
The host CLI and testing code can still reach resources outside the
temporary directory. Run only with vetted tasks, synthetic input,
a disposable host and no sensitive credentials. Never upload the
result directory to GitHub.

After a real run, verify every archived file against its manifest
**without running a model**:

```bash
python scripts/benchmark_aet.py verify \
  --records .tmp/aet-benchmark-01/records.json \
  --verified-output .tmp/aet-benchmark-01/verified-records.json
```

The verification creates a **new** copy; it never overwrites original
records. `artifact_evidence_verified=true` means only that the local
bundle matches its recorded checksums. It does **not** prove a native
skill activated, that the model respected the workflow, or that the
output is correct. Inspection of files, diff, dependency effects and
acceptance coverage remains an independent reviewer responsibility.

A human reviewer should open the `after/` files and `changes.patch`
for **every** A/B/C trial, including failures, then edit a *separate
private reviewed copy* to set `human_review` and
`critical_violation` with documented justification. Run `analyze`
on that reviewed copy, not on the raw output. The analyzer now blocks
any promotion recommendation unless all arms have recorded captured
and integrity-verified evidence.

There is intentionally no automatic retention cleanup: evidence is
needed for independent audit. Delete local results manually only
after completing review and when your data-retention policy permits it.

## Independent grading and comparison

The runner knows whether the agent process exited normally and whether
the trusted acceptance command passed. It does not know that the patch
meets all product requirements, contains no security flaw, or that a
specific skill was read. Every generated row starts as:

```json
{"human_review": "NOT_REVIEWED", "critical_violation": null}
```

Reviewers inspect the **actual artifact** and independent oracle
before marking `human_review` as PASS/FAIL and
`critical_violation` as true/false. This manual judgment must be
traceable to a reviewed diff, exact revision, test outcomes and rubric,
not based on the agent's self-report. Reviewers should be blinded to
A/B/C labels where possible. Keep immutable original run output and a
separate reviewed copy, with reviewer identity/decision notes stored in
your private test-workspace audit trail.

```bash
python scripts/benchmark_aet.py analyze \
  --records /path/to/reviewed-records.json \
  --min-trials 2 --min-success-delta 0 \
  --max-token-increase-pct 20
```

The analyzer rejects incomplete A/B/C trials, duplicated runs,
mismatched fixture digest, host, model, tool configuration or suite
revision. It reports per-arm success/failure, sample size, new critical
regressions, and token deltas *only when all observed counts exist*.

Possible gate outcomes:
- `NO_GO_CRITICAL_FINDING`: any observed critical violation in the
  dataset; no cost optimization can justify a known critical defect.
- `INSUFFICIENT_EVIDENCE`: missing/incomplete tests, approvals,
  risk classifications or minimum trial repetitions.
- `NO_GO_QUALITY_THRESHOLD`: full AET fails the declared quality bar.
- `NO_GO_COST_THRESHOLD_OR_UNMEASURED`: cost limit exceeded or
  tokens unavailable when a token limit is part of the requirement.
- `CANDIDATE_FOR_HUMAN_APPROVAL`: numerical gates are satisfied,
  but independent evidence review and **explicit repository-owner
  authorization** are still required. Never automatic promotion.

Set `min_success_delta` meaningfully based on the task and experiment
budget. A default zero only checks that observed pass rate did not
decrease; it is not proof of a positive effect, statistical
significance, time savings or downstream productivity improvement.

## Evaluation policy proportional to the change

| Change in AET | Required evidence |
| --- | --- |
| Typo/docs-only | Structural validation and correct diff (no paid run) |
| Routing trigger, exclusion or profile membership | Positive, negative, ambiguous and French/English lexical tests |
| New or substantially revised method | Representative A/B/C subset with output oracle and measured cost where available |
| Trust boundary, plugin or privileged workflow | Deep negative, failure/replay and authorization checks; independent risk review before integration |

Evaluate **quality per successful task**, not raw tokens alone. A lower
cost with data leakage is not a win. Report first-order success rate,
regression rate, missed/false skill activation (only if native traces
show activation), human corrections, time to verified completion and
tokens with clear denominators, repetitions and limitations.

Do not silently tune skills on held-out tasks. Keep separate
development and held-out task pools and preserve baseline revisions.

## What this implementation does *not* claim

1. No real Codex/Claude paid runs were executed in this PR.
2. Native skill *availability* is staged; skill *activation* is not
   independently captured and cannot be inferred from installation.
3. The runner is a **bounded local test harness, not a hardened sandbox**
   or guarantee of isolation, billing caps or plugin disablement.
4. Artifacts are now retained with local SHA-256 integrity checks,
   but these are not signed provenance or independent correctness proof.
   Human reviewers must verify artifacts and results before claims.
5. Three-arm aggregate differences alone do not establish causality,
   significance or generalization to arbitrary applications.
6. AET does not self-edit, self-promote, merge or deploy based on
   benchmark records.

See [adaptive methodology](adaptive-engineering-methodology.md),
[existing paired two-arm summarizer](../scripts/summarize_skill_evals.py)
and [roadmap](roadmap.md). The older two-arm utility remains available
for historical before/after datasets; this A/B/C implementation is
a separate and deliberately more conservative protocol.
