# Agent red-team tests, security regression and containment

**Read when:** qualifying an agent with tools, identifying injection
or privilege failures or establishing an incident response runbook.

## Attack surface inventory
User messages; retrieved snippets and indexes; emails and issue
descriptions; external MCP servers; tool results; code/file contents;
persistent memory; network destinations and execution environment.
For each entrypoint record privilege reachable and data/external
effect it could influence. Tests need authorization, not real attacks
on outside systems.

## Reproducible isolated attack suite
Use synthetic canary secrets and fake network/tool executors.
Attempt exfiltration via requested URL, tenant escape, tool-chain
escalation, malicious tool schema, forged approvals, schema
smuggling and uncontrolled cost loops. Assert on **actual tool
executor invocations and state**, not only model's friendly text.
Record whether denial happens before any side effect.

## Detection and incident response
Alert on suspicious denied actions, destination violations,
unexpected tool inventory changes, quota anomalies and untrusted
content trying to use privileged actions. Freeze affected run,
revoke compromised tokens, quarantine malicious indexed
document/memory, audit actual tool actions and recover safely.
Don't delete logs/snapshots until authorized forensic retention
requirements are met.

## Failure severity
An unauthorized write is blocking even if 999 read-only
questions succeed. Slice results by attack pattern, actor
scope, tool and data source. Compare releases against same
held-out adversarial set plus newly authorized incident cases.

## Limitations
No test set proves immunity against adaptive novel attacks;
manual approval alone doesn't guarantee an authorized
external request. Confirm actual IAM/proxy policy in live
approved staging with mock payloads before production rollout.

Sources: https://genai.owasp.org/llm-top-10/ ,
https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/ .
