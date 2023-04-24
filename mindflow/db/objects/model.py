import time
from typing import Optional, Union

import openai
import anthropic

import numpy as np
from traitlets import Callable

from mindflow.db.objects.static_definition.model_type import ModelType

import tiktoken

from mindflow.db.db.json import JSON_DATABASE
from mindflow.db.db.static import STATIC_DATABASE
from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject
from mindflow.db.objects.service import ServiceConfig
from mindflow.db.objects.static_definition.model import ModelID
from mindflow.db.objects.static_definition.service import ServiceID
from mindflow.utils.errors import ModelError


class Model(BaseObject):
    """Model object."""

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

    _collection: Collection = Collection.MODEL
    _database = STATIC_DATABASE


class ModelConfig(BaseObject):
    """Model config object."""

    id: str
    soft_token_limit: int

    _collection: Collection = Collection.CONFIGURATIONS
    _database = JSON_DATABASE


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
        model = Model.load(model_id)
        model_config = ModelConfig.load(f"{model_id}_config")

        if model:
            for key, value in model.__dict__.items():
                setattr(self, key, value)

        if model_config:
            for key, value in model_config.__dict__.items():
                if value not in [None, ""]:
                    setattr(self, key, value)

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

        service_config = ServiceConfig.load(f"{self.service}_config")
        self.api_key = service_config.api_key

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
                response = client.completion(
                    prompt=prompt,
                    stop_sequences=[],
                    model=self.id,
                    max_tokens_to_sample=max_tokens,
                    temperature=temperature,
                )["completion"]
                return response
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
        if self.service == ServiceID.OPENAI.value:
            if self.model_type == ModelType.TEXT_COMPLETION.value:
                return self.openai_chat_completion(prompt, *args, **kwargs)
            else:
                return self.openai_embedding(prompt, *args, **kwargs)
        elif self.service == ServiceID.ANTHROPIC.value:
            if self.model_type == ModelType.TEXT_COMPLETION.value:
                return self.anthropic_chat_completion(prompt, *args, **kwargs)
        else:
            raise NotImplementedError(f"Service {self.service} not implemented.")
