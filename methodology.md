# Methodology and Evaluation Framework

**A Comparative Evaluation of Hallucination in Large Language Models for English and Indian Languages**

| | |
|---|---|
| **Document type** | Research methodology and evaluation framework (formal specification) |
| **Deliverable** | Methodology + Evaluation Framework |
| **Status** | **Finalized methodology — the experiment has NOT been run.** |
| **Data status** | The finalized question bank exists (`data/raw/question_bank.xlsx`); no model responses, annotations, or numerical results exist. |

> **Important.** This document is a *specification*. It defines what the study will do, how
> hallucination is defined *for this study*, how responses will be annotated, and how results
> will be computed and interpreted. It contains **no experimental results**. Every worked
> example appearing below (Section 5.6) is an *illustrative* annotation case constructed to
> demonstrate decision rules — it is not an observed experimental finding. No statistical test has
> been run, and no statistical significance is claimed or reported anywhere in this document.

---

## Contents

1. Introduction and Scope
2. Study Design
3. Research Questions
4. Operational Definition of Hallucination
5. Annotation Scheme
5.1 Annotation Fields · 5.2 Correctness · 5.3 Hallucination · 5.4 Hallucination Types ·
5.5 Severity · 5.6 Boundary Examples · 5.7 Correctness Versus Hallucination Decision Matrix
6. Evidence / Reference Protocol
7. Two-Independent-Annotator Protocol
8. Disagreement Resolution
9. Inter-Annotator Agreement
10. Evaluation Metrics
11. Statistical Analysis Plan
12. Qualitative Error Analysis
13. Reproducibility
14. Literature Grounding
15. Limitations of the Methodology
Appendix A. Reference Conventions

---

## 1. Introduction and Scope

This document specifies the methodology for the project *“A Comparative Evaluation of
Hallucination in Large Language Models for English and Indian Languages.”* The study is a
**controlled, paired, human-annotated comparative study of hallucination behavior in large
language models (LLMs)** when the same underlying question is posed in **English (en)** and in
**Hindi (hi)** by the same model under identical experimental settings.

The scope of this document covers (i) study design, (ii) research questions, (iii) the
operational definition of hallucination, (iv) the annotation scheme and protocol,
(v) evidence/reference procedures, (vi) disagreement resolution, (vii) inter-annotator
agreement, (viii) evaluation metrics, (ix) statistical analysis, (x) qualitative error
analysis, (xi) reproducibility, (xii) literature grounding, and (xiii) limitations.

The following project artifacts are owned by other workstreams and are **not** modified by
this document or by its author: the question bank (`data/raw/question_bank.xlsx`), the
experiment pipeline (`experiments/`), prompt templates (`experiments/prompts.py`), model
selection (`experiments/config.py:MODEL_IDS`), the README, analysis scripts (`analysis/`),
the annotation guideline draft (`annotations/annotation_guidelines.md`), and the literature
tracking files (`literature/*`, `paper/references.bib`). Where the annotation scheme defined
here extends or supersedes the preliminary labels in `annotations/annotation_guidelines.md`,
the definitions in this document govern.

**Conventions used throughout this document:** “designated reference evidence (DRE) refers
to the `Expected Answer` and `Source` recorded for the question plus any reliable supporting
evidence specified for that question; `[REF NEEDED]` denotes a citation that is required but
cannot be provided at the time of writing because the repository contains no verified
literature entry or BibTeX record yet (Section 14 and Appendix A).

## 2. Study Design

### 2.1 Controlled comparative design

The study is a controlled comparative evaluation of LLM hallucination across two languages.
The comparison is structured as follows:

```
            same underlying question
                     ↓
    English version          Hindi version
                     ↓
                 same model
                     ↓
        same experimental settings (identical for en and hi)
                     ↓
          compare hallucination outcomes
```

Question content is held fixed across languages by construction (English–Hindi pairing of
the same underlying question), so language is the primary experimental factor. Any
language-related difference in outcome is attributed to language-dependent generation
behavior rather than to differences in question content or difficulty.

### 2.2 Finalized dataset specification

The finalized question bank (`data/raw/question_bank.xlsx`, sheet `Question Bank`) contains
**200 underlying questions**, one row per underlying question in a wide format in which the
English and Hindi versions share the row:

| Column | Content |
|---|---|
| `Question ID` | Unique identifier `Q001`–`Q200`. |
| `Category` | Task category (title case, see Table 1). |
| `English Question` | The question in English. |
| `Hindi Question` | The matched question in Hindi — the same underlying question. |
| `Expected Answer` | The reference answer for the question. |
| `Source` | Designated provenance/source record for the question and its reference answer. |

**Table 1. Category distribution of the finalized question bank**

| Category | Number of underlying questions |
|---|---|
| Factual | 50 |
| Numerical | 50 |
| Reasoning | 50 |
| Cultural/India-specific | 50 |
| **Total** | **200** |

Each underlying question contributes exactly two language-specific prompts (one `en`, one
`hi`), so the prompt set comprises **400 language-specific prompts (200 English +
200 Hindi)**. With **3–4 LLMs**, each model will therefore receive **400 prompts**, yielding
up to **400 responses per model**. The exact model list and versions are finalized by the
experiment workstream (`experiments/config.py:MODEL_IDS`); this methodology is
model-agnostic, and every metric defined in Section 10 is computed per model.

### 2.3 Structural notes on the question bank (documented, not modified)

1. **Category-name normalization.** The question bank stores category names in title case
   (`Factual`, `Numerical`, `Reasoning`, `Cultural/India-specific`), whereas the repository
   code (`experiments/config.py:TASK_CATEGORIES`) uses lowercase internal identifiers
   (`factual`, `numerical`, `reasoning`, `cultural_contextual`). A **name-mapping step is
   required at data ingestion** so that category joins are correct. The mapping is:
   `Factual → factual`, `Numerical → numerical`, `Reasoning → reasoning`,
   `Cultural/India-specific → cultural_contextual`. This is a documented normalization
   requirement; neither the code nor the question bank is modified by this document. In this
   methodology, the question-bank names refer to the dataset categories, and the lowercase
   identifiers refer to the internal code names.
2. **ID ordering.** `Q001–Q049` and `Q200` are `Factual`; `Q050–Q099` `Numerical`;
   `Q100–Q149` `Reasoning`; `Q150–Q199` `Cultural/India-specific`. `Q200` appearing after
   the Cultural block is purely an **ordering quirk**; categories are assigned per row and
   are not derived from ID position, so this has no methodological consequence.
3. **Short `Expected Answer` values.** A substantial number of `Expected Answer` values are
   very short (single characters, single numbers, short letter sequences, etc.).
   Consequently, the `Expected Answer` field is **not guaranteed to be sufficient on its
   own** for judging whether a response claim is supported. Section 6 therefore requires
   annotators to consult the designated `Source` (and reliably documented supporting
   evidence) for substantive verification.

### 2.4 Experimental settings and response capture

- **Prompts** are constructed from the standardized, neutral templates in
  `experiments/prompts.py`. The system instruction is identical across languages and models
  and contains no content that encourages or discourages hallucination. Only the question
  text and the “Question:/Answer:” marker differ by language.
