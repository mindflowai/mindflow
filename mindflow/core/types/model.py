from abc import ABC, abstractmethod
import asyncio

import aiohttp
import logging
import time
from result import Err, Ok, Result

from typing import Dict, Optional, Tuple, Union

import numpy as np
import tiktoken
from mindflow.core.token_counting import (
    get_token_count_of_messages_for_model,
    get_token_count_of_text_for_model,
)

from mindflow.core.types.store_traits.json import JsonStore
from mindflow.core.types.store_traits.static import StaticStore
from mindflow.core.types.service import ServiceConfig
from mindflow.core.types.definitions.model import ModelID
from mindflow.core.types.definitions.service import ServiceID


class ModelConfig(JsonStore):
    id: str
    soft_token_limit: int


class Model(StaticStore):
    id: str
    api: str
    name: str
    url: str
    service: str
    model_type: str
    default_soft_token_limit: int
    hard_token_limit: int
    token_cost: int
    token_cost_unit: str
    max_requests_per_minute: int
    max_tokens_per_minute: int

    config_description: Optional[str]
    config: ModelConfig


class ModelStatusTracker:
    def __init__(self, max_requests_per_minute: float, max_tokens_per_minute: float):
        self._max_requests_per_minute = max_requests_per_minute
        self._max_tokens_per_minute = max_tokens_per_minute

        self._time_capacities_last_updated = time.time()
        self._time_of_last_api_error = 0
        self._time_of_last_rate_limit_error = 0
        self._time_of_last_other_error = 0

        self._available_request_capacity = max_requests_per_minute
        self._available_token_capacity = max_tokens_per_minute

        self._requests_count_total = 0
        self._requests_count_failed = 0
        self._requests_count_successful = 0
        self._requests_count_in_progress = 0

        self._error_count_rate_limit = 0
        self._error_count_api = 0
        self._error_count_other = 0

        self._tokens_count_total = 0

        self._time_capacities_last_updated_lock = asyncio.Lock()
        self._time_of_last_error_api_lock = asyncio.Lock()
        self._time_of_last_error_rate_limit_lock = asyncio.Lock()
        self._time_of_last_error_other_lock = asyncio.Lock()

        self._available_request_capacity_lock = asyncio.Lock()
        self._available_token_capacity_lock = asyncio.Lock()

        self._requests_count_total_lock = asyncio.Lock()
        self._requests_count_failed_lock = asyncio.Lock()
        self._requests_count_successful_lock = asyncio.Lock()
        self._requests_count_in_progress_lock = asyncio.Lock()

        self._error_count_rate_limit_lock = asyncio.Lock()
        self._error_count_api_lock = asyncio.Lock()
        self._error_count_other_lock = asyncio.Lock()

        self._tokens_count_total_lock = asyncio.Lock()

    async def get_available_capacities(self) -> Tuple[float, float]:
        async with self._available_request_capacity_lock:
            current_time = time.time()
            seconds_since_last_update = (
                current_time - self._time_capacities_last_updated
            )
            self._time_capacities_last_updated = current_time

            self._available_request_capacity = available_request_capacity = min(
                self._available_request_capacity
                + self._max_requests_per_minute * seconds_since_last_update / 60.0,
                self._max_requests_per_minute,
            )
            self._available_token_capacity = available_token_capacity = min(
                self._available_token_capacity
                + self._max_tokens_per_minute * seconds_since_last_update / 60.0,
                self._max_tokens_per_minute,
            )
            return available_request_capacity, available_token_capacity

    async def increment_requests_count_total(self):
        async with self._requests_count_total_lock:
            self._requests_count_total += 1

    async def increment_requests_count_failed(self):
        async with self._requests_count_failed_lock:
            self._requests_count_failed += 1

    async def increment_requests_count_successful(self):
        async with self._requests_count_successful_lock:
            self._requests_count_successful += 1

    async def increment_requests_count_in_progress(self):
        async with self._requests_count_in_progress_lock:
            self._requests_count_in_progress += 1

    async def decrement_requests_count_in_progress(self):
        async with self._requests_count_in_progress_lock:
            self._requests_count_in_progress -= 1

    async def increment_error_count_rate_limit(self):
        async with self._error_count_rate_limit_lock and self._time_of_last_error_rate_limit_lock:
            self._error_count_rate_limit += 1
            self._time_of_last_rate_limit_error = time.time()

    async def increment_error_count_api(self):
        async with self._error_count_api_lock and self._time_of_last_error_api_lock:
            self._error_count_api += 1
            self._time_of_last_api_error = time.time()

    async def increment_error_count_other(self):
        async with self._error_count_other_lock and self._time_of_last_error_other_lock:
            self._error_count_other += 1
            self._time_of_last_other_error = time.time()

    async def add_tokens_count_total(self, tokens: int):
        async with self._tokens_count_total_lock:
            self._tokens_count_total += tokens


