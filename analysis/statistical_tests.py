"""Statistical tests for the hallucination comparison (placeholders).

Planned analysis strategy (preliminary, to be confirmed)

- Language comparison: paired, within-question comparison of English vs.
  Hindi for the same ``question_id`` — e.g. a McNemar-type test for paired
  binary outcomes or a permutation test on per-question differences.
- Category and model comparisons follow the same per-question paired design.

No test is implemented and no output is produced until the experiment has
produced annotated data.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


def test_language_difference(
    annotations: pd.DataFrame, label_column: str = "label"
) -> Any:
    """Test whether hallucination rates differ between English and Hindi.

    Intended design: a paired comparison on matched (``question_id``) items,
    so that language is a within-question factor.

    Parameters
    ----------
    annotations:
        Long-format annotated dataset with at least ``question_id``,
        ``language``, and ``label_column``.
    label_column:
        Name of the column holding the annotation labels.

    Returns
    -------
    Any
        Test result object (exact type TBD).

    Raises
    ------
    NotImplementedError
        Until the tests are implemented.
    """
    raise NotImplementedError("Statistical tests are not implemented yet.")


def test_category_differences(
    annotations: pd.DataFrame, label_column: str = "label"
) -> Any:
    """Compare hallucination rates across task categories (placeholder).

    Raises
    ------
    NotImplementedError
        Until the tests are implemented.
    """
    raise NotImplementedError("Statistical tests are not implemented yet.")


def test_model_effects(
    annotations: pd.DataFrame, label_column: str = "label"
) -> Any:
    """Compare models, with language as a within-model factor (placeholder).

    Raises
    ------
    NotImplementedError
        Until the tests are implemented.
    """
    raise NotImplementedError("Statistical tests are not implemented yet.")


def compute_effect_size(
    group_rates: dict[str, float],
) -> float:
    """Compute an effect size between two groups (exact measure TBD).

    Parameters
    ----------
    group_rates:
        Mapping of group name to hallucination rate, e.g.
        ``{"en": ..., "hi": ...}``.

    Returns
    -------
    float
        Effect size estimate.

    Raises
    ------
    NotImplementedError
        Until effect size conventions are finalized and implemented.
    """
    raise NotImplementedError("Effect-size computation is not implemented yet.")