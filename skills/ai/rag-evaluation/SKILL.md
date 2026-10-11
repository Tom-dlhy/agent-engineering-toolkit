---
name: rag-evaluation
domain: ai
version: "0.2.0"
description: >-
  Use when measuring retrieval quality, ranking, grounding, citations,
  ACL leakage and answer faithfulness of an existing RAG pipeline.
  Do not use as the primary RAG indexing or ingestion implementation guide.
---

# RAG evaluation — retrieval and generation must be tested separately

## Method
1. Collect answerable and **unanswerable** questions with authorized,
   time-versioned supporting passages, tenant and document ACL labels.
2. Evaluate first-stage retrieval separately: recall@k, precision@k,
   MRR/nDCG where appropriate, filtering and query slice failures.
3. Assess grounding and citation **against actual quoted/source spans**,
   not just plausibility or a model judge's verbal confidence.
4. Evaluate end-to-end accuracy, abstention on missing/unauthorized
   evidence, stale document handling, freshness and citation precision.
5. Compare chunking, hybrid search, rerank and embedding models
   with the *same* held-out questions and frozen corpus/index revisions.
6. Stress cross-tenant retrieval, deleted docs, poisoning/injection,
   adversarial questions, duplicates, and overlong context.
7. Report quality, cost, latency and failure categories together;
   gate deployment on evidence and rerun after index/retriever changes.

## On-demand references
- [Retrieval gold sets and ranking metrics](references/retrieval-metrics-and-goldsets.md)
  — **read when** scoring retrieval, negatives or hybrid/rerank experiments.
- [Answer grounding, attribution and abstention](references/grounding-citations-and-abstention.md)
  — **read when** evaluating answer/citation quality and missing support.
- [Security, drift and end-to-end RAG regression](references/security-drift-and-regressions.md)
  — **read when** checking ACL leaks, index staleness and release blockers.

## Boundaries
rag-engineering owns building ingestion/chunk/index/query pipeline;
llm-evaluation owns model-wide graders and experiment statistics;
agent-tool-safety owns runtime authorization, not tests alone.

## Completion
Separate retrieval and answer scores, traceable gold evidence,
negative security cases, and named uncertainties (not just LLM judge scores).
