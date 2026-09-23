"""Experiment configuration for the English-Hindi hallucination study.

All experiment-level settings live here so that the pipeline (prompts,
model runner, and analysis) reads from a single source of truth.

API keys are never stored in this file. They are loaded from the local
.env file by the model runner.
"""

from __future__ import annotations

from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

DATA_RAW_DIR: Path = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR: Path = PROJECT_ROOT / "data" / "processed"

RAW_RESPONSES_DIR: Path = (
    PROJECT_ROOT / "responses" / "raw_responses"
)

RESULTS_TABLES_DIR: Path = (
    PROJECT_ROOT / "results" / "tables"
)

RESULTS_FIGURES_DIR: Path = (
    PROJECT_ROOT / "results" / "figures"
)

FINAL_LABELS_DIR: Path = (
    PROJECT_ROOT / "annotations" / "final_labels"
)


OUTPUT_DIRECTORIES: tuple[Path, ...] = (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    RAW_RESPONSES_DIR,
    RESULTS_TABLES_DIR,
    RESULTS_FIGURES_DIR,
    FINAL_LABELS_DIR,
)


def ensure_output_directories() -> None:
    """Create all experiment output directories."""

    for directory in OUTPUT_DIRECTORIES:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================================
# LANGUAGES
# ============================================================================

SUPPORTED_LANGUAGES: list[str] = [
    "en",
    "hi",
]

LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "hi": "Hindi",
}


# ============================================================================
# TASK CATEGORIES
# ============================================================================

TASK_CATEGORIES: list[str] = [
    "factual",
    "numerical",
    "reasoning",
    "cultural_contextual",
]


# ============================================================================
# DATASET SIZE
# ============================================================================

# Final number of paired underlying questions.
PLANNED_NUM_QUESTIONS: int = 200

# Each underlying question has:
#   1 English version
#   1 Hindi version
PLANNED_NUM_PROMPTS: int = 400

# Final curated question count.
NUM_CURATED_QUESTIONS: int = 200


# ============================================================================
# MODELS
# ============================================================================

# Exact model/provider configuration used by the experiment.
#
# API keys are NOT stored here.
# They are loaded from .env:
#
#   GEMINI_API_KEY
#   GROQ_API_KEY
#   COHERE_API_KEY

MODELS: list[dict[str, str]] = [
    {
        "name": "Gemini 3.6 Flash",
        "provider": "gemini",
        "model_id": "gemini-3.6-flash",
    },
    {
        "name": "GPT-OSS 120B",
        "provider": "groq",
        "model_id": "openai/gpt-oss-120b",
    },
    {
        "name": "Command A",
        "provider": "cohere",
        "model_id": "command-a-03-2025",
    },
    {
        "name": "Qwen 3.8 27B",
        "provider": "groq",
        "model_id": "qwen/qwen3.8-27b",
    },
]


# ---------------------------------------------------------------------------
# Compatibility list
# ---------------------------------------------------------------------------
# The pipeline uses this list to iterate through the selected models.
# Keep this automatically derived from MODELS so that the two lists
# cannot accidentally become inconsistent.

MODEL_IDS: list[str] = [
    model["model_id"]
    for model in MODELS
]


# ============================================================================
# GENERATION SETTINGS
# ============================================================================

# Deterministic generation for the controlled experiment.
TEMPERATURE: float = 0.0

# Maximum generated tokens per response.
MAX_OUTPUT_TOKENS: int = 256

# Each question-language pair is run once per model.
NUM_RUNS: int = 1

# External tools are disabled.
USE_TOOLS: bool = False

# Web search/retrieval is disabled.
USE_WEB_SEARCH: bool = False


# ============================================================================
# PILOT EXPERIMENT
# ============================================================================

# Number of paired questions used for pipeline validation.
PILOT_NUM_QUESTIONS: int = 10


# ============================================================================
# EXPERIMENT METADATA
# ============================================================================

EXPERIMENT_ID: str = "en_hi_hallucination_v0"

EXPERIMENT_VERSION: str = "0.2.0"

CREATED_ON: str = "2026-09-21"

# Current development stage.
#
# This is still the pilot stage. Do not mark the experiment as
# "full-data-collected" until the complete experiment has actually run.
STATUS: str = "pilot-ready"