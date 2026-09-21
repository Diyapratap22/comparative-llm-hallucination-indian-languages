# Annotation Guidelines — Preliminary Framework

> **Status: PRELIMINARY — under development.**
> This is a **draft** framework for the human annotation step of the study.
> Nothing here is final. The label scheme, definitions, and workflow will be
> finalized and piloted **before** annotation begins on real model responses.

## 1. Purpose

Annotation produces the ground-truth labels that the quantitative analysis
relies on. Each annotator evaluates a **model response** against a **reliable
reference answer/source** for the corresponding question and assigns one
preliminary label (Section 4).

## 2. Materials per annotation unit

Each annotation unit is a single model response for a single prompt:

| Field | Content |
|---|---|
| `question_id` | identifier of the underlying paired question |
| `language` | `en` or `hi` |
| `model` | model identifier (to be finalized) |
| `response` | the model's raw answer text |
| `reference` | the reliable reference answer/source for this question |

## 3. Reference answers

- Every question must have a reference answer and/or a reliable source
  **before** annotation begins.
- Reference materials must be verifiable (e.g. authoritative sources or
  well-established factual content).
- Annotators evaluate the response **against the reference**, not against
  personal knowledge alone.

## 4. Preliminary label scheme

**These labels are preliminary and will be finalized before annotation
begins.** They are recorded here so the review process has a concrete starting
point.

| Label | Working definition |
|---|---|
| **Correct** | The response answers the question and is consistent with the reference answer/source. |
| **Partially Correct** | The response is partially consistent with the reference — some relevant part is correct, but it contains omissions, unsupported additions, or inaccuracies. |
| **Hallucinated** | The response contains claims not supported by (or contradicting) the reference answer/source, presented with unjustified confidence. |
| **Refusal / No Answer** | The model declines to answer or provides no substantive answer. |
| **Unclear / Requires Adjudication** | The appropriate label is ambiguous, the response is off-topic, or the reference is insufficient — requires joint review/adjudication. |

Open questions about the scheme (to be resolved before annotation):

- Whether one label per response is sufficient, or whether multi-label or
  span-level annotation is needed for fine-grained error analysis.
- Exact boundary rules for "Partially Correct" vs. "Hallucinated".
- Whether "Refusal / No Answer" responses are excluded from hallucination
  rate denominators or analysed separately.
- Whether any additional labels are needed.

## 5. Guiding principles

1. **Evidence-based.** Every decision must be traceable to the reference
   answer/source; annotators should be able to say *why* a label was chosen.
2. **Independently reproducible.** Procedures should be defined such that a
   different annotator reaches the same label from the same materials.
3. **Independence.** Each annotator works independently before any
   adjudication step.

## 6. Workflow (planned)

1. Pilot round on a small sample (e.g. ~20 responses) to test the scheme.
2. Full annotation by annotator 1 and annotator 2 (independent).
3. Measure inter-annotator agreement (metric TBD).
4. Adjudicate disagreements (jointly or with a third reviewer) →
   `annotations/final_labels/`.

## 7. Storage

- `annotations/annotator_1/` — annotator 1's raw annotation files (empty).
- `annotations/annotator_2/` — annotator 2's raw annotation files (empty).
- `annotations/final_labels/` — adjudicated, agreed labels (empty).

## 8. Items to be finalized before annotation

- This guideline document (label definitions, boundary rules, workflow).
- The annotation form / CSV schema.
- The adjudication protocol.
- The inter-annotator agreement metric.