- **Generation settings** (temperature, max tokens, top-p, seed, provider-specific
  parameters) are fixed per model across the whole run and recorded in the run manifest, so
  that `en` and `hi` prompts for the same model are generated under identical settings.
- **Raw responses** are stored unmodified under `responses/raw_responses/` together with the
  run manifest and full metadata (Section 13).
- **Evaluation** is performed by **two independent human annotators** (A1, A2) who label
  every response against the designated reference evidence (Sections 5–8).

### 2.5 Unit of analysis

One annotated unit is one model response to one language-specific prompt
(one `(question_id, language, model)` triple). The paired comparison unit is the `(en, hi)`
response pair produced by the same model for the same underlying `question_id`; language is
therefore a **within-question (paired) factor**, as required by the statistical plan in
Section 11.

## 3. Research Questions

The study addresses the project's five research questions:

- **RQ1.** How does hallucination frequency differ between English and Hindi when LLMs are
  evaluated using semantically equivalent and parallel questions?
- **RQ2.** How does hallucination frequency vary across different LLMs and task categories?
- **RQ3.** What types of hallucinations are most prevalent in English and Hindi responses?
- **RQ4.** Does the difference in hallucination rate between English and Hindi vary across
  task categories?
- **RQ5.** Is the observed difference between English and Hindi hallucination rates
  statistically significant?

**Table 2. RQ-to-methods mapping**

| RQ | Addressed in |
|---|---|
| RQ1 | Study design (Section 2), language hallucination rates (Section 10.3) |
| RQ2 | Model-wise and category-wise rates (Section 10), per-stratum paired analysis (Section 11) |
| RQ3 | Hallucination types (Section 5.4), qualitative error analysis (Section 12) |
| RQ4 | Category-wise metrics and category-stratified paired tests (Sections 10–11) |
| RQ5 | Paired statistical hypothesis testing (Section 11) |

## 4. Operational Definition of Hallucination

### 4.1 Definition

For the purposes of this study, **hallucination is defined operationally as follows:**

> A response is **hallucinated** when it presents a **materially false, fabricated,
> contradictory, or unsupported factual claim as true**, where the claim **cannot be
> justified** using the designated reference answer/source (the `Expected Answer` and
> `Source` for the question) **or reliable evidence** established for that question
> (Section 6).

The definition has three jointly required elements:

1. **A claim exists.** The response asserts a factual claim (about entities, events,
   numbers, people, places, causal/logical relations, processes, or cultural/contextual
   facts) rather than merely restating the question.
2. **The claim is presented as true.** The claim is asserted without qualification or with
   an assertion that implies factuality. A hedged, explicitly speculative, or transparently
   hypothetical statement (“I am not sure”, “possibly”, “one theory holds”) is **not**
   presented as true and is not, by itself, a hallucination.
3. **The claim is materially false, fabricated, contradictory, or unsupported relative to
   the designated evidence.** It either (i) states as fact something that the evidence
   contradicts (contradiction), (ii) introduces content with no basis in the evidence
   (fabrication), (iii) asserts internally inconsistent claims, or (iv) cannot be justified
   by the designated reference answer/source or reliable evidence (unsupported), and the
   falsity/unsupportedness is **material** — i.e., it affects the substance of the answer the
   model was asked to provide.

This definition is deliberately **reference-grounded and evidence-based**: a claim is
judged against the `Expected Answer`, the `Source`, and any reliable evidence designated for
the question — not against the annotator's general recollection alone, although reliably
verifiable general knowledge may corroborate a claim (boundary rule (d)).

### 4.2 Boundary rules

The following rules constrain the definition and prevent conflation of related but distinct
phenomena. The rules apply identically to **English and Hindi** responses.

**(a) Not every incorrect answer is a hallucination.** Correctness (Section 5.2) and
hallucination (Section 5.3) are separate annotation dimensions. A response may be
*Incorrect* because it is incomplete, off-target, or refuses to answer, without containing
any materially false or unsupported *claim presented as true*. Only responses that assert
such a claim are hallucinated. The full Correctness × Hallucination decision matrix is
given in Section 5.7.

**(b) A refusal/no-answer is not a hallucination.** A response that explicitly declines to
answer, states that it does not know, or provides no substantive answer is coded as a
refusal/no-answer. It is **never** coded as hallucinated and is excluded from hallucination
rate denominators (Section 10.6). Reporting it separately prevents a model from achieving an
artificially low hallucination rate by refusing many questions.

**(c) Different wording is not a hallucination.** A response that conveys the same
substantive content as the reference in different words — including a fluent Hindi
paraphrase of a correct English answer, or a correct answer expressed with different
phrasing/units/style — is not hallucinated. Divergence in form is not divergence in truth.

**(d) Absence from the short `Expected Answer` is not automatically hallucination.** Many
`Expected Answer` values in the finalized bank are very short (Section 2.3). A claim that is
absent from the short `Expected Answer` is **not automatically hallucinated** if it is
independently supported by the designated `Source` or by reliably verifiable evidence. The
`Expected Answer` is the primary anchor, but the `Source` and reliable evidence decide
support when the `Expected Answer` is silent.

**(e) Unverifiable important claims are flagged, not guessed.** If a claim is important to
the answer and **cannot be verified** from the `Expected Answer`, the designated `Source`,
or reliable evidence available to the annotator, the annotator records the case as
**flag for adjudication** rather than guessing a label (Sections 6 and 8).

**(f) The operational definition is language-invariant.** The same claim-level criteria are
applied to English and Hindi responses. A Hindi response is not judged by looser or stricter
standards; any difference in hallucination outcomes between languages is an empirical
finding, not an annotation artifact.

### 4.3 Literature grounding of the definition

The definition is grounded in the hallucination/factuality literature reviewed for this
project. The repository's literature review is currently being finalized
(`literature/literature_matrix.csv` and `paper/references.bib` contain no verified entries
at the time of writing), so citation entries cannot yet be supplied; each required citation
is marked with `[REF NEEDED]` and will be replaced once the review is verified (Section 14
and Appendix A). In particular, the notion of hallucination as fluent but **unfaithful
and/or unsupported content** in neural text generation is adopted as conceptual background
`[REF NEEDED: hallucination / factuality survey]`, and the emphasis on **verifiability
against designated evidence** and on separating **non-answer behaviour from hallucination**
follows standard factuality-evaluation practice `[REF NEEDED: factuality evaluation,
citation support]`. BHRAM-IL is acknowledged as related large-scale benchmark context for
hallucination in Indian languages `[REF NEEDED: BHRAM-IL]`; it is discussed further in
Section 14, and, crucially, the annotation taxonomy of this study (Section 5) is a
**study-specific operational taxonomy** — it is not claimed to be derived from BHRAM-IL or
any single prior work.

## 5. Annotation Scheme

Each annotation unit (one model response to one language-specific prompt) receives a set of
labels defined in this section. The scheme is a **study-specific operational taxonomy**:
it is designed to serve the paired English–Hindi comparison and is defined entirely by the
operational criteria below. It is **not** claimed to be a reproduction, copy, or direct
adaptation of the BHRAM-IL taxonomy or of any other external taxonomy (Section 14).

