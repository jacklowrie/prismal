"""Inference clients for prismal."""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, NoReturn

from dotenv import load_dotenv
from loguru import logger
from openai import AsyncOpenAI, OpenAI
from pydantic import BaseModel
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from tqdm.asyncio import tqdm

# Load environment variables from .env if present
load_dotenv()

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletionMessageParam


class InferenceResponse(BaseModel):
    """Standardized response from an inference client."""

    content: str
    raw_response: Any


class AsyncRateLimiter:
    """A simple token-bucket rate limiter for asyncio.

    This ensures that requests (including retries) do not exceed a certain
    Requests Per Minute (RPM) limit.
    """

    def __init__(self, requests_per_minute: int) -> None:
        """Initialize the rate limiter.

        Args:
            requests_per_minute: Maximum number of requests allowed per minute.
        """
        self.rpm = requests_per_minute
        self.delay = 60.0 / requests_per_minute if requests_per_minute > 0 else 0
        self.last_request_time = 0.0
        self.lock = asyncio.Lock()

    async def wait(self) -> None:
        """Wait for a token to become available."""
        if self.delay <= 0:
            return

        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_request_time
            sleep_time = self.delay - elapsed

            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                self.last_request_time = time.monotonic()
            else:
                self.last_request_time = now


class BaseInferenceClient(ABC):
    """Base class for all inference clients."""

    @abstractmethod
    def generate(
        self,
        model_id: str,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> InferenceResponse:
        """Generate a response from the model."""
        pass


class BaseAsyncInferenceClient(ABC):
    """Base class for all asynchronous inference clients."""

    @abstractmethod
    async def generate(
        self,
        model_id: str,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> InferenceResponse:
        """Generate a response from the model asynchronously."""
        pass

    async def generate_batch(
        self,
        model_id: str,
        prompts: list[str],
        system_prompts: list[str | None] | None = None,
        max_concurrency: int | None = None,
        rpm_limit: int | None = None,
        show_progress: bool = False,
        **kwargs: Any,  # noqa: ANN401
    ) -> list[InferenceResponse | BaseException]:
        """Generate a batch of responses concurrently.

        Args:
            model_id: The ID of the model to use.
            prompts: A list of user prompts.
            system_prompts: An optional list of system prompts (one per user prompt).
            max_concurrency: Maximum number of concurrent requests.
            rpm_limit: Maximum requests per minute.
            show_progress: Whether to show a progress bar.
            **kwargs: Additional parameters passed to generate().

        Returns:
            A list of InferenceResponse objects or Exceptions if individual
            requests failed.
        """
        if system_prompts is None:
            system_prompts = [None] * len(prompts)

        if len(prompts) != len(system_prompts):
            msg = "prompts and system_prompts must have the same length."
            raise ValueError(msg)

        # Set the client-level RPM limit if provided
        if rpm_limit and hasattr(self, "rate_limiter"):
            self.rate_limiter = AsyncRateLimiter(rpm_limit)

        semaphore = asyncio.Semaphore(max_concurrency) if max_concurrency else None

        async def sem_generate(p: str, s: str | None) -> InferenceResponse:
            if semaphore:
                async with semaphore:
                    return await self.generate(model_id, p, s, **kwargs)
            return await self.generate(model_id, p, s, **kwargs)

        tasks = [
            sem_generate(p, s) for p, s in zip(prompts, system_prompts, strict=True)
        ]

        if show_progress:
            # We use asyncio.gather and wrap it with a progress update logic
            # to avoid tqdm.gather issues with return_exceptions
            pbar = tqdm(total=len(tasks))

            async def wrapped_task(task: Any) -> Any:  # noqa: ANN401
                try:
                    return await task
                finally:
                    pbar.update(1)

            wrapped_tasks = [wrapped_task(t) for t in tasks]
            try:
                return await asyncio.gather(*wrapped_tasks, return_exceptions=True)
            finally:
                pbar.close()

        return await asyncio.gather(*tasks, return_exceptions=True)


class OpenAIInferenceClient(BaseInferenceClient):
    """Client for OpenAI-compatible APIs (like PGAIS)."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        max_retries: int = 5,
    ) -> None:
        """Initialize the OpenAI client.

        Args:
            api_key: The API key. Defaults to OPENAI_API_KEY environment variable.
            base_url: The base URL for the API.
            max_retries: Number of times to retry failed requests.
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.max_retries = max_retries

    def generate(
        self,
        model_id: str,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> InferenceResponse:
        """Generate a response using the OpenAI-compatible API."""

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_random_exponential(multiplier=1, min=4, max=60),
            retry=retry_if_exception_type((ValueError, Exception)),
            reraise=True,
        )
        def _generate_with_retry() -> InferenceResponse:
            messages: list[ChatCompletionMessageParam] = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            try:
                response = self.client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    **kwargs,
                )
                if (
                    not response
                    or not hasattr(response, "choices")
                    or not response.choices
                ):
                    return self._handle_invalid_response(response)

                content = response.choices[0].message.content or ""
                return InferenceResponse(content=content, raw_response=response)
            except Exception:
                logger.warning("Inference attempt failed for model {}", model_id)
                raise

        return _generate_with_retry()

    def _handle_invalid_response(self, response: Any) -> NoReturn:  # noqa: ANN401
        """Raise an error for an invalid response."""
        msg = f"Invalid or empty response from API: {response}"
        raise ValueError(msg)


class AsyncOpenAIInferenceClient(BaseAsyncInferenceClient):
    """Asynchronous client for OpenAI-compatible APIs."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        max_retries: int = 5,
        requests_per_minute: int = 20,
    ) -> None:
        """Initialize the async OpenAI client.

        Args:
            api_key: The API key.
            base_url: The base URL.
            max_retries: Number of retries for failed requests.
            requests_per_minute: Global RPM limit (including retries).
        """
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.max_retries = max_retries
        self.rate_limiter = AsyncRateLimiter(requests_per_minute)

    async def generate(
        self,
        model_id: str,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> InferenceResponse:
        """Generate a response using the async OpenAI-compatible API."""

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_random_exponential(multiplier=1, min=4, max=60),
            retry=retry_if_exception_type((ValueError, Exception)),
            reraise=True,
        )
        async def _generate_with_retry() -> InferenceResponse:
            # Wait for rate limiter before every attempt
            await self.rate_limiter.wait()
            messages: list[ChatCompletionMessageParam] = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            try:
                response = await self.client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    **kwargs,
                )
                if (
                    not response
                    or not hasattr(response, "choices")
                    or not response.choices
                ):
                    self._handle_invalid_response(response)

                content = response.choices[0].message.content or ""
                return InferenceResponse(content=content, raw_response=response)
            except Exception as e:
                logger.warning(
                    "Async inference attempt failed for model {} (Error: {})",
                    model_id,
                    str(e),
                )
                raise

        return await _generate_with_retry()

    def _handle_invalid_response(self, response: Any) -> NoReturn:  # noqa: ANN401
        """Raise an error for an invalid response."""
        msg = f"Invalid or empty response from API: {response}"
        raise ValueError(msg)
