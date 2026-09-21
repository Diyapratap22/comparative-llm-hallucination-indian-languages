"""Error analysis utilities (placeholders).

Planned purpose: qualitative and descriptive analysis of hallucination
patterns — where they occur (category, language, model) and in what form
(e.g. wholesale fabrication vs. unsupported additions to an otherwise
correct answer).

No analysis is performed and no output is produced until the annotated data
exist.
"""

from __future__ import annotations

import pandas as pd


def error_distribution_by_category(
    annotations: pd.DataFrame, label_column: str = "label"
) -> pd.DataFrame:
    """Cross-tabulate hallucination events by task category (placeholder).

    Parameters
    ----------
    annotations:
        Long-format annotated dataset with a ``category`` column.
    label_column:
        Name of the column holding the annotation labels.

    Returns
    -------
    pd.DataFrame
        Counts / proportions per category.

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )


def error_distribution_by_language(
    annotations: pd.DataFrame, label_column: str = "label"
) -> pd.DataFrame:
    """Cross-tabulate hallucination events by language (placeholder).

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )


def qualitative_error_summary(
    annotations: pd.DataFrame, label_column: str = "label"
) -> pd.DataFrame:
    """Summarize hallucination characteristics for qualitative review.

    Planned: a per-response table of error types/notes to be reviewed by the
    researchers (category, language, model, response, reference, note).

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )


def extract_representative_examples(
    annotations: pd.DataFrame,
    n_per_group: int = 10,
    label_column: str = "label",
) -> pd.DataFrame:
    """Select representative example responses for the paper/report.

    Parameters
    ----------
    annotations:
        Long-format annotated dataset.
    n_per_group:
        Number of examples to select per group (e.g. per language).
    label_column:
        Name of the column holding the annotation labels.

    Returns
    -------
    pd.DataFrame
        A curated example table.

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )