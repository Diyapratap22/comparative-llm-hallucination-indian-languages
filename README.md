# A Comparative Evaluation of Hallucination in Large Language Models for English and Indian Languages

> An empirical study of hallucination in Large Language Models through a controlled English–Hindi comparison across factual, numerical, reasoning, and cultural/contextual tasks.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat)
![NLP](https://img.shields.io/badge/NLP-3776AB?style=flat)
![LLM Evaluation](https://img.shields.io/badge/LLM%20Evaluation-4B0082?style=flat)
![Multilingual AI](https://img.shields.io/badge/Multilingual%20AI-008080?style=flat)
![Research](https://img.shields.io/badge/Research-555555?style=flat)

## Overview

This project investigates hallucination in large language models (LLMs) through a controlled empirical comparison between **English** and **Hindi**. The same underlying question is presented in both languages, so that language is the primary factor being compared while the question content is held constant.

The study evaluates model responses across four planned task categories — factual, numerical, reasoning, and cultural/contextual tasks — using human annotation and quantitative/statistical analysis.

This is an **empirical comparative study**, not a generic multilingual benchmark. The focus is on whether, and how, hallucination behaviour differs when the same question is asked in English versus Hindi.

## Motivation

Hallucination — the generation of fluent but incorrect or unsupported content — is most commonly evaluated in English. LLMs are increasingly used by Hindi and other Indian-language speakers in substantial numbers, yet evidence about hallucination behaviour in these languages remains comparatively limited.

It is an open question whether models hallucinate at the same rate, in the same places, or in the same forms when the identical underlying question is posed in Hindi instead of English. Understanding such language-dependent behaviour matters both for evaluation practice and for the reliable deployment of language assistants in Indian-language contexts.

## Research Objectives

1. **Estimate** hallucination frequency for English and Hindi on matched question pairs, for each model.
2. **Compare** hallucination rates between English and Hindi statistically, treating the underlying question as a paired (within-item) factor.
3. **Examine** whether any language-dependent difference varies across the planned task categories (factual, numerical, reasoning, cultural/contextual).
4. **Compare** several LLMs (3–4) to assess whether any language effect is consistent across models.
5. **Characterise** the type and form of hallucinations in each language through qualitative error analysis.

## Research Questions

- **RQ1.** Does hallucination frequency differ between English and Hindi for the same underlying question?
- **RQ2.** Does any English–Hindi difference vary across task categories?
- **RQ3.** Are any language differences consistent across the models studied?
- **RQ4.** Do hallucination characteristics — for example, partial versus wholesale fabrication, or refusal behaviour — differ between languages?
- **RQ5.** *(Exploratory)* Can plausible language-related factors help interpret any observed differences, such as translation fidelity, tokenization, or training-data coverage?

RQ5 is exploratory and is not intended to establish causal explanations; it will only be pursued if the data support it.

## Experimental Design

The following design is **planned/proposed** and is subject to revision as the study progresses.

| Component | Planned design |
|---|---|
| **Languages** | English and Hindi. |
| **Question set** | Approximately 250 paired underlying questions, resulting in approximately 500 language-specific prompts (one English and one Hindi prompt per question). |
| **Task categories** | Factual · Numerical · Reasoning · Cultural/Contextual. |
| **Models** | 3–4 LLMs; exact models and versions will be finalized before experimentation. |
| **Evaluation** | Human annotation of model responses against reliable reference answers/sources. |
| **Analysis** | Hallucination rates, language/category/model comparisons, statistical testing, and qualitative error analysis. |

The central design choice is the pairing of questions: the underlying question is held constant across languages, so that any observed differences can be attributed to language rather than to question content.

## Methodology

The planned pipeline is:

```
Question Curation
→ English–Hindi Pairing
→ Standardized Prompting
→ LLM Response Collection
→ Human Annotation
→ Hallucination Classification
→ Statistical Analysis
→ Error Analysis
```

A curated set of approximately 250 questions will be paired into English–Hindi equivalents that preserve the same underlying meaning. Each question will be accompanied by a reliable reference answer or source to support annotation.

Prompts will be constructed from standardized, neutral templates so that no instruction encourages or discourages hallucination. The same prompt structure and instruction will be used for both languages. Responses will be collected from 3–4 LLMs and stored unmodified for downstream analysis.

Human annotators will classify each response using the preliminary label scheme described below, and adjudication will resolve disagreements. The resulting labels will support hallucination-rate estimation, statistical comparisons across languages, categories, and models, and qualitative error analysis.

## Evaluation Framework

The annotation framework is preliminary and will be finalized before the main annotation stage. The current label scheme consists of:

- **Correct** — the response answers the question and is consistent with the reference answer/source.
- **Partially Correct** — some relevant part is correct, but the response contains omissions, unsupported additions, or inaccuracies.
- **Hallucinated** — content not supported by (or contradicting) the reference answer/source, presented with unjustified confidence.
- **Refusal / No Answer** — the model declines to answer or provides no substantive answer.
- **Unclear / Requires Adjudication** — the appropriate label is ambiguous and requires joint review.

Final label definitions, boundary rules, and the adjudication protocol will be documented in `annotations/annotation_guidelines.md` before annotation begins.

## Related Work

Existing research on hallucination evaluation in Indian languages includes **BHRAM-IL**, a large multilingual benchmark for hallucination in Indian languages. This study discusses such work as related context while maintaining a different experimental design.

A verified citation for BHRAM-IL will be maintained in `paper/references.bib` as the literature review is finalized. No specific statistics or findings about BHRAM-IL are reported here.

## How This Study Differs from BHRAM-IL

| Aspect | This Study | BHRAM-IL |
|---|---|---|
| **Primary scope** | Controlled English–Hindi hallucination comparison | Large multilingual hallucination benchmark |
| **Languages** | English and Hindi | Multilingual, with a focus on Indian languages |
| **Question design** | Paired questions; the same underlying question in both languages | Benchmark-scale multilingual question sets |
| **Research objective** | Whether language affects hallucination frequency and characteristics | Broad hallucination evaluation across languages |
| **Scale/emphasis** | Smaller, curated, carefully annotated comparative design | Large-scale benchmark design |

The characterisation of BHRAM-IL above is limited to its description as a large multilingual hallucination benchmark for Indian languages. A verified citation will be maintained in `paper/references.bib`.

## Repository Structure

```
comparative-llm-hallucination-indian-languages/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── experiments/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   ├── model_runner.py
│   └── run_experiment.py
├── responses/
│   ├── raw_responses/
│   └── README.md
├── annotations/
│   ├── annotation_guidelines.md
│   ├── annotator_1/
│   ├── annotator_2/
│   └── final_labels/
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

## Reproducibility and Setup

The project targets **Python 3.12**.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment (Windows):

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

API credentials, when eventually required, belong in a local `.env` file (copy `.env.example` and fill it in). The `.env` file is ignored by git and must never be committed.

## Project Status

Research in progress. The repository currently contains the experimental architecture and supporting research infrastructure; model selection, question construction, response collection, annotation, and statistical analysis will be completed as part of the study.

## Authors

**Diya Pratap**

B.Tech. Artificial Intelligence & Machine Learning
Dr. Akhilesh Das Gupta Institute of Professional Studies, GGSIPU, New Delhi
GitHub: [Diyapratap22](https://github.com/Diyapratap22)

**Kinjal Sidharth**

B.Tech. Artificial Intelligence & Machine Learning
Dr. Akhilesh Das Gupta Institute of Professional Studies, GGSIPU, New Delhi
GitHub: [Kinjal7127](https://github.com/Kinjal7127)

## References

Verified references will be added to `paper/references.bib` as the literature review is finalized. No unverified citations are included in this repository.