### 5.1 Annotation fields

Every annotation record contains exactly the following fields:

| Field | Type | Allowed values / format |
|---|---|---|
| `question_id` | string | Underlying question identifier (`Q001`–`Q200`). |
| `language` | string | `en` or `hi`. |
| `category` | string | Question-bank category: `Factual`, `Numerical`, `Reasoning`, `Cultural/India-specific` (Section 2.3, item 1). |
| `model` | string | Exact model identifier and version snapshot used to generate the response. |
| `correctness` | categorical | `Correct` / `Incorrect` (Section 5.2). |
| `hallucination` | categorical | `Yes` / `No` (Section 5.3). |
| `hallucination_type` | categorical | One of the six study-specific types (Section 5.4); recorded only when `hallucination = Yes`, otherwise `NA`. |
| `severity` | categorical | `Minor` / `Major` (Section 5.5); recorded only when `hallucination = Yes`, otherwise `NA`. |
| `evidence_reference` | string | Which part of the designated evidence was used to reach the decision (e.g., `Expected Answer` for `Q007`, or `Source: <sketch>`, or “flag—not verifiable”); Section 6. |
| `annotator` | string | `A1` or `A2` (final adjudicated records additionally carry `FINAL` origin in the adjudicated file; Section 8). |
| `annotation_note` | free text | Concise justification, especially for `Incorrect`, `Yes`, `Other/Mixed`, `flag for adjudication`, and any boundary decision. |

The raw response text and the question's `Expected Answer`/`Source` are attached to each
annotation unit from `responses/raw_responses/` and the question bank at ingestion time; they
are not duplicated into every annotation record.

### 5.2 Correctness

`correctness` is a binary judgment on whether the response substantively answers the
question as posed.

- **Correct** — The response provides a substantive answer that is consistent with the
  designated reference evidence. Minor stylistic differences, alternative but true
  phrasings, or correct supplementary detail supported by the evidence do not make a
  response Incorrect.
- **Incorrect** — The response fails to substantively answer the question: it provides an
  answer that is materially inconsistent with the reference evidence; it asserts answer
  content that is wrong; it omits a required part of the answer so that the response is
  materially incomplete; it is off-topic; or it declines to answer (refusal/no-answer,
  Section 5.6, case R).

A response can be `Incorrect` **without** being hallucinated — for example, a refusal,
a material omission, or a purely hedged non-answer. Correctness and hallucination are
therefore recorded as **independent dimensions** (Section 5.7).

### 5.3 Hallucination

`hallucination` is a binary judgment of whether **any claim in the response** satisfies the
operational definition of Section 4.

- **Yes** — At least one claim in the response is a materially false, fabricated,
  contradictory, or unsupported factual claim presented as true and not justified by the
  designated reference answer/source or reliable evidence.
- **No** — The response contains no such claim. This includes correct responses, refusals,
  hedged non-answers, and incomplete responses that assert nothing false or unsupported.

The binary `Yes`/`No` decision is the **primary outcome** of the study (the variable used in
the paired statistical tests, Section 11). When `hallucination = Yes`, annotators additionally
record `hallucination_type` and `severity`.

### 5.4 Hallucination types (study-specific taxonomy)

`hallucination_type` classifies the *form* of the hallucinated claim(s) when
`hallucination = Yes`. The taxonomy is **operational and study-specific**: each type is
defined by the criteria below for the purposes of this English–Hindi evaluation, and the six
types are exhaustive with respect to this study (the residual category `Other/Mixed` covers
anything that does not fit). This exact six-type arrangement is **not** asserted to originate
from BHRAM-IL or any other named work (Section 14).

| Type | Operational definition |
|---|---|
| **Factual Fabrication** | The response asserts as true a factual claim about the world that does not exist or is not supported by the evidence — invented entities, events, people, dates, places, properties, or sources. The claim has no basis in the designated `Expected Answer`, `Source`, or reliable evidence, and it is false or unverifiable against them. |
| **Factual Contradiction** | The response asserts as true a claim that directly **contradicts** the designated `Expected Answer`/`Source` (or reliable evidence), i.e., it states the opposite of, or a directly incompatible alternative to, what the reference establishes. Internal self-contradiction between two claims in the same response is also classified here when it concerns answer-relevant facts. |
| **Numerical Hallucination** | A numerical claim (count, amount, percentage, date-as-number, measure, currency figure, or computational result) asserted as true is wrong relative to the reference evidence, and the wrongness is an error in the asserted number itself (or the number has no basis in the evidence). Includes invented or misstated statistics, amounts, and computation outputs. |
| **Reasoning/Logical Hallucination** | The response asserts as true a conclusion or an intermediate step that is **not entailed** by the question's premises — a non-sequitur, an invented justification, or a fabricated causal/logical link presented as if it followed from the given information. The flaw is in the asserted chain of reasoning rather than in a discrete factual number named independently. |
| **Cultural/Contextual Hallucination** | The response asserts as true a claim about cultural, social, customary, religious, linguistic, regional, or India-specific context (festivals, traditions, language usage, ethnicity, heritage, practices, or context-dependent facts) that is fabricated, wrong, or unsupported relative to the designated evidence. |
| **Other/Mixed** | The hallucinated content does not fit any single type above, or the response contains multiple hallucinated claims of different types. Annotators **must** enumerate the contributing types and reasons in `annotation_note`. |

**Type-assignment rules**

- **Numerical vs. Reasoning/Logical.** If the asserted claim that fails is a discrete
  number/value (the answer or a component of it), assign `Numerical Hallucination`. If the
  asserted claim that fails is an invented inferential step, justification, or conclusion
  whose error is logical rather than numeric, assign `Reasoning/Logical Hallucination`. When a
  flawed computation both applies a wrong method and asserts a wrong number, assign the type
  that best describes the *primary* asserted claim and record the other aspect in
  `annotation_note`.
- **Factual Fabrication vs. Factual Contradiction.** A claim with **no basis** in the
  evidence is a Fabrication. A claim that is **explicitly incompatible with** the evidence is
  a Contradiction. When both apply (a fabricated claim that also contradicts the reference),
  assign **Factual Contradiction** as primary (it is the sharper, evidence-anchored error)
  and note the fabrication in `annotation_note`.
- **Cultural/Contextual vs. Factual.** If the claim concerns culture/context/India-specific
  material of the kind listed above, assign `Cultural/Contextual Hallucination`, even if in a
  different study it might be called “factual”. The type describes *where* the hallucination
  lives, not a value judgment of it.
- **Multiple claims of one type.** Map each hallucinated claim to its best single type; if all
  claims share one type, record that type. If claims span two or more types, record
  `Other/Mixed`.
- **Consistency with category.** The `hallucination_type` is independent of the question's
  task `category`: e.g., a `Factual` question can produce a `Numerical Hallucination`, and a
  `Reasoning` question can produce a `Factual Fabrication`. Category and type are different
  dimensions and must not be conflated (Section 5.7, final note).

### 5.5 Severity

`severity` rates the potential impact of the hallucinated claim(s), recorded only when
`hallucination = Yes`.

