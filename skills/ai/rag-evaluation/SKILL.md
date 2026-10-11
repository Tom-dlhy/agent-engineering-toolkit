---
name: rag-evaluation
domain: ai
version: "0.1.0"
description: >-
  Use when designing, debugging or evaluating retrieval-augmented generation, embeddings, chunking and grounded answer quality. Do not rely on subjective one-off answers as a sufficient evaluation.
---

# rag-evaluation

## Retrieval
Collect representative questions, authoritative documents, expected answer/support evidence and negative examples. Evaluate chunking, hybrid search, metadata filters, reranking and access controls.
## Metrics
Measure retrieval recall/precision at k, groundedness, answer correctness, citation accuracy, latency and cost. Use human-labelled gold sets for critical workflows, and treat LLM judges as noisy instruments.
## Safety
Preserve document ACLs, avoid leaking cross-tenant data, and isolate retrieved text from instructions to mitigate prompt injection. Handle empty and stale retrieval explicitly.
## Runbook
Version indexes and retrieval parameters; compare against a baseline, analyze failure slices and define regression thresholds before shipping.
