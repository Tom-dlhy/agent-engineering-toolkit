# RAG grounded answer, attribution and abstention QA

**Read when:** deciding whether generated answers cite real
evidence, correctly decline unsupported questions or invent citations.

## Separate three questions
1. Did retrieval deliver sufficient authorized passages?
2. Did answer statements faithfully follow those passages?
3. Are displayed citations actually tied to source offsets/IDs?

A correct general-world answer **without support in allowed
corpus** may be unacceptable for enterprise grounded RAG.
An answer can cite a real document yet make a claim that
the document does not justify. Citation existence != fidelity.

## Citation acceptance
For each material answer claim map source document ID, version,
page/section/span and supporting quote where policy permits.
Resolve every citation to an authorized currently accessible
source. Explicitly reject fabricated source IDs, irrelevant
chunks, stale versions and inaccessible tenant documents.

## Abstention
Collect unanswerable cases, missing document, empty retrieval,
conflicting sources, revoked access and uncertain updates.
Desired output may be a qualified refusal or clarification
rather than inference outside approved sources. Track false
refusals too, because over-abstention can make tool unusable.

## Grading
Use deterministic source ID/ACL checks for hard failures;
human judges for semantic support; calibrated model-as-judge
only as a noisy proxy. Report examples, denominators,
annotation disagreements and critical hallucination types.

Sources: https://docs.llamaindex.ai/en/stable/module_guides/evaluating/ ,
https://platform.openai.com/docs/guides/evals .
