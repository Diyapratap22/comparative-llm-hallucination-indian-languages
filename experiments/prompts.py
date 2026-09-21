"""Prompt templates for the English–Hindi paired-question study.

Design notes
------------
- The templates are deliberately **neutral**: they contain no instruction that
  encourages or discourages hallucination (no "be factual", no "say you don't
  know"). The goal is to observe the model's default behaviour.
- The system prompt uses identical wording for both languages so that the
  instruction content is held constant; only the question and the "Answer:"
  marker differ by language. This is a preliminary decision and is easy to
  change (edit the template constants below).
- Category-specific stimulus phrasing (factual, numerical, reasoning,
  cultural/contextual) will be added here later if the study design requires
  it. No such phrasings exist yet.
"""

from __future__ import annotations

from typing import Literal

Language = Literal["en", "hi"]

# System message: identical for both languages so the instruction is constant.
SYSTEM_PROMPT: str = (
    "You are an AI assistant taking part in a research study. "
    "Respond to the question you are asked."
)

# User-message templates (one per language).
EN_QUESTION_TEMPLATE: str = "Question:\n{question}\n\nAnswer:"
HI_QUESTION_TEMPLATE: str = "प्रश्न:\n{question}\n\nउत्तर:"

TEMPLATES: dict[Language, str] = {
    "en": EN_QUESTION_TEMPLATE,
    "hi": HI_QUESTION_TEMPLATE,
}


def build_system_prompt() -> str:
    """Return the neutral system prompt used for all models and languages."""
    return SYSTEM_PROMPT


def build_prompt(question: str, language: Language) -> str:
    """Return the formatted user prompt for ``question`` in ``language``.

    Parameters
    ----------
    question:
        Question text in the target language (already paired / translated).
    language:
        One of the supported languages: ``"en"`` or ``"hi"``.

    Returns
    -------
    str
        The final user prompt sent to the model for this item.

    Raises
    ------
    ValueError
        If ``language`` is not supported.
    """
    try:
        template = TEMPLATES[language]
    except KeyError as exc:
        raise ValueError(f"Unsupported language: {language!r}") from exc
    return template.format(question=question)