class RateLimitError(Exception):
    def __init__(self, message: str):
        self.message = message


class APIError(Exception):
    def __init__(self, message: str):
        self.message = message


class UncaughtModelException(Exception):
    def __init__(self, message: str):
        self.message = message


ModelApiCallError = Union[RateLimitError, APIError, UncaughtModelException]


class ConfiguredModel(ABC):
    model: Model
    config: ModelConfig

    tokenizer: tiktoken.Encoding
    status_tracker: ModelStatusTracker
    headers: Dict[str, str]

    api_key: str

    def __init__(self, model_id: str):
        if model := Model.load(model_id):
            self.model = model

        if model_config := ModelConfig.load(f"{model_id}_config"):
            self.config = model_config
        else:
            self.config = ModelConfig(
                {
                    "id": f"{model_id}_config",
                    "soft_token_limit": self.model.default_soft_token_limit,
                }
            )

        if service_config := ServiceConfig.load(f"{self.model.service}_config"):
            self.api_key = service_config.api_key

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.status_tracker = ModelStatusTracker(
            self.model.max_requests_per_minute, self.model.max_tokens_per_minute
        )

        try:
            if self.model.service == ServiceID.OPENAI.value:
                if self.model.id == ModelID.GPT_4.value:
                    self.tokenizer = tiktoken.encoding_for_model(
                        ModelID.GPT_3_5_TURBO.value
                    )
                else:
                    self.tokenizer = tiktoken.encoding_for_model(self.model.id)
        except NameError:
            pass


class ApiTextCompletionModel(ABC):
    @abstractmethod
    async def call_api(self, *args, **kwargs) -> Result[str, ModelApiCallError]:
        pass


class ApiEmbeddingModel(ABC):
    @abstractmethod
    async def call_api(self, *args, **kwargs) -> Result[np.ndarray, ModelApiCallError]:
        pass


class ConfiguredTextCompletionModel(ApiTextCompletionModel, ConfiguredModel, ABC):
    pass


class ConfiguredEmbeddingModel(ApiEmbeddingModel, ConfiguredModel, ABC):
    pass


class ConfiguredOpenAIChatCompletionModel(ConfiguredTextCompletionModel):
    async def call_api(
        self,
        messages: list,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        stop: Optional[list] = None,
        request_tokens: Optional[int] = None,
    ) -> Result[str, ModelApiCallError]:
        assert isinstance(messages, list) and len(messages) > 0
        assert request_tokens is None or request_tokens > 0
        assert max_tokens is None or max_tokens > 0
        assert temperature >= 0.0 and temperature <= 1.0
        assert stop is None or isinstance(stop, list)

        payload = {
            "model": self.model.id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
        }

        if request_tokens is None:
            request_tokens = get_token_count_of_messages_for_model(
                self.tokenizer, messages
            )

        while True:
            (
                available_request_capacity,
                available_token_capacity,
            ) = await self.status_tracker.get_available_capacities()
            if (
                available_request_capacity < 1
                or available_token_capacity < request_tokens
            ):
                await asyncio.sleep(0.001)
                continue
            break

        try_count = 0
        model_error: Err
        await self.status_tracker.increment_requests_count_total()
        await self.status_tracker.increment_requests_count_in_progress()
        await self.status_tracker.add_tokens_count_total(request_tokens)
        async with aiohttp.ClientSession() as session:
            while try_count < 5:
                try:
                    async with session.post(
                        self.model.url, headers=self.headers, json=payload
                    ) as response:
                        result = await response.json()

                        if "error" not in result:
                            await self.status_tracker.increment_requests_count_successful()
                            await self.status_tracker.decrement_requests_count_in_progress()
                            # print(result)
                            return Ok(result["choices"][0]["message"]["content"])

                        logging.warning(
                            f"Request {payload} failed with error {result['error']}"
                        )
                        try_count += 1
                        if "Rate limit" in result["error"].get("message", ""):
                            model_error = Err(RateLimitError(result["error"]))
                            await self.status_tracker.increment_error_count_rate_limit()
                            await asyncio.sleep(5)
                            continue

                        model_error = Err(APIError(result["error"]))
                        await self.status_tracker.increment_error_count_api()

                except Exception as e:
                    logging.warning(f"Request {payload} failed with exception {e}")
                    await self.status_tracker.increment_error_count_other()
                    return Err(UncaughtModelException(str(e)))

            return model_error


