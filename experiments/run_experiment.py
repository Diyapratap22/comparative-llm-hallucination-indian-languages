"""Main experiment pipeline for the English-Hindi hallucination study.

Pipeline:

    question_bank.xlsx
        -> load questions
        -> generate English + Hindi prompts
        -> run each prompt through each configured model
        -> collect responses + metadata
        -> save consolidated Excel output

Run from repository root:

    python -m experiments.run_experiment

The pipeline runs in PILOT mode by default.
Set RUN_FULL_EXPERIMENT = True only after the pilot succeeds.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from experiments.config import (
    MODEL_IDS,
    NUM_RUNS,
    PILOT_NUM_QUESTIONS,
    PLANNED_NUM_QUESTIONS,
    RAW_RESPONSES_DIR,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    ensure_output_directories,
)

from experiments.model_runner import create_runner
from experiments.prompts import (
    build_prompt,
    build_system_prompt,
)


# ============================================================================
# RUN CONTROL
# ============================================================================

# IMPORTANT:
# Keep False for the 10-question pilot.
# Change to True only after the pilot is verified.
RUN_FULL_EXPERIMENT: bool = True


# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

QUESTION_BANK_PATH: Path = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "question_bank.xlsx"
)

OUTPUT_FILE: Path = (
    RAW_RESPONSES_DIR
    / "experiment_responses.xlsx"
)


# ============================================================================
# MODEL -> PROVIDER MAPPING
# ============================================================================

MODEL_PROVIDERS: dict[str, str] = {
    "gemini-3.5-flash-lite": "gemini",
    "openai/gpt-oss-120b": "groq",
    "command-a-03-2025": "cohere",
    "qwen/qwen3.8-27b": "groq",
}


MODEL_NAMES: dict[str, str] = {
    "gemini-3.5-flash-lite": "Gemini 3.5 Flash-Lite",
    "openai/gpt-oss-120b": "GPT-OSS 120B",
    "command-a-03-2025": "Cohere Command A",
    "qwen/qwen3.8-27b": "Qwen 3.8 27B",
}


# ============================================================================
# QUESTION BANK
# ============================================================================

def load_questions(
    path: Path = QUESTION_BANK_PATH,
) -> list[dict[str, Any]]:
    """Load the paired English-Hindi question bank from Excel."""

    if not path.exists():
        raise FileNotFoundError(
            f"Question bank not found:\n{path}"
        )

    df = pd.read_excel(path)

    # Expected columns from Person 1's deliverable.
    required_columns = {
        "Question ID",
        "Category",
        "English Question",
        "Hindi Question",
        "Expected Answer",
        "Source",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "The question bank is missing these required columns:\n"
            + "\n".join(sorted(missing_columns))
        )

    questions: list[dict[str, Any]] = []

    for _, row in df.iterrows():

        # Ignore completely empty rows.
        if pd.isna(row["Question ID"]):
            continue

        questions.append(
            {
                "question_id": str(row["Question ID"]).strip(),
                "category": str(row["Category"]).strip(),
                "english_question": str(
                    row["English Question"]
                ).strip(),
                "hindi_question": str(
                    row["Hindi Question"]
                ).strip(),
                "expected_answer": str(
                    row["Expected Answer"]
                ).strip(),
                "source": str(row["Source"]).strip(),
            }
        )

    if not questions:
        raise ValueError(
            "No valid questions were found in the question bank."
        )

    return questions


# ============================================================================
# PROMPT GENERATION
# ============================================================================

def generate_prompt_records(
    questions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Generate one English and one Hindi prompt for every question."""

    system_prompt = build_system_prompt()

    prompt_records: list[dict[str, Any]] = []

    for question in questions:

        language_questions = [
            (
                "en",
                question["english_question"],
            ),
            (
                "hi",
                question["hindi_question"],
            ),
        ]

        for language, question_text in language_questions:

            prompt = build_prompt(
                question=question_text,
                language=language,
            )

            prompt_records.append(
                {
                    "question_id": question["question_id"],
                    "category": question["category"],
                    "language": language,
                    "question": question_text,
                    "expected_answer": question["expected_answer"],
                    "source": question["source"],
                    "system_prompt": system_prompt,
                    "user_prompt": prompt,
                }
            )

    return prompt_records


# ============================================================================
# MODEL HELPERS
# ============================================================================

def get_provider(model_id: str) -> str:
    """Return the provider associated with a model."""

    if model_id not in MODEL_PROVIDERS:
        raise ValueError(
            f"No provider mapping exists for model: {model_id}"
        )

    return MODEL_PROVIDERS[model_id]


def get_model_name(model_id: str) -> str:
    """Return human-readable model name."""

    return MODEL_NAMES.get(
        model_id,
        model_id,
    )


# ============================================================================
# MODEL EXECUTION
# ============================================================================

