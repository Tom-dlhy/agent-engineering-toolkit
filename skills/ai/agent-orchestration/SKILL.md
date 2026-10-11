---
name: agent-orchestration
domain: ai
version: "0.1.0"
description: >-
  Use when designing persistent multi-step LLM agent execution,
  LangGraph checkpointing, human-in-the-loop interrupts,
  recovery, handoffs, deadlines and state machines.
  Do not build a graph for a single stateless tool call.
---

# Agent orchestration — resumable execution, not unrestricted autonomy

## Design procedure
1. Choose deterministic workflow/state machine before autonomous agent
   when actions and transitions can be specified. Use model planning
   only where actual uncertainty benefits from it.
2. Model run/thread, tenant, actor, state/schema version, step, tool
   arguments/results, approvals, deadlines and terminal state.
3. Decide persistence: in-memory for disposable PoC; durable checkpoint
   store when resume-after-crash is required. LangGraph checkpoint
   semantics depend on thread IDs, nodes and configured durability.
4. Mark external side effects explicitly; checkpoint/replaying a node
   can rerun actions. Use durable operation ID, provider idempotency
   and reconciliation at remote commit uncertainty.
5. Human approval must be bound to exact action+actor+arguments and
   expire when the plan changes. Never infer approval from old context.
6. Bound iteration, cost, memory, parallel branches and queue work;
   handle streaming disconnect and model/tool failures as state changes.
7. Test crash at every side effect boundary, cancellation, stale
   approval, cross-tenant resumes, duplicate tool request and recovery.

## References on demand
- [State graph, checkpointers and resume](references/state-checkpoints-and-replay.md)
  — **read when** implementing LangGraph/DB-backed durable runs.
- [Human approvals, handoffs and memory](references/approvals-and-memory.md)
  — **read when** designing intervention, identity, memory and cross-agent delegation.
- [Reliability, cost bounds and recovery tests](references/failures-budgets-and-tests.md)
  — **read when** preventing loops, replaying interrupted steps or choosing agent vs workflow.

## Ownership
agent-tool-safety enforces tool authorization, python-llm-gateways
chooses libraries/gateways, llm-evaluation measures agent quality,
mcp-integration specifies protocol integration.

## Completion
Persisted state contract, authorization/approval invariant, bounded
execution, fault-injection evidence and recoverable failure cases.
