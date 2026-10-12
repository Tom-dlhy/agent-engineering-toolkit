# Installer v2 — Managed skill distribution

Status: opt-in. Native host plugins and managed directory copies are **alternative**
delivery methods. There is no implicit code execution, network download or
modification of agent configuration.

## Managed installation

Requires Python 3.12+ and PyYAML. Run from a toolkit checkout.

~~~bash
# Preview selection (read-only)
python scripts/manage_install.py plan --agent codex --project /path/to/project --profile web-app
# Install selected skills
python scripts/manage_install.py install --agent codex --project /path/to/project --profile web-app --apply
# Add a single skill cumulatively, preserving prior installed selections
python scripts/manage_install.py install --agent codex --project /path/to/project --skill aws-bedrock --apply
# Check local edits or missing files
python scripts/manage_install.py doctor --agent codex --project /path/to/project
python scripts/manage_install.py list --agent codex --project /path/to/project
# Review and explicitly update
python scripts/manage_install.py update --agent codex --project /path/to/project
python scripts/manage_install.py update --agent codex --project /path/to/project --apply
# Restore missing files, only if the exact old source bytes are still present
python scripts/manage_install.py repair --agent codex --project /path/to/project --apply
# Remove only unchanged managed files; omit --skill for full uninstall
python scripts/manage_install.py uninstall --agent codex --project /path/to/project --skill aws-bedrock --apply
~~~

Switch --agent to claude for Claude Code. Switch --scope to user for installation
under the corresponding home-directory agent skills path. Default is project.

The authenticated per-agent ledger is stored in .aet/install-<scope>-<agent>.json and tracks
source revision, selected skills and SHA-256 per installed file. Preserve it
to enable safe updates and removals. Do not hand-edit ownership state.

**Safe defaults:** dry-run unless --apply; idempotent reinstallation, cumulative
additions, no overwrite of unknown files, detection of edited/extra/symlinked
files, refusal on conflicts, no implicit execution. Repair requires source
files matching the originally installed SHA-256 values.

**Recovery:** staging and backups are on the same filesystem; authenticated trust keys are outside the target project. A journal records
the transaction; normal failures roll back, and an interrupted transaction is
rolled back at the next explicit mutating invocation. A process lock prevents
concurrent toolkit operations on the same target. Read-only doctor reports
pending recovery. Do not manually delete .aet/pending-* or .aet/tx-*.
A transactional filesystem update cannot protect against drive failure or
arbitrary hostile concurrent writes.

The original scripts/install_profile.py remains as deprecated v1-compatible
copy-only tooling. New installations should use manage_install.py. Previously
copied unmanaged skills are never silently adopted: safe ownership migration
requires an explicit separate audit and opt-in.

## Native Claude Code and Codex distribution

~~~bash
python scripts/package_plugins.py build --profile python-backend --output dist/backend
python scripts/package_plugins.py build --profile python-backend --output dist/backend --version 1.0.0 --zip --apply
python scripts/package_plugins.py verify --output dist/backend
~~~

The generated marketplace root has this structure:

~~~text
dist/backend/
  .agents/plugins/marketplace.json
  .claude-plugin/marketplace.json
  plugins/agent-engineering-toolkit/
    plugin.json
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    skills/<selected-skill>/SKILL.md
    skills/<selected-skill>/references/...
  aet-distribution.json
~~~

The build is selective. All packaged files are included in a verifiable
SHA-256 distribution inventory. It rejects existing output paths, invalid
versions and source changes while copying. ZIP creation is deterministic.

~~~bash
claude plugin marketplace add /absolute/path/to/dist/backend
claude plugin install agent-engineering-toolkit@agent-engineering-toolkit-local
codex plugin marketplace add /absolute/path/to/dist/backend
# Install the plugin from the host's supported marketplace UI
~~~

For plugin packages, updates and removals belong to the host plugin manager,
not to our directory-copy installer. Do not install overlapping copies and
plugins in the same host scope. Different packages share one plugin identity:
install only one curated variant at a time. Native distribution does not
automatically publish to a public directory or inject a startup hook.

Choose an explicit SemVer and pin the source Git commit for a published release.
The default local version is 0.0.0-g<sha> or 0.0.0-dev for non-Git sources.

## P2 release evidence: actual host activation

Static unit tests validate file ownership, lifecycle safety, crash recovery,
manifests and packaged skill trees; they do not prove native loading or agent
behavior. Before certifying a release, on an authorized workstation:

1. Test the distribution on macOS, Linux and Windows with host versions recorded.
2. Add the built Codex marketplace, install the plugin, open a fresh session,
   request one exact packaged skill, and record the skill load trace.
3. Repeat in Claude Code via marketplace (or its --plugin-dir option), including
   a second session after a version upgrade.
4. Run a negative activation prompt, so unrelated skills remain unloaded.
5. Repeat with a modified local skill, interrupted installation and clean
   uninstall on throwaway projects. Preserve the outcome and transcript.
6. Measure agent output quality and actual tokens separately from metadata
   budget approximations. Publish only tested claims.

No agent API key or live CLI is available in the repository's static CI; live
agent behavior tests are an explicit, authorized release gate, not a passing
CI assertion.

Official host specifications:
- https://developers.openai.com/plugins/build/plugins
- https://code.claude.com/docs/en/plugins

## Reproducible project lockfiles

The lockfile records the exact selected skills, source Git SHA and source-file
SHA-256 hashes. It is portable between machines with the same source checkout.
New installs can use a frozen lock; source drift or a different installed
selection causes an error rather than a silent update.

~~~bash
python scripts/manage_install.py lock --agent codex --project /path/to/app --profile web-app
python scripts/manage_install.py lock --agent codex --project /path/to/app --profile web-app --apply
python scripts/manage_install.py install --agent codex --project /path/to/app --locked --apply
~~~

The default path is .aet/skills-lock-<agent>.json. Existing lockfiles are
never replaced silently: review and explicitly remove or version-control a
superseded lock before regenerating it. A frozen install does not fetch the
source Git SHA automatically; checkout the required revision beforehand.

## Optional real-agent acceptance harness

A separate probe fixture contains a verification token found ONLY inside the
probe SKILL.md (not in the model prompt). Run only with explicit authorization
and a configured native CLI; this can consume model usage.

~~~bash
python scripts/native_agent_smoke.py prepare --output /tmp/aet-probe
# For Claude, the probe is passed with --plugin-dir by the harness:
python scripts/native_agent_smoke.py run --agent claude --output /tmp/aet-probe --allow-paid-agent-run
# For Codex, first add/install/enable the generated local marketplace, then:
python scripts/native_agent_smoke.py run --agent codex --output /tmp/aet-probe --allow-paid-agent-run
~~~

The test checks the secret token in the positive response and its absence
in an unrelated negative response. The host transcript must still be reviewed
to prove the negative case did not load the skill. Neither CLI nor paid model
credentials are used in standard CI.

For several independently installed native profile packages, use unique
plugin IDs with --name aet-<profile> when building each distribution.

## Installer v2 safety changes

See [security, legacy ledger sealing, release and native host verification](installer-v2-security.md). Earlier unsigned Installer v2 ledgers require explicit verified sealing before new updates or uninstall. Deleted/modified files and forged journals fail closed. The marketplace name is based on the plugin identity, not a shared aet-local identifier. Frozen lockfiles and release packaging require a clean Git source. Versioned profile archives may be published only through an explicitly created vX.Y.Z release tag on main.