def query_models(
    prompt_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Run every prompt through every configured model."""

    results: list[dict[str, Any]] = []

    # ------------------------------------------------------------------------
    # Initialize model clients once.
    # ------------------------------------------------------------------------

    runners: dict[str, Any] = {}

    print("\nInitializing models...")
    print("-" * 60)

    for model_id in MODEL_IDS:

        provider = get_provider(model_id)

        print(
            f"Initializing: {get_model_name(model_id)} "
            f"({provider})"
        )

        runners[model_id] = create_runner(
            provider=provider,
            model_id=model_id,
        )

    print("-" * 60)

    total_requests = (
        len(prompt_records)
        * len(MODEL_IDS)
        * NUM_RUNS
    )

    completed_requests = 0

    print(
        f"\nTotal API requests planned: {total_requests}\n"
    )

    # ------------------------------------------------------------------------
    # Execute experiment.
    # ------------------------------------------------------------------------

    for record in prompt_records:

        for model_id in MODEL_IDS:

            runner = runners[model_id]

            for run_number in range(1, NUM_RUNS + 1):

                completed_requests += 1

                print(
                    f"[{completed_requests}/{total_requests}] "
                    f"{get_model_name(model_id)} | "
                    f"{record['question_id']} | "
                    f"{record['language']}"
                )

                started_at = datetime.now(timezone.utc)
                start_time = time.perf_counter()

                response_text = ""
                status = "success"
                error_message = ""

                try:

                    response_text = runner.generate(
                        prompt=record["user_prompt"],
                        language=record["language"],
                        system_prompt=record["system_prompt"],
                    )

                except Exception as exc:

                    status = "error"
                    error_message = str(exc)

                    print(
                        f"    ERROR: {error_message}"
                    )

                finished_at = datetime.now(timezone.utc)

                latency_seconds = (
                    time.perf_counter()
                    - start_time
                )

                # ------------------------------------------------------------
                # Store complete metadata.
                # ------------------------------------------------------------

                results.append(
                    {
                        "question_id": record["question_id"],
                        "category": record["category"],
                        "language": record["language"],
                        "question": record["question"],
                        "expected_answer": record[
                            "expected_answer"
                        ],
                        "source": record["source"],
                        "model": get_model_name(model_id),
                        "model_id": model_id,
                        "provider": get_provider(model_id),
                        "run_number": run_number,
                        "temperature": TEMPERATURE,
                        "max_output_tokens": MAX_OUTPUT_TOKENS,
                        "system_prompt": record[
                            "system_prompt"
                        ],
                        "user_prompt": record[
                            "user_prompt"
                        ],
                        "response": response_text,
                        "status": status,
                        "error": error_message,
                        "started_at_utc": started_at.isoformat(),
                        "finished_at_utc": finished_at.isoformat(),
                        "latency_seconds": round(
                            latency_seconds,
                            3,
                        ),
                    }
                )

    return results


# ============================================================================
# SAVE RESULTS
# ============================================================================

def save_results(
    results: list[dict[str, Any]],
    output_path: Path = OUTPUT_FILE,
) -> None:
    """Save experiment results into one Excel workbook."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.DataFrame(results)

    df.to_excel(
        output_path,
        index=False,
        engine="openpyxl",
    )

    print("\n" + "=" * 60)
    print("EXPERIMENT FINISHED")
    print("=" * 60)

    print(
        f"Results saved to:\n{output_path}"
    )

    print(
        f"\nRows written: {len(df)}"
    )

    successful = (
        (df["status"] == "success").sum()
        if not df.empty
        else 0
    )

    failed = (
        (df["status"] == "error").sum()
        if not df.empty
        else 0
    )

    print(f"Successful responses: {successful}")
    print(f"Failed responses: {failed}")

    print("=" * 60)


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """Run the experiment pipeline."""

    ensure_output_directories()

    print("=" * 60)
    print("ENGLISH-HINDI LLM HALLUCINATION STUDY")
    print("=" * 60)

    # ------------------------------------------------------------------------
    # Load question bank
    # ------------------------------------------------------------------------

    print(
        f"\nLoading question bank:\n"
        f"{QUESTION_BANK_PATH}"
    )

    questions = load_questions()

    print(
        f"Questions loaded: {len(questions)}"
    )

    # ------------------------------------------------------------------------
    # Select pilot/full dataset
    # ------------------------------------------------------------------------

    if RUN_FULL_EXPERIMENT:

        selected_questions = questions[
            :PLANNED_NUM_QUESTIONS
        ]

        print(
            f"\nMODE: FULL EXPERIMENT"
        )

    else:

        selected_questions = questions[
            :PILOT_NUM_QUESTIONS
        ]

        print(
            f"\nMODE: PILOT"
        )

    print(
        f"Questions selected: "
        f"{len(selected_questions)}"
    )

    # ------------------------------------------------------------------------
    # Generate prompts
    # ------------------------------------------------------------------------

    prompt_records = generate_prompt_records(
        selected_questions
    )

    print(
        f"Prompts generated: "
        f"{len(prompt_records)}"
    )

    # ------------------------------------------------------------------------
    # Calculate API calls
    # ------------------------------------------------------------------------

    total_requests = (
        len(prompt_records)
        * len(MODEL_IDS)
        * NUM_RUNS
    )

    print(
        f"Models: {len(MODEL_IDS)}"
    )

    print(
        f"API requests expected: "
        f"{total_requests}"
    )

    # ------------------------------------------------------------------------
    # Run models
    # ------------------------------------------------------------------------

    results = query_models(
        prompt_records
    )

    # ------------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------------

    save_results(
        results
    )


if __name__ == "__main__":
    main()