- **Minor** — The hallucinated claim is peripheral to the question: it does not change the
  substantive answer the question asks for, involves low-stakes or cosmetic detail, and
  correcting it would not reverse or undermine the overall answer. Examples: an incidental
  extra sentence containing a false supporting detail while the core answer is correct; a
  wrong parenthetical date in an otherwise correct explanation.
- **Major** — The hallucinated claim (i) constitutes or substantially determines the answer
  to the question (e.g., the wrong number, wrong entity, wrong conclusion is the answer
  itself); (ii) introduces high-stakes false information that would materially mislead a
  reader (wrong identities, figures, responsibilities, safety or health-relevant facts); or
  (iii) touches sensitive cultural, social, or India-specific content in a way that
  misrepresents it. A response whose answer is wrong because of the hallucinated claim is
  `Major` by definition.

**Boundary rule.** When it is not immediately clear whether a claim is `Minor` or `Major`,
annotators weigh whether the claim determines or reverses the answer; if the outcome is still
unclear after consulting the evidence, the case is **flagged for adjudication** (Section 8)
rather than guessed.

### 5.6 Boundary examples (illustrative, not experimental results)

The examples below are illustrative annotation vignettes used to calibrate decision rules.
Each row shows the field values a trained annotator would record under the finalized rules.

| # | Case (illustrative) | correctness | hallucination | type | severity | Notes |
|---|---|---|---|---|---|---|
| 1 | **Correct response.** Q: “What is the capital of France?” EN response: *“Paris is the capital of France.”* Expected Answer: `Paris`. | Correct | No | NA | NA | Fully supported by evidence. |
| 2 | **Incorrect, non-hallucinatory (omission).** Q asks for a capital *and its approximate population*; EN response states only *“Paris.”* | Incorrect | No | NA | NA | Materially incomplete; asserts nothing false. Incomplete ≠ hallucination. |
| 3 | **Fabricated fact.** Q: “What is the national bird of India?” EN response: *“The national bird of India is the Himalayan monal.”* Expected Answer: `Peacock`. | Incorrect | Yes | Factual Fabrication | Major | Invented (wrong) entity presented as fact; determines the answer. |
| 4 | **Contradictory fact.** Reference (Expected Answer `Paris`) and Source establish the capital; response asserts *“The capital of France is Lyon.”* | Incorrect | Yes | Factual Contradiction | Major | Directly contradicts the reference evidence. |
| 5 | **Unsupported extra claim.** Q: “What is the capital of France?” Response: *“The capital is Paris; it was rebuilt in 1789 by Napoleon.”* (correct core; invented, false addition). | Correct* | Yes | Factual Fabrication | Minor | Core answer correct; incidental fabricated extra claim. *If the extra claim were answer-critical, correctness would be `Incorrect`. |
| 6 | **Numerical error.** Q: “What is 25% of 80?” Response: *“25% of 80 is 15.”* Expected Answer: `20`. | Incorrect | Yes | Numerical Hallucination | Major | Wrong asserted number, determines the answer. |
| 7 | **Reasoning error.** Direction/relation puzzle; response asserts an intermediate step that does not follow from the premises to conclude the wrong person is leftmost. | Incorrect | Yes | Reasoning/Logical Hallucination | Major | Flaw lies in the asserted (invented) inference. |
| 8 | **Cultural/Contextual claim.** India-specific festival question; response asserts a false origin/region for the festival with unsupported “traditional” detail. | Incorrect | Yes | Cultural/Contextual Hallucination | Major | Fabricated cultural attribution; also sensitive (see severity rule). |
| 9 | **Refusal / no-answer.** Response: *“I cannot answer that.”* / *“मुझे नहीं पता।”* | Incorrect | No | NA | NA | Refusal: never hallucinated; excluded from hallucination denominators; counted in refusal rate (Section 10.6). |
| 10 | **Ambiguous / unverifiable.** Response asserts an important claim absent from the short `Expected Answer` and not resolvable from the `Source` or available reliable evidence. | (pending) | (pending) | (pending) | (pending) | **Flag for adjudication**; annotators record `evidence_reference` and do **not** guess (Sections 4.2(e), 6, 8). |

Annotators are instructed that the distinction between cases 1–2 and 3–8 reduces to: *does
the response assert a materially false/fabricated/contradictory/unsupported claim as true?*
If yes → `hallucination = Yes` (and its type+severity); if the response is wrong only by
omission, refusal, hedging, or off-topic emptiness → `hallucination = No`.

### 5.7 Correctness × Hallucination decision matrix

Because correctness and hallucination are independent dimensions, every annotated response
falls into exactly one cell of the following matrix:

|  | `hallucination = No` | `hallucination = Yes` |
|---|---|---|
| **`correctness = Correct`** | Canonical correct response. All asserted claims supported/true; answer consistent with reference. *(Example 1)* | Core answer correct, but the response additionally asserts an incidental fabricated/unsupported claim that does not determine the answer. *(Example 5)* |
| **`correctness = Incorrect`** | Wrong by omission, refusal, hedging, or off-topic emptiness with **no** material false/unsupported claim asserted as true. *(Examples 2, 9)* | Answer is wrong and the wrongness is carried by one or more false/fabricated/contradictory/unsupported claims asserted as true. *(Examples 3, 4, 6, 7, 8)* |

Reading guide for annotators:

1. Judge `correctness` against “does the response substantively answer the question, consistent
   with the reference evidence?” (Section 5.2).
2. Judge `hallucination` against claim-level criteria (Sections 4 and 5.3).
3. **Do not** equate `Incorrect` with `Yes` and do **not** equate `Correct` with `No`.
4. **Task category is not hallucination type.** The question's `category`
   (`Factual`/`Numerical`/`Reasoning`/`Cultural/India-specific`) describes what the question
   is about; `hallucination_type` describes the form of the failed claim. The two are recorded
   and analyzed separately (Sections 10 and 12).

## 6. Evidence / Reference Protocol

### 6.1 Designated reference evidence

Every question in the finalized bank is accompanied by an `Expected Answer` and a `Source`
(Section 2.2). Together these constitute the **designated reference evidence (DRE)** for the
question. Additional reliable documentary evidence may be designated per question by the
research team when needed; it is recorded with the question (provenance-preserving, no
invented URLs).

### 6.2 Use of the evidence during annotation

Annotators evaluate each response **against the expected answer and its source**, not against
the short answer value alone or personal recollection alone, according to the following
hierarchy:

1. **`Expected Answer`** — the first anchor. If the response's claims are consistent with it,
   the claim is supported at this level.
2. **`Source` and designated supporting evidence** — because many `Expected Answer` values are
   very short (e.g., a single character or number; Section 2.3, item 3), the `Expected
   Answer` is frequently **insufficient on its own**. Annotators must consult the designated
   `Source` (and any designated supporting evidence) to verify substantively whether a claim
   is true, false, or unverifiable. A claim absent from the short `Expected Answer` is not
   hallucinated if it is supported by the `Source`/reliable evidence (Section 4.2(d)).
3. **Reliably verifiable general knowledge** — may corroborate (or refute) a claim only when
   the fact is uncontroversial and verifiable; this is an auxiliary check, not the primary
   basis, and any such reliance is recorded in `annotation_note`.

