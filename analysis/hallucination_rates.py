"""Hallucination-rate calculations (placeholders).

No results are computed in this module: the experiment has not been run and
no annotated dataset exists yet. These functions define the `intended`
interface so the analysis step can be implemented later without changing
conventions.

Data contract (planned)
-----------------------
The annotated dataset is expected to be a long-format table with at least:

    question_id, language, model, category, label

where ``label`` is one of the preliminary annotation labels described in
``annotations/annotation_guidelines.md``.
"""

from __future__ import annotations

import pandas as pd

#: Labels counted as hallucination events (preliminary scheme).
HALLUCINATED_LABELS: tuple[str, ...] = ("Hallucinated",)


def compute_hallucination_rate(labels: pd.Series) -> float:
    """Return the fraction of responses labelled as hallucinated.

    Parameters
    ----------
    labels:
        Series of annotation labels for a group of responses.

    Returns
    -------
    float
        Hallucination rate in [0.0, 1.0].

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists and aggregation is implemented.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )


def hallucination_rate_by_language(
    annotations: pd.DataFrame, label_column: str = "label"
) -> pd.Series:
    """Hallucination rate per language (preliminary grouping: en, hi).

    Parameters
    ----------
    annotations:
        Long-format annotated dataset.
    label_column:
        Name of the column holding the annotation labels.

    Returns
    -------
    pd.Series
        Hallucination rate indexed by language.

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )


def hallucination_rate_by_category(
    annotations: pd.DataFrame, label_column: str = "label"
) -> pd.Series:
    """Hallucination rate per task category (placeholder).

    Categories are defined in ``experiments.config.TASK_CATEGORIES``.

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )


def hallucination_rate_by_model(
    annotations: pd.DataFrame, label_column: str = "label"
) -> pd.Series:
    """Hallucination rate per model (placeholder).

    Raises
    ------
    NotImplementedError
        Until an annotated dataset exists.
    """
    raise NotImplementedError(
        "Requires annotated data; the experiment has not been run yet."
    )