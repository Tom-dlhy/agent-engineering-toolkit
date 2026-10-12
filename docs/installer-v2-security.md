# Installer v2 — Security, adoption and release runbook

## Trust and recovery

Managed ownership ledgers and transaction journals are now authenticated using
a per-target HMAC key stored outside the project under
~/.config/agent-engineering-toolkit/trust/. On POSIX, key files use mode 0600
and their parent trust directory uses 0700. On Windows, profile ACLs apply.
The AET_TRUST_HOME override is reserved for isolated tests. Never commit keys.

A tampered ledger or journal fails closed. Recovery verifies the signed
transaction identity, exact destination and backup file hashes, and state
snapshots before removing or restoring any directory. An unexpected concurrent
edit leaves the journal and backup untouched for manual review. Installation
rechecks all destinations after staging and immediately before replacement.

This does not protect against a process that controls the user's trusted key,
nor guarantee atomicity across an uncooperative external editor. Projects
moved to a different canonical path require explicit recovery of trust.

## Migrate old unsigned Installer v2 ledgers

Earlier v2 installations used unsigned project-owned metadata. They now fail
closed, rather than silently claiming a user's files.

First back up the project; inspect each entry of the old ledger and verify
the listed folders really belong to AET. Matching SHA hashes does not by
itself establish ownership. Only after manual verification run:

~~~bash
python scripts/manage_install.py seal --agent codex --project /path/to/project --confirm-adoption I-VERIFIED-OWNERSHIP --apply
python scripts/manage_install.py doctor --agent codex --project /path/to/project
~~~

Use claude or user scope as needed. Installer v1 had no ownership ledger and
cannot be adopted automatically. If recovery refuses, preserve the pending
journal, tx backup folder and current files; never delete them to force repair.

## Reproducibility and releases

A dirty Git working tree is marked dirty-<sha> rather than presented as an
immutable source revision. Generating a frozen lockfile and creating a native
distribution from dirty source are refused. Installations track per-skill
revisions so adding one skill does not relabel all others.

Each native package gets a unique marketplace name derived from its plugin ID.
For example, plugin aet-web-app uses marketplace aet-web-app-local.

~~~bash
claude plugin validate /absolute/path/to/distribution
claude plugin marketplace add /absolute/path/to/distribution
claude plugin install aet-web-app@aet-web-app-local
codex plugin marketplace add /absolute/path/to/distribution
codex plugin marketplace list
~~~

Codex marketplace discovery does not mean the plugin is enabled. Enable/install
with the host-supported UI or configuration and independently verify runtime
loading. The optional release-skills workflow triggers only on an explicitly
pushed vX.Y.Z tag whose commit belongs to main, runs validation, builds every
profile, checks SHA-256 sums and publishes GitHub release archives. This
implementation does NOT create a tag or GitHub release automatically.

## Native acceptance (requires installed CLI)

~~~bash
python scripts/native_agent_smoke.py prepare --output /tmp/aet-native-probe
python scripts/native_agent_smoke.py validate --agent claude --output /tmp/aet-native-probe
python scripts/native_agent_smoke.py run --agent claude --output /tmp/aet-native-probe --allow-paid-agent-run
~~~

For Codex first install/enable the exact probe marketplace, then use
validate --agent codex and run --agent codex. The validation preflight checks
that the registered Codex marketplace list references the correct distribution.
The positive probe prompt does not contain its secret token; a successful
response should return that token. An unrelated negative request should not.
Inspect actual host logs for positive loading and negative non-activation, and
record agent versions, source paths and transcripts. Text checks alone do not
prove which copy of a plugin was invoked or that a skill was not activated.

Native vendor documentation:
- https://developers.openai.com/plugins/build/plugins
- https://code.claude.com/docs/en/plugin-marketplaces