### 6.3 Unverifiable claims

If a claim that is **important** to the answer **cannot be verified** from the `Expected
Answer`, the designated `Source`, or reliable evidence available to the annotator, the
annotator **flags the case for adjudication** and records it as such in `annotation_note`
and `evidence_reference` (e.g., “flag—no evidence located”). The annotator does **not**
guess a hallucination label for that claim (Sections 4.2(e) and 8). Flagged cases are tracked
and resolved during adjudication; they are reported alongside the final labels.

### 6.4 Provenance discipline

No URLs, DOIs, or bibliographic citations are invented. The `evidence_reference` field
records only what is actually present in the question bank (`Expected Answer` text and the
`Source` label) plus any explicitly designated supporting evidence. Where a literature
citation is needed, the `[REF NEEDED]` convention of Appendix A applies.

## 7. Two-Independent-Annotator Protocol

### 7.1 Roles

Two annotators — **A1** and **A2** — annotate the **same full set** of model responses. Both
annotators evaluate responses under identical instructions (the finalized scheme of Sections
4–6) and identical materials (question, response, `Expected Answer`, `Source`, designated
supporting evidence).

### 7.2 Independence

A1 and A2 **independently annotate responses without seeing each other's labels or
decisions**: they work in separate annotation stores (`annotations/annotator_1/`,
`annotations/annotator_2/`), record their decisions before any comparison step, and do not
discuss individual items until the comparison step (Section 8.2). The annotation set ordering
is identical for both annotators, but each annotator's decisions are concealed from the other
until both have completed their independent annotation.

Annotators are **not blinded to the language being evaluated**: each unit is presented with
its prompt language (`en` or `hi`) explicitly identified, and neither annotator is prevented
from reading or assessing the response in its original language. Independence refers
strictly to the annotation decisions — each annotator records their own labels without seeing
the other's labels or decisions — and does not imply a language-blind evaluation.

### 7.3 Records

For every unit, each annotator records **all** of the following fields (Section 5.1):
`correctness`, `hallucination`, `hallucination_type`, `severity`, `evidence_reference`, and
`annotation_note` (together with the unit's `question_id`, `language`, `category`, and
`model`). Both annotators must be able to justify every label by referencing the evidence
used (Section 6).

### 7.4 Language invariance

A1 and A2 apply the **same criteria to English and Hindi responses**. Any difference in
treatment between languages would confound the comparison; therefore, mixed-language
response spans (e.g., a Hindi question answered in partly English text) are annotated with
the same claim-level rules, and the language of the *prompt* determines the unit's
`language` field.

### 7.5 Pilot calibration

Before full annotation, both annotators complete a pilot round on a small held-out sample
(e.g., 20–30 units) to calibrate the boundary rules of Sections 4–5 and to identify
ambiguous cases early. A1/A2 agreement on the pilot informs whether the guidelines need
clarification before the full round; the pilot results are retained for reporting but are
re-annotated in the full round when the guidelines change. (Pilot sample size is a
pre-registration detail; the exact size will be documented in the annotation log.)

## 8. Disagreement Resolution

### 8.1 Aim

Disagreements between A1 and A2 are resolved through a defined procedure that (i) preserves
both original annotations, and (ii) produces a single **final adjudicated label** stored
separately from the original annotations.

### 8.2 Procedure

1. **Comparison.** Merge the A1 and A2 annotation files on the annotation unit and fieldwise
   compare `correctness`, `hallucination`, `hallucination_type`, and `severity`.
2. **Identification.** For each disagreement, identify the **exact claim** (or omission) in
   the response that drives the difference (e.g., which sentence/assertion leads A1 to `Yes`
   but A2 to `No`).
3. **Re-reading.** Re-read the question, the model response, the `Expected Answer`, and the
   `Source` for that unit, treating these as the sole basis for the decision (Section 6).
4. **Rule application.** Apply the predefined annotation rules (Sections 4 and 5) to the
   identified claim, checking whether the dispute is resolved by the boundary rules
   (e.g., omission vs. fabrication; `Minor` vs. `Major`).
5. **Adjudication / discussion.** If the disagreement remains after steps 2–4, the case
   proceeds to adjudication: the two annotators (with the methodology owner where needed)
   discuss the case against the evidence; a **third reviewer** may be consulted when the
   disagreement persists. The adjudicated decision must be evidence-grounded and recorded
   with its rationale.
6. **Final labels.** The agreed/adjudicated outcome is written to a **separate** final-labels
   store (`annotations/final_labels/`) carrying the `annotator = FINAL` provenance marker.

### 8.3 Preservation rule

**Original A1 and A2 annotations are never overwritten.** The final adjudicated labels are
stored separately and joined to the originals by annotation-unit key. This preserves, for
every unit: A1's labels, A2's labels, the final label, and (where applicable) the
adjudication rationale. The distinction between original and final labels is therefore
always recoverable for analysis and reporting (including inter-annotator agreement computed
on the *original* labels, Section 9).

## 9. Inter-Annotator Agreement

Inter-annotator agreement (IAA) is computed on the **original A1 and A2 labels** (before
adjudication) to measure the reliability of the annotation scheme.

### 9.1 Primary measure: Cohen's kappa

Because there are **two annotators** and the label variables are **categorical**, **Cohen's
κ (kappa)** is the primary IAA measure. For a categorical variable with any number of
categories:

```
κ = (p_o − p_e) / (1 − p_e)

p_o = observed proportion of agreement       = (1/N) · Σ_i n_ii
p_e = expected agreement under chance        = (1/N²) · Σ_k (row_k · col_k)
```

where `N` is the number of jointly annotated units, `n_ii` the count of units in agreement on
category `i`, and `row_k`, `col_k` the marginal counts for category `k` across the two
annotators. κ = 1 indicates perfect agreement; κ = 0 indicates agreement no better than
chance; negative values indicate agreement below chance.

### 9.2 Supplementary measure: raw percentage agreement

Raw percentage agreement is reported as a supplementary, transparent measure:

```
raw agreement (%) = p_o × 100
```

Raw agreement is useful because κ can be low even when agreement is high when label
distributions are highly skewed (see 9.4); both numbers are reported together.

### 9.3 Variables and scopes

IAA is reported **separately** for each annotated variable:

- `correctness` (`Correct`/`Incorrect`), computed over all units;
- `hallucination` (`Yes`/`No`), computed over all units — this is the primary outcome
  variable and its agreement is the most important to interpret;
- `hallucination_type` (six categories), computed over units **where `hallucination` applies**
  — i.e., the subset of units in which both annotators could meaningfully record a type
  (units whose final-agreed `hallucination = Yes`, or the union of units flagged `Yes` by
  either annotator, as documented in the annotation log);
- `severity` (`Minor`/`Major`), computed over the same applicable subset.

The scope definitions for type/severity subsets are recorded in the annotation log so that
the reported denominators are explicit and reproducible.

### 9.4 Interpretation: no rigid universal threshold

The study does **not** impose a rigid universal κ threshold (e.g., a single “acceptable ≥
0.8” cutoff) that is applied mechanically. Instead, agreement is **interpreted together
with**:

