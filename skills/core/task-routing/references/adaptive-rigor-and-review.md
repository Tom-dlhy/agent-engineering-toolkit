# Adaptive rigor, review and execution decision procedure

**Read when:** assessing review R0/R1/R2, a possible subagent dispatch, parallelism or escalation from newly observed risks.

## Separate the three knobs

Workflow = amount of preparation and verification: LIGHT, STANDARD or DEEP.
Review = who assesses the diff and what independent evidence is needed:
R0 (self), R1 (targeted), R2 (risk-led independent).
Execution = inline, subagent-driven or parallel *independent* domains.
They must be chosen separately. DEEP does not logically entail three
agents, and R1 does not imply a full-repository audit.

~~~text
Signal                                      Workflow     Review     Execution
Local label with visual oracle               LIGHT        R0         inline
Small backend validation, fully tested       STANDARD     R0         inline
New public API across components             STANDARD     R1         inline or delegated
Authorization bypass, even one line          DEEP         R2         inline + reviewer
Distributed data migration, rollback risk    DEEP         R2         task graph
Three disjoint failure investigations        STANDARD     R0/R1      parallel if supported
~~~

These are defaults, not a classifier based only on the user prompt.
A review request can explicitly demand more assurance; tool availability
can limit execution strategy but never silently satisfy an unmet safety gate.

## Cost-aware dispatch threshold

Before adding an agent, estimate benefit: will fresh context catch a
likely class of defect, avoid a known context-window limit, run genuinely
independent investigations concurrently or reduce total wall time?
Estimate cost: duplicated code reading, agent/model invocation, tool setup,
review loops and merging. If the same actor with a deterministic test
can achieve the accepted oracle cheaply, remain inline.

A targeted reviewer should receive a narrow packet: accepted requirements,
base and head SHA, affected paths/interfaces, actual tests/outputs,
expected invariants, risk focus, known exclusions. Do not forward the
entire session or a giant unrelated code dump. Ask one coherent
re-review of *changed findings* rather than recirculating the entire diff.

## Dynamic escalation and downgrade

Start with the lowest compatible default. If a failing test reveals a
shared invariant, switch to STANDARD; if the failure exposes
authorization/data loss, switch to DEEP and independent review.
If the seemingly sensitive subject is only a harmless copy change,
document why the change does not touch the trust boundary and keep
LIGHT. If an independent reviewer is unavailable for R2, the task may
still be locally implemented and tested with evidence, but the independent
gate remains unmet and merge/deploy readiness must be reported BLOCKED.
No invented "reviewer" result.

## Stop conditions

Pause the affected action for a destructive file operation not yet
authorized, production write, credential publication, merge or policy
change outside scope. Tool absence never grants authority. A user-approved
source-code fix is not automatically authorization for deployment.
Use exact current revision when evaluating readiness; green checks on
an older commit are insufficient.

## Measurement

Measure on comparable held-out tasks with/without the method: context
loaded (or approximate chars where tokens absent), agent starts,
review count, passed acceptance cases, defects found and escaped,
human corrections, latency and explicit skipped gates. Low token usage
alone is not success when authorization or correctness regresses.
