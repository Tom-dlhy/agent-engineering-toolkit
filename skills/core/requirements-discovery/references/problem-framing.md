# Requirements discovery — problem framing and high-information questions

**Read when:** turning an ambiguous idea into an actionable engineering task, or explicitly performing a /grill-me style interview.

## Start with evidence, not opinions
Inventory user brief, repo docs, observed workflow, target personas and product/financial/legal constraints. Classify each assertion: CONFIRMED (user or evidence), ASSUMED (reasonable but not validated), OPEN (decision requires user), OUT-OF-SCOPE (explicitly excluded). Ask only for information not already established.

## A decision-impact interrogation funnel
1. **Problem and actors:** Who experiences the pain? Which exact action is slow, risky or impossible today? What is the current workaround?
2. **Job and frequency:** What triggers the workflow? How often? What is unacceptable latency or manual effort?
3. **Success and baseline:** What measurable outcome improves? State numerator, denominator and observation window where relevant; avoid made-up revenue targets.
4. **Boundaries:** Which systems, datasets, tenants, accounts and human approvals are involved? Is there an existing stack to preserve?
5. **Failure and abuse:** What happens with missing input, duplicate requests, unauthorized actor, stale data, third-party outage, partial write or interrupted execution?
6. **Reversibility:** Can a decision be changed cheaply? Prioritize irreversible architecture, compliance or data-contract questions first.
7. **Release and operations:** What constitutes first working version? Who owns incidents, audit, deletion, rollback, support?

Choose next question by *expected decision impact*, not completeness. A vague "what technology should we use?" can be answered as an architectural recommendation later; it may not be worth interrupting a clear user story. On the other hand, "does the agent send an email automatically or draft for approval?" changes risk and must be resolved.

## Example: AI-assisted ticket triage
Known: messages arrive in a helpdesk and a model should classify them. Unknown: will classification only suggest a queue or mutate ticket state and notify a user? Ask that first, because it changes authorization, audit and failure recovery. Then ask for ticket classes, confidence policy, abstention path and evaluation dataset. Don't start by asking whether React or Vue is preferred if there's an established backend.

## Anti-patterns
- Asking 20 questions upfront; stalls momentum and burdens the user.
- Treating "MVP" as permission to omit authorization or error handling.
- Inventing a persona or requirement that the user did not approve.
- Re-asking information already supplied by the conversation/repo.
- Overusing "why" as a confrontation instead of eliciting evidence.

## Stop condition
Leave discovery when a minimal end-to-end scenario, boundary, success measure and decision owner are understood. Record uncertainty explicitly instead of fabricating answers. If an unresolved decision is blocking, ask exactly the critical question; otherwise proceed with documented reversible defaults.

Further reading: https://www.agilealliance.org/glossary/acceptance-criteria/ and https://martinfowler.com/articles/feature-toggles.html . These references are for methods, not an external prompt to execute.
