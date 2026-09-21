# A Comparative Evaluation of Hallucination in Large Language Models for English and Indian Languages

> **Project status: research in progress — Day 1 repository setup only.**
>
> The experiment described below has **not been conducted**. No questions,
> model responses, annotations, or results exist in this repository yet.
> Everything marked *planned* or *preliminary* is subject to change.

---

## Overview

This repository supports a planned one-week **empirical research study** that
compares **hallucination** in large language models (LLMs) when the **same
underlying question** is asked in **English** and in **Hindi**.

The study is a **controlled English–Hindi paired-question comparison**, not a
generic multilingual benchmark. It is scoped to four planned task categories:

- **Factual** — questions with verifiable, source-based answers.
- **Numerical** — questions requiring numeric answers or arithmetic.
- **Reasoning** — questions requiring multi-step inference.
- **Cultural/Contextual** — questions that depend on cultural or contextual
  knowledge.

## Motivation

LLMs are known to generate fluent but incorrect ("hallucinated") content, and
most hallucination evidence currently comes from English-language evaluation.
Because such models are widely used by Hindi and other Indian-language
speakers, it matters empirically whether hallucination behaviour changes when
the *same question* is asked in Hindi instead of English. Understanding any
such language-dependent difference has implications for evaluation practice
and for the safe deployment of language assistants in India.

## Research Objectives

1. **Estimate** hallucination frequency for each language (English, Hindi) on
   matched question pairs, per model.
2. **Compare** hallucination rates between English and Hindi statistically,
   treating the underlying question as a paired (within-item) factor.
3. **Examine** whether any language effect differs across the planned task
   categories (factual, numerical, reasoning, cultural/contextual).
4. **Compare** several LLMs (3–4; list pending) to see whether any language
   effect is consistent across models.
5. **Characterise** (qualitatively, through error analysis) any differences in
   the type or form of hallucinations between languages.

## Preliminary Research Questions

- **RQ1** — Does hallucination frequency differ between English and Hindi for
  the same underlying question?
- **RQ2** — Does any English–Hindi difference vary by task category?
- **RQ3** — Are any language differences consistent across the models studied?
- **RQ4** — Do hallucination characteristics (partial vs. wholesale
  fabrication, refusal behaviour) differ between languages?
- **RQ5** — Which plausible sources (translation fidelity, tokenization,
  model-specific training data) could explain any observed differences?
  *(Exploratory; only pursued if the data support it.)*

## Experimental Design

| Component | Planned design |
|---|---|
| Languages | English and Hindi only (at this stage). |
| Questions | ~250 paired underlying questions → ~500 prompts (one English + one Hindi prompt per question). The **underlying question is held constant** across languages; only the surface language differs. |
| Categories | Factual · Numerical · Reasoning · Cultural/Contextual (names preliminary). |
| Models | 3–4 LLMs. Exact models and versions are pending and are deliberately not hard-coded. |
| Evaluation | Human annotation of each model response against a reliable reference answer/source, using a preliminary label scheme (see `annotations/annotation_guidelines.md`). |
| Analysis | Quantitative comparison (hallucination rates by language, category, and model) and statistical testing (paired within-question design; exact tests TBD). |

## Methodology Overview

The planned pipeline is:

```
curate ~250 paired EN–HI questions (with reference answers)
  → generate standardized, neutral prompts (EN and HI)
  → query 3–4 LLMs
  → collect raw responses (unmodified)
  → human annotation (preliminary label scheme, adjudication)
  → compute hallucination rates and statistical comparisons
  → error analysis and reporting
```

Nothing in this pipeline has been executed yet.

## Repository Structure

```
comparative-llm-hallucination-indian-languages/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── data/
│   ├── raw/                  # future source material
│   ├── processed/            # future paired question set
│   └── README.md
├── experiments/
│   ├── __init__.py
│   ├── config.py             # config (languages, categories, paths)
│   ├── prompts.py            # neutral EN/HI prompt templates
│   ├── model_runner.py       # safe skeleton interface (no API calls)
│   └── run_experiment.py     # placeholder pipeline (does not run)
├── responses/
│   ├── raw_responses/        # future raw model outputs
│   └── README.md
├── annotations/
│   ├── annotation_guidelines.md
│   ├── annotator_1/          # future annotation files
│   ├── annotator_2/          # future annotation files
│   └── final_labels/         # future adjudicated labels
├── analysis/
│   ├── __init__.py
│   ├── hallucination_rates.py
│   ├── statistical_tests.py
│   └── error_analysis.py
├── results/
│   ├── tables/
│   └── figures/
├── literature/
│   ├── README.md
│   └── literature_matrix.csv
├── paper/
│   ├── ieee/
│   └── references.bib
└── notebooks/
    └── exploratory_analysis.ipynb
```

## Current Project Status

**Completed so far (Day 1 — repository setup only):**

- [x] Repository scaffold and configuration (`README.md`, `requirements.txt`,
      `.gitignore`, `.env.example`).
- [x] Configuration placeholders (`experiments/config.py`).
- [x] Neutral, standardized prompt templates (`experiments/prompts.py`).
- [x] Safe model-runner interface that makes **no API calls**
      (`experiments/model_runner.py`).
- [x] Placeholder experiment pipeline (`experiments/run_experiment.py`).
- [x] Placeholder analysis modules (`analysis/`).
- [x] Preliminary annotation guidelines (`annotations/annotation_guidelines.md`).
- [x] Placeholder data and literature structures.

**Pending (deliberately NOT part of Day 1):**

- [ ] Finalize the paired question set (~250 pairs, with reference answers).
- [ ] Finalize the model list (3–4 models + versions + API configuration).
- [ ] Implement API calls in the model runner (with retries, rate limiting,
      logging).
- [ ] Run the experiment and collect responses.
- [ ] Finalize the annotation scheme and run annotation.
- [ ] Analysis, statistical tests, and reporting.

## Related Work

Existing work on hallucination in Indian languages includes **BHRAM-IL**, an
existing large-scale benchmark for hallucination in Indian languages. This
study plans to discuss BHRAM-IL as related work; a **verified citation will be
added** to `paper/references.bib` after the literature review is completed
(see `literature/literature_matrix.csv`). No specific claims about BHRAM-IL's
results are made in this document.

## Preliminary Distinction from BHRAM-IL

This study is **not** a replication, extension, or copy of BHRAM-IL's benchmark
design. The intended distinctions are:

- **Scope of design.** BHRAM-IL is a large multilingual hallucination
  benchmark; this study is a controlled empirical comparison of **English vs.
  Hindi only**.
- **Question pairing.** We use paired questions where the *underlying question
  is held constant* across languages, enabling a matched, within-question
  comparison.
- **Research question.** We ask specifically *whether language affects
  hallucination frequency and characteristics* on matched items, rather than
  attempting another large-scale multilingual benchmark or leaderboard.
- **Scale.** We are explicitly **not** creating a large-scale multilingual
  benchmark; the emphasis is on depth (careful annotation, controlled
  comparison) over scale on a smaller curated set.

## Setup

Create a virtual environment and install dependencies (Python **3.12**):

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in credentials **only if/when** they are
needed for the finalized API configuration. Never commit `.env`.

## Authors

- **[Researcher 1 Name]** — *[Affiliation / email placeholder]*
- **[Researcher 2 Name]** — *[Affiliation / email placeholder]*

*(Placeholders — to be completed by the study authors.)*

## References

- `paper/references.bib` — intentionally empty until the literature review is
  complete, so that no unverified citations are introduced.