class ConfiguredAnthropicChatCompletionModel(ConfiguredTextCompletionModel):
    async def call_api(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = 100,
        request_tokens: Optional[int] = None,
    ) -> Result[str, ModelApiCallError]:
        assert isinstance(prompt, str) and prompt != ""
        assert request_tokens is None or request_tokens > 0
        assert max_tokens is None or max_tokens > 0
        assert temperature >= 0.0 and temperature <= 1.0

        payload = {
            "model": self.model.id,
            "prompt": prompt,
            "stop_sequences": [],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if request_tokens is None:
            request_tokens = get_token_count_of_text_for_model(self.tokenizer, prompt)

        while True:
            (
                available_request_capacity,
                available_token_capacity,
            ) = await self.status_tracker.get_available_capacities()
            if (
                available_request_capacity < 1
                or available_token_capacity < request_tokens
            ):
                await asyncio.sleep(0.001)
                continue
            break

        try_count = 0
        model_error: Err
        await self.status_tracker.increment_requests_count_total()
        await self.status_tracker.increment_requests_count_in_progress()
        await self.status_tracker.add_tokens_count_total(request_tokens)
        async with aiohttp.ClientSession() as session:
            while try_count < 5:
                try:
                    async with session.post(
                        self.model.url, headers=self.headers, json=payload
                    ) as response:
                        result = await response.json()

                        if "error" not in result:
                            await self.status_tracker.increment_requests_count_successful()
                            await self.status_tracker.decrement_requests_count_in_progress()
                            return Ok(result["completion"])

                        logging.warning(
                            f"Request {payload} failed with exception {result['error']}"
                        )

                        # Figure out how to catch rate limiting errors
                        try_count += 1
                        model_error = Err(APIError(result["error"]))
                        await self.status_tracker.increment_error_count_other()

                except Exception as e:
                    logging.warning(f"Request {payload} failed with exception {e}")
                    await self.status_tracker.increment_error_count_other()
                    return Err(UncaughtModelException(str(e)))

            return model_error


class ConfiguredOpenAITextEmbeddingModel(ConfiguredEmbeddingModel):
    async def call_api(
        self, text: str, request_tokens: Optional[int] = None
    ) -> Result[np.ndarray, ModelApiCallError]:
        assert isinstance(text, str) and text != ""

        payload = {
            "model": self.model.id,
            "input": text,
        }

        # May need to update tokenizer for embedding models.
        if request_tokens is None:
            request_tokens = get_token_count_of_text_for_model(self.tokenizer, text)

        while True:
            (
                available_request_capacity,
                available_token_capacity,
            ) = await self.status_tracker.get_available_capacities()
            if (
                available_request_capacity < 1
                or available_token_capacity < request_tokens
            ):
                await asyncio.sleep(0.001)
                continue
            break

        try_count = 0
        model_error: Err
        await self.status_tracker.increment_requests_count_total()
        await self.status_tracker.increment_requests_count_in_progress()
        await self.status_tracker.add_tokens_count_total(request_tokens)
        async with aiohttp.ClientSession() as session:
            while try_count < 5:
                try:
                    async with session.post(
                        self.model.url, headers=self.headers, json=payload
                    ) as response:
                        result = await response.json()

                        if "error" not in result:
                            await self.status_tracker.increment_requests_count_successful()
                            await self.status_tracker.decrement_requests_count_in_progress()
                            return Ok(np.array(result["data"][0]["embedding"]))

                        e = str(result["error"])
                        logging.warning(
                            f"Request {payload} failed with error {result['error']}"
                        )
                        try_count += 1
                        if "Rate limit" in result["error"].get("message", ""):
                            model_error = Err(RateLimitError(result["error"]))
                            await self.status_tracker.increment_error_count_rate_limit()
                            await asyncio.sleep(5)
                            continue
                        model_error = Err(APIError(result["error"]))
                        await self.status_tracker.increment_error_count_api()

                except Exception as e:
                    logging.warning(f"Request {payload} failed with exception {e}")
                    await self.status_tracker.increment_error_count_other()
                    return Err(UncaughtModelException(str(e)))

            return model_error
