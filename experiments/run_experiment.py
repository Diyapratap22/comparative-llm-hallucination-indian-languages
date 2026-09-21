"""Experiment pipeline (placeholder — executes nothing).

Intended flow (shows the architecture; steps will be implemented later):

    load questions
        -> generate standardized prompts (EN + HI)
        -> send prompts to selected models
        -> save raw responses
        -> log metadata

``EXPERIMENT_ENABLED`` is ``False`` until the question set, the model list,
the API configuration, and the pipeline implementation are all finalized.

Run from the repository root as a module:

    python -m experiments.run_experiment
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from experiments.config import DATA_PROCESSED_DIR, RAW_RESPONSES_DIR

# The pipeline refuses to run while this is False.
EXPERIMENT_ENABLED: bool = False

# Default locations (overridable per run).
DEFAULT_QUESTION_SET: Path = DATA_PROCESSED_DIR / "questions.csv"
DEFAULT_OUTPUT_DIR: Path = RAW_RESPONSES_DIR


def load_questions(path: Path | None = None) -> list[dict[str, Any]]:
    """TODO: load the paired EN–HI question set from ``data/processed``.

    Expected columns are described in ``data/README.md``
    (question_id, category, english_question, hindi_question, ...).

    Raises
    ------
    NotImplementedError
        Until question loading is implemented.
    """
    raise NotImplementedError("load_questions is not implemented yet.")


def generate_prompts(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """TODO: build EN and HI prompts with ``experiments.prompts.build_prompt``.

    Returns one record per (question_id, language), containing the prompt
    text, the system prompt, and the metadata needed downstream.

    Raises
    ------
    NotImplementedError
        Until prompt generation is implemented.
    """
    raise NotImplementedError("generate_prompts is not implemented yet.")


def query_models(prompt_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """TODO: instantiate runners from ``MODEL_IDS`` and collect responses.

    Must record the raw output plus metadata (model, version, timestamp,
    decoding settings) for every prompt. Must not modify the model output.

    Raises
    ------
    NotImplementedError
        Until model querying is implemented.
    """
    raise NotImplementedError("query_models is not implemented yet.")


def save_raw_responses(
    response_records: list[dict[str, Any]],
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> None:
    """TODO: persist raw responses and metadata under ``responses/raw_responses``.

    Raises
    ------
    NotImplementedError
        Until response saving is implemented.
    """
    raise NotImplementedError("save_raw_responses is not implemented yet.")


def log_metadata(
    metadata: dict[str, Any],
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> None:
    """TODO: write a run manifest (config snapshot, timestamps, hashes).

    Raises
    ------
    NotImplementedError
        Until metadata logging is implemented.
    """
    raise NotImplementedError("log_metadata is not implemented yet.")


def main() -> None:
    """Run the pipeline if enabled; otherwise do nothing."""
    if not EXPERIMENT_ENABLED:
        print(
            "[run_experiment] Pipeline disabled (EXPERIMENT_ENABLED = False). "
            "Nothing was executed."
        )
        return

    # The steps below are placeholders and are unreachable until the
    # functions above are implemented and EXPERIMENT_ENABLED is set to True.
    questions = load_questions()  # noqa: F841
    prompt_records = generate_prompts(questions)
    response_records = query_models(prompt_records)
    save_raw_responses(response_records)
    log_metadata({"experiment_id": "<TBD>"})


if __name__ == "__main__":
    main()