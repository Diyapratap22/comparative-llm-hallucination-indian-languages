"""LLM model runners for the English-Hindi hallucination experiment.

This module provides a common interface for calling the selected LLMs.

Supported providers:
    - Google Gemini
    - Groq
    - Cohere

API keys are loaded from environment variables:
    GEMINI_API_KEY
    GROQ_API_KEY
    COHERE_API_KEY

No API keys are stored in source code.

Experiment-level generation settings are imported from config.py.
"""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar

from dotenv import load_dotenv

from experiments.config import (
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
)

load_dotenv()

_T = TypeVar("_T")


# ============================================================================
# Base Model Runner
# ============================================================================


class ModelRunner(ABC):
    """Common interface for all LLM providers."""

    def __init__(
        self,
        model_id: str,
        timeout_seconds: float = 60.0,
        max_retries: int = 3,
        retry_delay_seconds: float = 2.0,
    ) -> None:
        self.model_id = model_id
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

        self._client: Any = None

        self.initialize()

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the provider-specific API client."""
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        prompt: str,
        language: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a model response for a given prompt."""
        raise NotImplementedError

    def _with_retries(
        self,
        fn: Callable[[], _T],
    ) -> _T:
        """Execute an API request with exponential-backoff retries.

        The request is attempted up to ``max_retries`` times.
        The final exception is preserved and included in the error message
        so provider-specific failures are visible during pilot testing.
        """

        last_error: Exception | None = None

        for attempt in range(
            1,
            self.max_retries + 1,
        ):
            try:
                return fn()

            except Exception as exc:
                last_error = exc

                print(
                    f"    Attempt {attempt}/{self.max_retries} "
                    f"failed for {self.model_id}: {exc}"
                )

                if attempt == self.max_retries:
                    break

                delay = (
                    self.retry_delay_seconds
                    * (2 ** (attempt - 1))
                )

                print(
                    f"    Retrying in {delay:.1f} seconds..."
                )

                time.sleep(delay)

        raise RuntimeError(
            f"Model '{self.model_id}' failed after "
            f"{self.max_retries} attempts. "
            f"Last error: {last_error}"
        ) from last_error


# ============================================================================
# Gemini Runner
# ============================================================================


class GeminiRunner(ModelRunner):
    """Runner for Google Gemini models."""

    def initialize(self) -> None:
        """Initialize the Gemini API client."""

        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY was not found in the environment."
            )

        self._client = genai.Client(
            api_key=api_key,
        )

    def generate(
        self,
        prompt: str,
        language: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a response using Gemini."""

        def request() -> str:
            from google.genai import types

            config_kwargs: dict[str, Any] = {
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
            }

            if system_prompt:
                config_kwargs["system_instruction"] = system_prompt

            response = self._client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    **config_kwargs
                ),
            )

            text = getattr(
                response,
                "text",
                None,
            )

            if not text:
                raise RuntimeError(
                    f"Gemini returned an empty response for "
                    f"model '{self.model_id}'. "
                    f"Raw response: {response!r}"
                )

            return text.strip()

        return self._with_retries(request)


# ============================================================================
# Groq Runner
# ============================================================================


class GroqRunner(ModelRunner):
    """Runner for models served through Groq."""

    def initialize(self) -> None:
        """Initialize the Groq API client."""

        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY was not found in the environment."
            )

        self._client = Groq(
            api_key=api_key,
            timeout=self.timeout_seconds,
        )

    def generate(
        self,
        prompt: str,
        language: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a response using a Groq-hosted model."""

        def request() -> str:
            messages: list[dict[str, str]] = []

            if system_prompt:
                messages.append(
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            response = self._client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_OUTPUT_TOKENS,
            )

            if not response.choices:
                raise RuntimeError(
                    f"Groq returned no choices for model "
                    f"'{self.model_id}'."
                )

            text = response.choices[0].message.content

            if not text:
                raise RuntimeError(
                    f"Groq returned an empty response for model "
                    f"'{self.model_id}'."
                )

            return text.strip()

        return self._with_retries(request)


# ============================================================================
# Cohere Runner
# ============================================================================


class CohereRunner(ModelRunner):
    """Runner for Cohere chat models."""

    def initialize(self) -> None:
        """Initialize the Cohere API client."""

        import cohere

        api_key = os.getenv("COHERE_API_KEY")

        if not api_key:
            raise RuntimeError(
                "COHERE_API_KEY was not found in the environment."
            )

        self._client = cohere.ClientV2(
            api_key=api_key,
        )

    def generate(
        self,
        prompt: str,
        language: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a response using Cohere."""

        def request() -> str:
            messages: list[dict[str, str]] = []

            if system_prompt:
                messages.append(
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            response = self._client.chat(
                model=self.model_id,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_OUTPUT_TOKENS,
            )

            if not response.message.content:
                raise RuntimeError(
                    f"Cohere returned no content for model "
                    f"'{self.model_id}'."
                )

            # Cohere can return multiple content blocks.
            text_parts: list[str] = []

            for block in response.message.content:

                if hasattr(block, "text") and block.text:
                    text_parts.append(
                        block.text
                    )

            text = "\n".join(
                text_parts
            ).strip()

            if not text:
                raise RuntimeError(
                    f"Cohere returned no text for model "
                    f"'{self.model_id}'. "
                    f"Raw response: {response!r}"
                )

            return text

        return self._with_retries(request)


# ============================================================================
# Runner Factory
# ============================================================================


def create_runner(
    provider: str,
    model_id: str,
    timeout_seconds: float = 60.0,
) -> ModelRunner:
    """Create and initialize a provider-specific model runner.

    Parameters
    ----------
    provider:
        Provider name:
            ``gemini``
            ``groq``
            ``cohere``

    model_id:
        Exact API model identifier.

    timeout_seconds:
        Maximum time allowed for an API request.

    Returns
    -------
    ModelRunner
        Initialized provider-specific runner.

    Raises
    ------
    ValueError
        If the provider is unsupported.
    """

    provider = provider.lower().strip()

    if provider == "gemini":
        return GeminiRunner(
            model_id=model_id,
            timeout_seconds=timeout_seconds,
        )

    if provider == "groq":
        return GroqRunner(
            model_id=model_id,
            timeout_seconds=timeout_seconds,
        )

    if provider == "cohere":
        return CohereRunner(
            model_id=model_id,
            timeout_seconds=timeout_seconds,
        )

    raise ValueError(
        f"Unsupported provider: {provider!r}. "
        "Expected one of: gemini, groq, cohere."
    )