- the **label distribution** (base rates and marginal asymmetry) for each variable, since low
  prevalence can deflate κ even at high raw agreement, and high prevalence can inflate it;
- the **disagreement patterns** (which cells concentrate disagreement, e.g., `Yes↔No`
  confusions vs. type-boundary confusions), computed from the A1×A2 contingency table; and
- the **pilot results** and any **post-hoc κ confidence intervals** computed from the data.

Agreement statistics support two uses in this study: (i) documenting the reliability of the
annotated outcome variable `hallucination`, and (ii) guiding whether guideline clarifications
or additional adjudication are warranted. All IAA computations are performed on the
original labels per Section 8.3.

## 10. Evaluation Metrics

All metrics below are computed on the **final adjudicated labels** (Section 8), and all
denominators follow the **evaluable-response** convention defined in Section 10.1. No
numerical values are reported here: the experiment has not been run.

### 10.1 Definitions

For any subset `S` of annotated units (a scope: overall, a language, a model, or a task
category):

- `N_S` — the **total number of annotated responses** in `S` (final labels).
- `R_S` — the number of **refusal / no-answer** responses in `S` (Section 10.6).
- `N_eval(S) = N_S − R_S` — the number of **evaluable responses** in `S`. Refusals are
  excluded from evaluable denominators because refusal-to-answer is not a hallucination
  (Section 4.2(b)); a model cannot lower its hallucination rate by refusing questions.
- `H_S` — the number of **hallucinated evaluable responses** in `S`
  (`hallucination = Yes` on the final label).

The same definitions apply identically to English and Hindi, to each model, and to each
category. When inspection reveals responses that are empty/failed generations (no content
beyond the prompt echo), they are recorded and their handling is reported explicitly as part
of `N_S` accounting rather than silently dropped.

### 10.2 Overall hallucination rate

```
HR = ( H_overall / N_eval(overall) ) × 100
```

### 10.3 Language hallucination rates

```
HR_English = ( H_en / N_eval(en) ) × 100
HR_Hindi   = ( H_hi / N_eval(hi) ) × 100
```

where `en`/`hi` scope `S` = all evaluable response units in that language (across all
models and categories, or per stratum as specified).

### 10.4 Model-wise hallucination rate

For each model `m`:

```
HR_m = ( H_m / N_eval(m) ) × 100
```

Model-wise rates are additionally computed **per language** (`HR_m_en`, `HR_m_hi`) so that
language behavior can be compared within a model, as the paired design requires
(Section 11.3).

### 10.5 Category-wise hallucination rate

For each task category `c` (`Factual`, `Numerical`, `Reasoning`, `Cultural/India-specific`):

```
HR_c = ( H_c / N_eval(c) ) × 100
```

A language × category breakdown (`HR_c_en`, `HR_c_hi`) is computed for RQ4.

### 10.6 Refusal rate (reported separately)

```
RefusalRate_S = ( R_S / N_S ) × 100        (for any scope S: overall, language, model, category)
```

Refusal/no-answer responses are **not hallucinations** and are **not counted as hallucinated
responses**; they are excluded from hallucination-rate denominators (Section 10.1) and
reported as a **separate rate** so that refusal behavior is visible and interpretable on its
own.

### 10.7 Delta hallucination rate (ΔHR)

```
ΔHR = HR_Hindi − HR_English        (difference of the language rates, in percentage points)
```

Interpretation is strictly numeric and language-neutral:

- **ΔHR > 0** — the observed Hindi rate is **numerically higher** than the English rate;
- **ΔHR < 0** — the observed Hindi rate is **numerically lower** than the English rate;
- **ΔHR = 0** — the observed rates are numerically equal.

No evaluative claim (that one language is “better” or “worse”) is attached to the sign of
ΔHR; ΔHR is a descriptive and testable quantity. Nominal (unpaired) interpretations are
avoided because the design is paired: ΔHR is used as the effect-size-style summary and is
tested with the paired procedures of Section 11.

### 10.8 Confidence intervals

Where reported, rates are accompanied by confidence intervals computed with an appropriate
method for proportions (e.g., the Wilson interval) and the language-rate difference is
accompanied by an interval appropriate for paired binary data. The exact method is fixed in
the analysis protocol before results are produced, so that no method is chosen after seeing
the data.

### 10.9 Reporting conventions

- No hallucination/refusal rate, P value, or confidence interval appears in this document or
  in any interim artifact until annotation and adjudication are complete.
- Every reported rate states its scope and its raw counts (`H`, `N_eval`, `R`, `N_S`) so the
  rate is recomputable from the released labels.

## 11. Statistical Analysis Plan

### 11.1 Primary outcome and design

The primary outcome is the binary `hallucination` status (`Yes`/`No` on the final
adjudicated label). Because the **same underlying question** is represented in English and
Hindi and answered by the **same model**, the primary language comparison is **paired at the
question (and question×model) level**: each pair contributes an `(en, hi)` outcome pair.

### 11.2 Primary comparison: McNemar's test

The primary statistical test for the language comparison (RQ1, RQ5) is **McNemar's test for
paired binary outcomes** on the 2×2 table of question-level outcomes:

```
                Hindi no-halluc   Hindi hallucinated
English no-halluc      n00              n01
English hallucinated   n10              n11
```

Using the final evaluable labels per language, the table counts (over paired units) are:

- `n00` — neither language hallucinated;
- `n01` — English not hallucinated, Hindi hallucinated;
- `n10` — English hallucinated, Hindi not hallucinated;
- `n11` — both languages hallucinated.

**Hypotheses (two-sided, α = 0.05):**

- **H0:** English and Hindi have **equal marginal hallucination probability**
  (equivalently, discordant cells are equiprobable in expectation: E[n01] = E[n10]).
- **H1:** English and Hindi have **different marginal hallucination probability**.

Test statistics: McNemar's asymptotic chi-squared statistic with Edward's continuity
correction

```
χ² = ( |n01 − n10| − 1 )² / (n01 + n10),  df = 1
```

and, when the number of discordant pairs `n01 + n10` is small (convention: < 25), the exact
binomial version on the discordant pairs (number of Hindi-only hallucinations ~ Binomial(n01
+ n10, 0.5)) is used instead, since the asymptotic approximation is unreliable for sparse
tables.

### 11.3 Handling of refusals in the paired comparison

A **refusal / no-answer response is not a hallucination** (Sections 4.2(b) and 10.6): it is
never coded `hallucination = Yes`, and it is not counted as a hallucinated response.
Refusal behavior is reported separately through the **refusal rate** (Section 10.6).

Accordingly, the primary McNemar hallucination comparison is restricted to **paired question
instances for which both the English and the Hindi response have an evaluable hallucination
status** — i.e., neither member of the pair is a refusal/no-answer and both members carry a
final `hallucination` label of `Yes` or `No`. A refusal is **not silently treated as a
non-hallucinated response**: pairs excluded because either side lacks an evaluable status are
(i) counted in the descriptive per-language rates (whose denominators are the per-language
evaluable sets, Section 10.1) and (ii) reported transparently, including the number and
pattern of excluded pairs (counts per language and model, and the language mix of the
refusals within those pairs), so that a reader can see how much of the data the paired test
rests on. This rule is fixed before the analysis so that handling cannot depend on results.

