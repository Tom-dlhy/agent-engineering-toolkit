"""Explicit, paid native-agent acceptance probe (never invoked by default CI).

A probe package contains a private verification token in SKILL.md. The user
prompt does NOT contain the token: observing it in the agent reply provides
evidence that the packaged skill was actually loaded. This is a behavioral
smoke check, not proof of reliable auto-routing or production correctness.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toolkit.plugin_packager import build, verify
from toolkit.managed_installer import InstallError

TOKEN = "aet-native-confirmed-c85f9a7d2e64"
SKILL = "aet-activation-probe"
PROMPT = (
    "Explicitly use the installed skill called aet-activation-probe to execute "
    "the AET native plugin activation probe. Return only the exact verification "
    "token from that skill's SKILL.md; do not guess or infer a token."
)
NEGATIVE = "Answer the arithmetic question 2 plus 2, using only a single digit."


def prepare(output: Path) -> dict:
    result = build(ROOT / "tests/fixtures/native-probe", output, "probe", version="0.0.1")
    verify(output)
    return result


def run(agent: str, distribution: Path, timeout: int) -> dict:
    integrity = verify(distribution)
    manifest = json.loads((distribution / "aet-distribution.json").read_text(encoding="utf-8"))
    if manifest["selected"] != [SKILL]:
        raise InstallError("refusing to run a non-probe distribution")
    binary = shutil.which(agent)
    if not binary:
        raise InstallError("agent CLI is not on PATH: " + agent)
    version = subprocess.run([binary, "--version"], capture_output=True, text=True,
                             timeout=15).stdout.strip()[:300]
    plugin = distribution.resolve() / "plugins" / "agent-engineering-toolkit"
    with tempfile.TemporaryDirectory(prefix="aet-agent-probe-") as isolated:
        def invoke(message: str):
            if agent == "claude":
                command = [binary, "--plugin-dir", str(plugin), "-p", message,
                           "--output-format", "text"]
            elif agent == "codex":
                # Codex must have this distribution installed and enabled via
                # its local marketplace BEFORE running. Do not silently edit config.
                command = [binary, "exec", "--skip-git-repo-check",
                           "--sandbox", "read-only", message]
            else:
                raise InstallError("unsupported agent")
            start = time.monotonic()
            response = subprocess.run(
                command, cwd=isolated, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, timeout=timeout, check=False,
            )
            return {"exit_code": response.returncode,
                    "duration_seconds": round(time.monotonic() - start, 2),
                    "positive_token_seen": TOKEN in response.stdout,
                    "output_excerpt": response.stdout[-1200:],
                    "stderr_excerpt": response.stderr[-500:]}
        positive = invoke(PROMPT)
        negative = invoke(NEGATIVE)
    return {"agent": agent, "version": version, "distribution": str(distribution),
            "integrity": integrity, "positive": positive, "negative": negative,
            "passed": positive["exit_code"] == 0 and positive["positive_token_seen"]
                      and negative["exit_code"] == 0
                      and not negative["positive_token_seen"],
            "note": "Output checks alone cannot prove non-activation; review host skill logs."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("prepare", "run"))
    p.add_argument("--output", type=Path, required=True,
                   help="Fresh output for prepare; built probe distribution for run")
    p.add_argument("--agent", choices=("claude", "codex"))
    p.add_argument("--allow-paid-agent-run", action="store_true",
                   help="Explicitly authorize model invocations and associated usage")
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--report", type=Path, help="Optional local report; may contain model output")
    args = p.parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare(args.output)
        else:
            if not args.agent or not args.allow_paid_agent_run:
                raise InstallError("run requires --agent and --allow-paid-agent-run")
            if args.timeout < 10 or args.timeout > 600:
                raise InstallError("timeout must be between 10 and 600 seconds")
            result = run(args.agent, args.output, args.timeout)
            if args.report:
                if args.report.exists():
                    raise InstallError("report already exists; refusing overwrite")
                args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0 if args.command == "prepare" or result["passed"] else 2
    except (InstallError, OSError, subprocess.SubprocessError) as exc:
        p.error(str(exc))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
