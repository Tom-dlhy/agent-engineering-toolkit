# Global AET — one native entry point, on-demand specialist library

## Goal

Install AET **once per user account** for Codex and Claude Code. No project
configuration, no mandatory profiles, no Python dependency in the target
project and no 178-skill frontmatter dump at session start.

The host discovers **one native skill**, named `aet`, at:
- Codex: `~/.agents/skills/aet/SKILL.md`
- Claude Code: `~/.claude/skills/aet/SKILL.md`

That skill contains only a short navigation contract. Under its directory,
`index/INDEX.md` lists AET domains and `index/<domain>.md` lists the
specialists from the current registry/frontmatter. The full 178 original
specialist bodies and their references are copied on disk to
`library/<domain>/<name>/GUIDE.md` and `references/`.

**Only the gateway is a native skill.** Internal `SKILL.md` files become
`GUIDE.md` (bytes unchanged) so Codex/Claude do not accidentally discover
178 nested native skills. The original source repository remains unchanged.
The host/agent makes relevance decisions by reading a relevant domain index,
not by running AET's lexical ranking code.

## Quick start

Run from the AET source checkout (Python 3.12+, PyYAML installed):

```bash
# Preview both global installations (read-only).
python scripts/aet_global.py plan

# Install one gateway + all on-demand specialist guides for both hosts.
python scripts/aet_global.py install --apply

# Verify installed files and their authenticated ownership state.
python scripts/aet_global.py doctor

# Later, from an updated AET checkout:
python scripts/aet_global.py update --apply

# Explicitly remove only the managed AET gateway from both hosts:
python scripts/aet_global.py uninstall --apply
```

Select only one host with `--agent codex` or `--agent claude`. Omitting
`--apply` previews any operation; `plan` is always read-only.
For `--agent both`, both destinations are checked for conflicts before any
copy begins; the two host updates are not a single cross-host transaction.
If the second update is interrupted, `doctor` will show the state of both.

Once installed, **start a fresh session in an unrelated project**.
Ask for an engineering task without mentioning AET, and check whether the
native `aet` gateway was actually invoked, then which guides were read.
An explicit smoke request such as "Use the aet skill and find FastAPI
guidance" verifies availability but **not automatic activation**.

### What to expect

- The `aet` native metadata is discoverable globally.
- The agent may invoke `aet`, read the lightweight domain index, then just
  `index/backend.md` and `library/backend/fastapi-service/GUIDE.md`.
- The agent may select **no specialist**, especially for a trivial typo.
- An AET guide bundled as `GUIDE.md` is not reported as separately
  host-native activated; record gateway invocation and actual guide reads
  separately.
- Codex and Claude native discovery and automatic selection are **not
  guaranteed by offline tests**. Neither a hook nor a new model/router is
  installed. Live traces are needed for acceptance.

## Safety, updates, and migration

The command reuses the signed, rollback-aware, hash-checked
`ManagedInstaller`, with user scope. It does not overwrite unmanaged
`aet` folders or edited managed copies. It does not execute bundled
skills/scripts, contact a network service, install external packages, modify
agent settings, or run models. Source symlinks and changed source bytes are
rejected. The native skill and its library are versioned as **one owned
directory per host**.

Existing user-scope managed profiles and this one-gateway scheme share the
installer's signed ledger. They are **not silently removed or migrated**.
If `aet_global.py` reports an old managed profile, inspect it and explicitly
uninstall those old copies using `scripts/manage_install.py uninstall
--agent <host> --scope user --apply` before trying again. Project-scoped
profiles and third-party plugins remain untouched. Do not install duplicate
AET gateway copies from a plugin and this CLI in the same scope.

If a file was modified locally, `doctor` can report the drift; update and
uninstall will refuse to overwrite/remove an unowned or modified directory.
The user's `~/.aet/` ownership metadata remains after uninstall.

## Operational boundaries

This path optimizes **global availability with small native discovery
metadata**, not full native exposure of every specialist. If you need to
invoke `fastapi-service` as a separate native skill by name, use the existing
managed profile installer or plugin distribution instead. No change is made
to existing profiles, registry entries or `suggest_workflow` behavior.

Bootstrap guidance must not invent permission to merge/deploy or blindly
follow bundled scripts. The existing `task-routing` guide is used only when
risk/scope/rigor selection is uncertain. No router can infer authorization
from filenames, descriptions or keywords.

For an honest real-agent acceptance test, run at least:
1. New Codex session outside the AET repo, specialist-relevant request,
   gateway invocation and guide read confirmed by host trace.
2. New Claude Code session in the same conditions.
3. Trivial/irrelevant request: no unnecessary specialist reads.
4. Update in the source checkout and verify a new session reads the updated
   guide; inspect host/tool versions and actual context costs.

These native runs are opt-in, potentially consume plan usage, and are not run
in CI.
