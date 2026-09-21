"""Model runner interface (SAFE SKELETON — no API calls).

This module defines the interface that the future model runner will use. It
performs **no network activity**, requires no credentials, and cannot run
end-to-end yet. Every operation that will do real work later is either abstract
or raises ``NotImplementedError``.

Implementation TODOs (to be completed once the model list is finalized):

- model initialization (client; credentials read from the environment only)
- API request (per-provider implementation)
- response extraction (parse the provider's raw output)
- retry handling (transient failures, backoff)
- rate limiting (delay between requests)
- logging (request/response metadata for reproducibility)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Mapping, TypeVar

_T = TypeVar("_T")


class ModelRunner(ABC):
    """Interface for sending prompts to one LLM and collecting responses.

    Concrete per-provider subclasses will be written once the model list and
    API configuration are confirmed. Until then no subclass is required.
    """

    def __init__(self, model_id: str, timeout_seconds: float = 60.0) -> None:
        self.model_id = model_id
        self.timeout_seconds = timeout_seconds
        self._client: Any = None  # set by initialize()
        # TODO(logging): attach a logger here once logging is implemented.

    # ------------------------------------------------------------------
    # TODO(model-initialization): implement when the model list is final.
    # - read the API key from the environment (never from source code)
    # - instantiate and validate the provider client
    # - set up logging for this runner
    # ------------------------------------------------------------------
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the model client.

        Raises
        ------
        NotImplementedError
            Always, until the model list is finalized.
        """
        ...

    # ------------------------------------------------------------------
    # TODO(api-request): implement the actual HTTP/API call per provider.
    # - call self._rate_limit() before each request
    # - wrap the request with self._with_retries() for transient failures
    # - call self._extract_response() on the raw provider response
    # - call self._log() with request + response metadata
    # ------------------------------------------------------------------
    @abstractmethod
    def generate(self, prompt: str, language: str) -> str:
        """Send ``prompt`` to the model and return the extracted answer text.

        Parameters
        ----------
        prompt:
            The final prompt (see ``experiments.prompts.build_prompt``).
        language:
            The language of the prompt: ``"en"`` or ``"hi"``.

        Returns
        -------
        str
            The model's answer text.

        Raises
        ------
        NotImplementedError
            Always, until the provider API is implemented.
        """
        ...

    # ------------------------------------------------------------------
    # TODO(response-extraction): implement provider-specific parsing once the
    # raw response format is known. Providers may return chat messages, JSON
    # envelopes, or plain text, so extraction must be provider-specific.
    # ------------------------------------------------------------------
    def _extract_response(self, raw_response: Mapping[str, Any]) -> str:
        """Extract the answer text from a raw provider response (placeholder).

        Raises
        ------
        NotImplementedError
            Until the provider API is implemented.
        """
        raise NotImplementedError("Response extraction is not implemented yet.")

    # ------------------------------------------------------------------
    # TODO(retry-handling): implement retry with exponential backoff for
    # transient network/provider errors once API calls exist.
    # ------------------------------------------------------------------
    def _with_retries(
        self,
        fn: Callable[[], _T],
        *,
        max_attempts: int = 3,
        base_delay_seconds: float = 1.0,
    ) -> _T:
        """Run ``fn`` with retry and backoff (placeholder).

        Raises
        ------
        NotImplementedError
            Until the retry policy is implemented.
        """
        raise NotImplementedError("Retry handling is not implemented yet.")

    # ------------------------------------------------------------------
    # TODO(rate-limiting): implement a minimum delay between consecutive
    # requests, tuned to the provider's rate limits, once the API client
    # exists.
    # ------------------------------------------------------------------
    def _rate_limit(self) -> None:
        """Enforce a minimum delay between consecutive requests (placeholder).

        Raises
        ------
        NotImplementedError
            Until the rate limiter is implemented.
        """
        raise NotImplementedError("Rate limiting is not implemented yet.")

    # ------------------------------------------------------------------
    # TODO(logging): implement structured logging of every request/response
    # (run_id, timestamp, model_id, question_id, language, prompt, output)
    # so the experiment is fully reproducible.
    # ------------------------------------------------------------------
    def _log(self, record: Mapping[str, Any]) -> None:
        """Write a request/response metadata record (placeholder).

        Parameters
        ----------
        record:
            Dictionary with run_id, timestamp, model_id, question_id,
            language, prompt, and raw output.

        Raises
        ------
        NotImplementedError
            Until logging is implemented.
        """
        raise NotImplementedError("Logging is not implemented yet.")