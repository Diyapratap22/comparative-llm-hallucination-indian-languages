"""Experiment configuration for the English–Hindi hallucination study.

All experiment-level settings live here so that the pipeline (prompts,
model runner, analysis) reads from a single source of truth.

Open design decisions (e.g. the exact model list) are kept as explicit
placeholders with ``TBD`` markers. Nothing here is final.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

DATA_RAW_DIR: Path = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR: Path = PROJECT_ROOT / "data" / "processed"
RAW_RESPONSES_DIR: Path = PROJECT_ROOT / "responses" / "raw_responses"
RESULTS_TABLES_DIR: Path = PROJECT_ROOT / "results" / "tables"
RESULTS_FIGURES_DIR: Path = PROJECT_ROOT / "results" / "figures"
FINAL_LABELS_DIR: Path = PROJECT_ROOT / "annotations" / "final_labels"

# All output directories that the pipeline will write into.
OUTPUT_DIRECTORIES: tuple[Path, ...] = (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    RAW_RESPONSES_DIR,
    RESULTS_TABLES_DIR,
    RESULTS_FIGURES_DIR,
    FINAL_LABELS_DIR,
)


def ensure_output_directories() -> None:
    """Create the output directories if they do not exist yet.

    Intended to be called when the experiment actually runs. Not required
    during the setup phase.
    """
    for directory in OUTPUT_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Languages
# ---------------------------------------------------------------------------
#: Languages included in the controlled comparison. Only these two for now.
SUPPORTED_LANGUAGES: list[str] = ["en", "hi"]

#: Human-readable language names (for metadata and logging).
LANGUAGE_NAMES: dict[str, str] = {"en": "English", "hi": "Hindi"}

# ---------------------------------------------------------------------------
# Task categories (preliminary names — may be refined)
# ---------------------------------------------------------------------------
TASK_CATEGORIES: list[str] = [
    "factual",
    "numerical",
    "reasoning",
    "cultural_contextual",
]

# ---------------------------------------------------------------------------
# Dataset size (planned)
# ---------------------------------------------------------------------------
PLANNED_NUM_QUESTIONS: int = 250  # paired underlying questions
PLANNED_NUM_PROMPTS: int = 500    # ~2 prompts per question (EN + HI)

#: Current inventory. Zero until the question set is actually created.
NUM_CURATED_QUESTIONS: int = 0

# ---------------------------------------------------------------------------
# Models (placeholder — nothing finalized)
# ---------------------------------------------------------------------------
# TBD: the final list (3–4 models) will be decided in a later step, together
# with exact versions and API configuration. No model names are hard-coded.
MODEL_IDS: list[str] = []

# ---------------------------------------------------------------------------
# Experiment metadata
# ---------------------------------------------------------------------------
EXPERIMENT_ID: str = "en_hi_hallucination_v0"
EXPERIMENT_VERSION: str = "0.1.0"
CREATED_ON: str = "2026-09-21"  # Day 1 setup date
STATUS: str = "setup-only"       # no experiment has been run yet