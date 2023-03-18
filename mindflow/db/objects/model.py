from typing import Optional, Union

import openai
import numpy as np
from traitlets import Callable

try:
    import tiktoken
except ImportError:
    print(
        "tiktoken not not available in python<=v3.8. Estimation of tokens will be less precise, which may impact performance and quality of responses."
    )
    print("Upgrade to python v3.8 or higher for better results.")
    pass

from mindflow.db.controller import DATABASE_CONTROLLER
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
    _database = DATABASE_CONTROLLER.databases.static


class ModelConfig(BaseObject):
    """Model config object."""

    id: str
    soft_token_limit: int

    _collection: Collection = Collection.CONFIGURATIONS
    _database = DATABASE_CONTROLLER.databases.json


class ConfiguredModel(Callable):
    id: str
    name: str
    service: str
    model_type: str

    try:
        tokenizer: tiktoken.Encoding
    except NameError:
        pass

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
        try:
            openai.api_key = self.api_key
            return openai.ChatCompletion.create(
                model=self.id,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
            )["choices"][0]["message"]["content"]
        except ModelError as e:
            return e

    def openai_embedding(self, text: str) -> Union[np.ndarray, ModelError]:
        try:
            openai.api_key = self.api_key
            return openai.Embedding.create(engine=self.id, input=text)["data"][0][
                "embedding"
            ]
        except ModelError as e:
            return e

    def __call__(self, prompt, *args, **kwargs):
        if self.service == ServiceID.OPENAI.value:
            if self.id in [
                ModelID.GPT_3_5_TURBO.value,
                ModelID.GPT_3_5_TURBO_0301.value,
                ModelID.GPT_4.value,
            ]:
                return self.openai_chat_completion(prompt, *args, **kwargs)
            else:
                return self.openai_embedding(prompt, *args, **kwargs)
        else:
            raise NotImplementedError(f"Service {self.service} not implemented.")