As a **secondary sensitivity analysis** that may be conducted later, the paired comparison
can be re-examined under defined alternative refusal-assumption regimes (e.g., a documented
imputation rule for one or both refusal sides, or a complete-case contrast) to assess how
sensitive the primary result is to the exclusion of refusal pairs. No such analysis is run or
claimed in this document; any future sensitivity result would be reported as secondary and
kept clearly separate from the primary test.

### 11.4 Model-wise and category-wise comparisons

- **Model-wise (RQ2):** for each model, the same paired English–Hindi comparison
  (McNemar) is performed over that model's question-level pair set, so that language is a
  within-model factor. The model list is 3–4 models.
- **Category-wise (RQ4):** for each task category, the same paired English–Hindi comparison
  is performed over the pairs belonging to that category, so that language is a within-question
  factor within category. Category ΔHR values are reported alongside the tests.

These comparisons follow the **same paired logic** wherever the data structure supports a
pair (both languages evaluable for that question×model unit); unpaired strata are reported
descriptively without a paired test.

### 11.5 Multiple-comparison correction

If multiple hypothesis tests are conducted (the default: one per model and one per category),
the **Holm (step-down Bonferroni) correction** is applied within each family of tests, and
both raw and Holm-adjusted p-values are reported. Families are defined as (i) the model-wise
tests and (ii) the category-wise tests; the overall language test is treated as the primary
pre-specified test (no correction applied to it, and this is stated in the report).

### 11.6 What is reported

For each paired comparison, the report provides:

- English HR and Hindi HR for the scope (with raw counts `H`, `N_eval` per language);
- ΔHR;
- the McNemar test statistic (or exact-test note) and the p-value;
- a confidence interval for the language-rate difference where appropriate (per Section 10.8),
  and the counts of excluded pairs (Section 11.3).

No p-value, test statistic, or confidence interval is produced or claimed before the
experiment is run and annotated.

### 11.7 Possible secondary analysis

If the final data structure (multiple models × paired questions × categories) warrants a
repeated-measures/mixed-effects analysis — e.g., a generalized linear mixed-effects model
(GLIMM) with a logit link, random intercepts for question and model, and fixed effects for
language, category, and model, with Holm-corrected contrasts — it is described as a
**possible secondary analysis** to check robustness of the primary paired results. This
section does not assert that such an analysis will be necessary or that any specific result
will follow; it merely fixes the analysis plan so that such a model, if fitted, is a stated
robustness check rather than an ad-hoc addition.

## 12. Qualitative Error Analysis

### 12.1 Purpose

After annotation and adjudication, hallucinated responses are summarized **qualitatively** to
characterize *where* and *in what form* hallucinations occur. Qualitative analysis is
descriptive and pattern-oriented; it supports RQ3 and contextualizes the quantitative rates
of Sections 10–11.

### 12.2 Planned summaries

Hallucinated responses (from the final labels) will be summarized by:

- **`hallucination_type`** — frequency distribution of the six types (Section 5.4), overall
  and per language, model, and task category;
- **`severity`** — distribution of `Minor`/`Major`, and the cross-tabulation of severity ×
  type × language;
- **language** — type/severity distributions for English compared with Hindi, to inspect
  whether any qualitative difference mirrors the quantitative ΔHR;
- **model** — per-model type/severity profiles;
- **task category** — type/severity profiles per category (illustrating, e.g., whether
  `Numerical` questions surface `Numerical Hallucination` or other types, such as
  `Reasoning/Logical Hallucination`).

### 12.3 Pattern identification

The analysis will identify **recurring patterns** of the kinds defined by the taxonomy, such
as:

- fabricated facts (invented entities, events, source attributions);
- factual contradictions (claims that invert the designated reference evidence);
- numerical hallucinations (wrong or invented figures, amounts, percentages, computation
  outputs);
- reasoning/logical errors (asserted steps that do not follow from premises);
- cultural/contextual unsupported claims (fabricated or misattributed India-specific and
  cultural content).

These categories are the *target dimensions of analysis*, not claims about what will be
found. No observed pattern is asserted before data collection; the realized patterns will be
reported with representative response excerpts (paraphrased where needed) after annotation,
together with counts.

### 12.4 Reporting format

Qualitative findings are reported as (i) contingency tables and simple descriptive
summaries produced from the labels (`analysis/error_analysis.py` conventions), and
(ii) a narrative synthesis with representative examples labeled by `(question_id, language,
model, category, type, severity)` so they can be traced to the raw responses and evidence.

## 13. Reproducibility

The finalized experiment must preserve every artifact needed to reproduce the study from the
question bank through the final tables/figures. The artifact list below maps each item to its
repository location (locations follow the existing project structure).

| Artifact | Location / notes |
|---|---|
| Finalized question bank | `data/raw/question_bank.xlsx` (unmodified; columns `Question ID`, `Category`, `English Question`, `Hindi Question`, `Expected Answer`, `Source`). |
| Question IDs and English–Hindi pairings | One row per underlying question; `Q001`–`Q200`; pairings fixed by the wide-format rows. |
| Category assignment | `Category` column of the question bank; mapping to internal identifiers recorded at ingestion (Section 2.3, item 1). |
| Reference evidence (`Expected Answer`, `Source`) | Question bank; supporting-evidence designation notes recorded in the question metadata. |
| Exact model names/versions | `experiments/config.py:MODEL_IDS` and the run manifest (`responses/raw_responses/…__manifest.json`). |
| Prompt templates | `experiments/prompts.py` (system prompt and per-language user templates), byte-identical across languages except the question text and the language marker. |
| Generation settings | Run manifest: temperature, max tokens, top-p, seed, and provider-specific parameters, identical for `en` and `hi` within a model. |
| Raw responses | `responses/raw_responses/{run_id}/` — unmodified model outputs plus prompt echo and metadata. |
| A1 annotations | `annotations/annotator_1/` (original, never overwritten). |
| A2 annotations | `annotations/annotator_2/` (original, never overwritten). |
| Adjudicated labels | `annotations/final_labels/` — final labels with `FINAL` provenance, joined to the originals (Section 8.3). |
| Annotation artifact versions | Versioned annotation guidelines, pilot log, and adjudication log so label definitions are traceable. |
| Analysis scripts | `analysis/*.py` (hallucination rates, statistical tests, error analysis), `notebooks/` — version-locked with the commit. |
| Environment | `requirements.txt`, Python version, and package versions recorded at run time. |
| Final tables/figures | `results/tables/`, `results/figures/` — regenerated from the labels by the analysis scripts, with the run manifest hash recorded so that artifacts trace to code and data. |

**Integrity commitments.** Raw responses are stored unmodified; original A1/A2 annotations
are never overwritten (Section 8.3); committed artifacts carry the repository commit hash in
the run manifest; and every quantitative output is recomputable from the released labels
(Section 10.9). Any downstream normalization (e.g., category-name mapping) is applied in a
derived file, not in place, and is documented.

