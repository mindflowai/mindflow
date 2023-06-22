import time
from typing import Optional, Union

import openai
import anthropic

import numpy as np
from traitlets import Callable

from mindflow.core.types.definitions.model_type import ModelType

import tiktoken

from mindflow.core.types.store_traits.json import JsonStore
from mindflow.core.types.store_traits.static import StaticStore
from mindflow.core.types.service import ServiceConfig
from mindflow.core.types.definitions.model import ModelID
from mindflow.core.types.definitions.service import ServiceID
from mindflow.core.errors import ModelError


class Model(StaticStore):
    id: str
    api: str
    name: str
    service: str
    model_type: str
    hard_token_limit: int
    token_cost: int
    token_cost_unit: str

    config_description: Optional[str]

    # Config
    soft_token_limit: int


class ModelConfig(JsonStore):
    id: str
    soft_token_limit: int


class ConfiguredModel(Callable):
    id: str
    name: str
    service: str
    model_type: str

    tokenizer: tiktoken.Encoding

    hard_token_limit: int
    token_cost: int
    token_cost_unit: str

    # Config
    soft_token_limit: int
    api_key: str

    def __init__(self, model_id: str):
        if model := Model.load(model_id):
            for key, value in model.__dict__.items():
                setattr(self, key, value)

        if model_config := ModelConfig.load(f"{model_id}_config"):
            for key, value in model_config.__dict__.items():
                setattr(self, key, value)

        if service_config := ServiceConfig.load(f"{self.service}_config"):
            if hasattr(service_config, "api_key"):
                self.api_key = service_config.api_key

        try:
            if self.service == ServiceID.OPENAI.value:
                if self.id == ModelID.GPT_4.value:
                    self.tokenizer = tiktoken.encoding_for_model(
                        ModelID.GPT_3_5_TURBO.value
                    )
                else:
                    self.tokenizer = tiktoken.encoding_for_model(self.id)
        except NameError:
            pass

    def openai_chat_completion(
        self,
        messages: list,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        stop: Optional[list] = None,
    ) -> Union[str, ModelError]:
        try_count = 0
        error_message = ""
        while try_count < 5:
            try:
                openai.api_key = self.api_key
                return openai.ChatCompletion.create(
                    model=self.id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stop=stop,
                )["choices"][0]["message"]["content"]
            except Exception as e:
                try_count += 1
                error_message = f"Error: {str(e)}"
                time.sleep(5)

        return ModelError(error_message)

    def anthropic_chat_completion(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = 100,
    ) -> Union[str, ModelError]:
        try_count = 0
        error_message = ""
        while try_count < 5:
            try:
                client = anthropic.Client(self.api_key)
                return client.completion(
                    prompt=prompt,
                    stop_sequences=[],
                    model=self.id,
                    max_tokens_to_sample=max_tokens,
                    temperature=temperature,
                )["completion"]
            except Exception as e:
                try_count += 1
                error_message = f"Error: {str(e)}"
                time.sleep(5)

        return ModelError(error_message)

    def openai_embedding(self, text: str) -> Union[np.ndarray, ModelError]:
        try_count = 0
        error_message = ""
        while try_count < 5:
            try:
                openai.api_key = self.api_key
                return openai.Embedding.create(engine=self.id, input=text)["data"][0][
                    "embedding"
                ]
            except Exception as e:
                try_count += 1
                error_message = f"Error: {str(e)}"
                time.sleep(5)

        return ModelError(error_message)

    def __call__(self, prompt, *args, **kwargs):
        service_model_mapping = {
            (
                ServiceID.OPENAI.value,
                ModelType.TEXT_COMPLETION.value,
            ): self.openai_chat_completion,
            (
                ServiceID.OPENAI.value,
                ModelType.TEXT_EMBEDDING.value,
            ): self.openai_embedding,
            (
                ServiceID.ANTHROPIC.value,
                ModelType.TEXT_COMPLETION.value,
            ): self.anthropic_chat_completion,
        }
        if (
            func := service_model_mapping.get((self.service, self.model_type))
        ) is not None:
            return func(prompt, *args, **kwargs)
        raise NotImplementedError(f"Service {self.service} not implemented.")
