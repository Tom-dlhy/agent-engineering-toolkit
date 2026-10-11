# Agent workflow budgets and recovery test matrix

**Read when:** capping tool loops/fanout, dealing with
provider failures or evaluating autonomous orchestration.

## Bound resource consumption
Define max_steps, calls, total token/cost budget, tenant
concurrency, per-call deadline, absolute run deadline,
allowed tools, human escalation and terminal states.
Unbounded recursive tool loops, many parallel agents and
layered retries cause unpredictable costs and failures.
Do not assume a gateway budget can replace per-run caps.

## Recovery matrix
| Failure | Required invariant |
|---|---|
| Tool refused/unknown | No tool effect, durable failure reason |
| Provider 429 | Bounded wait within remaining deadline |
| Checkpointer outage | No fake successful completion |
| Crash after external mutation | Idempotent reconciliation |
| Approval expired | No privileged external action |
| Malicious retrieved instruction | No authority escalation |
| Partial streamed tool call | No incomplete argument execution |
| Cancel while running | Resource close and durable terminal state |

## Framework selection
For fixed business process with finite predictable transitions,
a typed state machine and durable queue can be simpler than
model-driven planner. Use LangGraph when persistence, branching,
human interrupts or tool loops justify framework cost.
Evaluate fixed-workflow baseline against task success,
latency, spend and operator review load.

Sources: https://docs.langchain.com/oss/python/langgraph/persistence ,
https://docs.langchain.com/oss/python/langgraph/interrupts ,
https://genai.owasp.org/llm-top-10/ .
