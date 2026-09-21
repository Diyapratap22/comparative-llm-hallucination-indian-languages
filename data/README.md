# Data

Planned organization of the future question dataset and derived files.
**No data files exist yet** — nothing is fabricated and nothing has been
downloaded or generated.

## Directory layout

| Directory | Purpose | Status |
|---|---|---|
| `raw/` | Source material (e.g. reference documents, notes behind questions) | empty |
| `processed/` | Cleaned, paired question set used by the experiment | empty |

## Planned question dataset schema (`data/processed/questions.csv`)

The future question dataset is planned to contain one row per paired question
with at least the following columns:

| Column | Description |
|---|---|
| `question_id` | Unique identifier, e.g. `Q001`. |
| `category` | Planned task category: `factual`, `numerical`, `reasoning`, `cultural_contextual`. Category names are preliminary. |
| `subcategory` | Finer-grained label within a category (to be defined). |
| `english_question` | Question text in English. |
| `hindi_question` | Matched question text in Hindi — the **same underlying question**. |
| `expected_answer` | Reference answer derived from a reliable source (used in annotation). |
| `source` | Provenance of the question and/or the reference answer. |
| `difficulty` | Planned difficulty label (definition to be finalized). |

## Rules

- No fabricated questions or answers.
- Each underlying question appears exactly twice in the final prompt set:
  once in English and once in Hindi (≈250 questions → ≈500 prompts).
- Reference answers must be reliable and verifiable before annotation starts.