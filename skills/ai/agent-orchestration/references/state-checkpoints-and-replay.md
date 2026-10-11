# LangGraph checkpoints, state and external replay

**Read when:** implementing recoverable agents after crash,
resume, interrupts or cross-request workflow continuity.

## Two different persistence scopes
LangGraph checkpointers hold thread-scoped snapshots for short-term
conversation/workflow state; a Store holds app-defined
cross-thread data. InMemorySaver is suitable for disposable
development only and loses state across process restarts.
Production choose supported durable checkpoint backend,
retention, tenant ownership and schema migration policy.

### Schematic Python
~~~python
from langgraph.checkpoint.memory import InMemorySaver

# builder is the application-defined state graph, not part
# of this standalone fragment.
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "synthetic-run-1"}}
result = graph.invoke({"messages": []}, config)
~~~

Version-specific state shape, graph nodes and integration packages
must be verified against the pinned LangGraph version.

## External side effect caveat
A checkpointed node may execute twice following recovery:
if remote payment/email succeeded but checkpoint failed,
retry can repeat side effects. Persist stable operation ID
and use downstream idempotency or query-and-reconcile.
No graph checkpoint can atomically commit with an arbitrary
external HTTP service.

## Verify
Terminate after each node, before/after remote tool effect,
restore thread under same tenant, deny cross-tenant resume,
check schema migration, stale approval, canceled run and
checkpoint retention; use real disposable DB backend for
production-durability claims.

Sources: https://docs.langchain.com/oss/python/langgraph/persistence ,
https://docs.langchain.com/oss/python/langgraph/interrupts .
