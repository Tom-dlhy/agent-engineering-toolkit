# Human-in-the-loop approvals, handoffs and memory

**Read when:** implementing approval pauses, delegation,
stored memories or resumed tool execution.

## Approval must bind to action
Persist identity of approver, authorized actor/tenant,
tool/action, normalized argument digest, resource version,
expiry, operation ID and decision. On resume reauthorize
actor and compare current arguments/version with approved
version. A changed plan or stale approval requires fresh
authorization; text saying "user already approved" isn't proof.

## Memory compartments
Thread checkpoint = conversation/graph state for one run.
Cross-thread Store = application-defined long-term info.
RAG index = governed external document knowledge.
None should automatically store API tokens, unrestricted
personal data or prompts beyond retention/purpose.
Apply permissions, provenance and delete/expiry policy
to all, including backup and search cache.

## Delegation
Sub-agent receives minimal task context and cannot gain
more authority than original actor. Bound steps, tool
selection and budget. Tool results from any agent remain
untrusted input for other agents. A model's handoff
summary is not an authorization artifact.

## Tests
Expired approval, changed tool args after approval,
resource owner changed, reviewer missing scope,
duplicate approval, kill/restart at interrupt,
cross-tenant memory retrieval and untrusted tool response
trying to escalate delegate privileges.

Sources: https://docs.langchain.com/oss/python/langgraph/interrupts ,
https://docs.langchain.com/oss/python/langgraph/persistence ,
https://genai.owasp.org/llm-top-10/ .