## 14. Literature Grounding

### 14.1 Status of the project's literature record

At the time of writing, the repository contains **no verified literature entries**:
`literature/literature_matrix.csv` contains only its header row, and
`paper/references.bib` is intentionally empty. Consequently:

- **No citation is fabricated** anywhere in this document or in the project artifacts;
- every place a literature citation is required carries the **`[REF NEEDED]`** placeholder of
  Appendix A, to be replaced only when a paper has been read and verified and recorded in
  `literature/literature_matrix.csv` and `paper/references.bib`;
- no authorship, year, venue, or DOI is invented.

### 14.2 Required literature anchors (placeholders)

The following citation types are needed to complete the literature grounding; all are
currently `[REF NEEDED]`, pending verification:

1. Survey/introduction to hallucination in neural text generation (conceptual basis for the
   “fluent but unfaithful/unsupported content” framing adopted in Section 4.3)
   `[REF NEEDED: hallucination / factuality survey]`.
2. Sources establishing standard factuality-evaluation practice — verification against
   reference evidence, and separate treatment of non-answer behavior — supporting Sections
   4.2 and 6 `[REF NEEDED: factuality evaluation, citation support]`.
3. BHRAM-IL, a large multilingual benchmark for hallucination in Indian languages
   `[REF NEEDED: BHRAM-IL]`. BHRAM-IL is acknowledged as related benchmark context in the
   project's README and is relevant related work *for the introduction and related-work
   section of the paper*.

### 14.3 Relationship between this study's taxonomy and prior work

The **six-type annotation taxonomy** of Section 5.4 (`Factual Fabrication`, `Factual
Contradiction`, `Numerical Hallucination`, `Reasoning/Logical Hallucination`,
`Cultural/Contextual Hallucination`, `Other/Mixed`) is a **study-specific operational
taxonomy** constructed for this paired English–Hindi evaluation. It is **explicitly not
claimed to be copied from BHRAM-IL** (or from any other single paper). The design, data
scale, and evaluation objectives differ between this study and BHRAM-IL (controlled paired
EN–HI comparison with human annotation vs. large-scale multilingual benchmarking); when
BHRAM-IL is eventually cited, the paper will (i) describe BHRAM-IL's design and taxonomy in
its own terms, and (ii) state clearly that the present study's annotation scheme is defined
independently for its own research questions, even where it happens to use similar-sounding
labels.

## 15. Limitations of the Methodology

The following limitations are acknowledged up front; the paper will discuss them in
proportion to their realized impact once results exist.

1. **Dependence on reference quality.** All hallucination judgments are evaluated against the
   designated reference evidence (`Expected Answer`, `Source`, supporting evidence). Errors
   or gaps in the reference material directly bound the validity of the labels; in
   particular, short `Expected Answer` values (Section 2.3, item 3) place additional weight on
   the `Source` and on reliable evidence, whose completeness the study does not control.
2. **Subjectivity in human annotation.** Despite the operational definitions, boundary
   judgments (e.g., omission vs. fabrication, `Minor` vs. `Major`) retain an irreducible
   subjective component; this is measured and limited by the two-annotator protocol and by
   reporting IAA (Sections 7, 9), not eliminated.
3. **Ambiguity in cultural/contextual questions.** `Cultural/India-specific` content is
   particularly sensitive to regional variability and to the annotators' own background;
   cases that cannot be resolved from evidence are flagged for adjudication (Section 6.3), and
   residual ambiguity is reported.
4. **Translation/semantic-equivalence risk.** The English–Hindi pairing intends semantic
   equivalence, but translation and cross-lingual reformulation can introduce subtle meaning
   shifts or differences in register; an English response and a Hindi response may therefore
   diverge in ways unrelated to hallucination. The paired design controls question content
   but not translation quality; translation review records (Section 13) bound this risk.
5. **Limited number of evaluated models.** With 3–4 LLMs, model-level conclusions are
   descriptive; generalization claims about “LLMs in general” are avoided.
6. **Refusal handling.** Refusals are excluded from hallucination denominators and analyzed
   separately (Sections 4.2(b), 10.6, 11.3). This is principled but means the hallucination
   rates describe *evaluable* answers only, and models with different refusal behavior are
   compared on different subpopulations of items; the refusal rate is always reported
   alongside HR so the two can be read together.
7. **Possible class imbalance.** If the frequency of `hallucination = Yes` is low (or high),
   prevalence effects will affect both IAA (Section 9.4) and the statistical power of paired
   tests (sparse discordant cells, Section 11.2); the plan reports counts and uses exact tests
   where the asymptotics are unreliable.
8. **Scope of the annotation unit.** Each unit yields a whole-response summary label set;
   span-level labeling of individual hallucinated sentences is not produced. Consequently,
   measures such as “number of hallucinated clauses per response” are out of scope, and
   `severity` summarizes the response-level impact of the worst claim (Sections 5.4–5.5 `[REF
   NEEDED: span-level vs. response-level hallucination labeling practice, citation support]`).

## Appendix A. Reference Conventions

### A.1 The `[REF NEEDED]` placeholder

Wherever this document requires literature support but the bibliographic entry is not yet
available in the repository (no verified entry exists in `literature/literature_matrix.csv`
and `paper/references.bib` is empty at the time of writing), the citation is marked as:

```
[REF NEEDED: <description of the needed citation>]
```

Semantics of the placeholder:

- It is **not** a citation and must never be converted into a bibliography entry;
- it must be replaced only by a **verified** reference — a paper that has been read,
  recorded in `literature/literature_matrix.csv`, and entered into `paper/references.bib`;
- no author, title, year, venue, or DOI is invented to fill it.

### A.2 Placeholders used in this document

| Location | Placeholder |
|---|---|
| Section 4.3 | `[REF NEEDED: hallucination / factuality survey]` |
| Section 4.3 | `[REF NEEDED: factuality evaluation, citation support]` |
| Section 4.3 | `[REF NEEDED: BHRAM-IL]` |
| Section 14.2, item 1 | `[REF NEEDED: hallucination / factuality survey]` |
| Section 14.2, item 2 | `[REF NEEDED: factuality evaluation, citation support]` |
| Section 14.2, item 3 | `[REF NEEDED: BHRAM-IL]` |
| Section 15, item 8 | `[REF NEEDED: span-level vs. response-level hallucination labeling practice, citation support]` |

### A.3 Data provenance note

All dataset facts cited in this document (200 underlying questions; 50 per category;
`Q001`–`Q200`; the six columns `Question ID`, `Category`, `English Question`, `Hindi
Question`, `Expected Answer`, `Source`; 400 language-specific prompts per model) are taken
from a read-only inspection of `data/raw/question_bank.xlsx`. That file is **not modified**
by this document or its author; the category-name normalization requirement (Section 2.3,
item 1) is documented for the pipeline but is applied in derived files only.

---

*End of document.* The methodology defined above is internally consistent with the finalized
200-question dataset, is aligned with research questions RQ1–RQ5, distinguishes correctness
from hallucination, task category from hallucination type, and refusal from hallucination,
preserves the paired English–Hindi design, and contains no fabricated results or citations.