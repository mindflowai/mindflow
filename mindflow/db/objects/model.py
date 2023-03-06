import openai

from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject, StaticObject
from mindflow.db.objects.service import ServiceConfig
from mindflow.db.objects.static_definition.model import ModelID
from mindflow.db.objects.static_definition.service import ServiceID

class Model(StaticObject):
    """Model object."""

    id: str
    api: str
    name: str
    service: str
    model_type: str
    hard_token_limit: int
    token_cost: int
    token_cost_unit: str

    # Config
    soft_token_limit: int

    _collection: Collection = Collection.MODEL

class ModelConfig(BaseObject):
    """Model config object."""
    id: str
    soft_token_limit: int

    _collection: Collection = Collection.CONFIGURATIONS

class ConfiguredModel:
    id: str
    name: str
    service: str
    model_type: str
    hard_token_limit: int
    token_cost: int
    token_cost_unit: str

    # Config
    soft_token_limit: int
    api_key: str

    def __init__(self, model_id: str, api_key: str = None):
        model = Model.load(model_id)
        model_config = ModelConfig.load(f"{model_id}_config")
        
        if model:
            for key, value in model.__dict__.items():
                setattr(self, key, value)
            
        if model_config:
            for key, value in model_config.__dict__.items():
                if value not in [None, ""]:
                    setattr(self, key, value)
        
        service_config = ServiceConfig.load(f"{self.service}_config")
        self.api_key = service_config.api_key
    
    def openai_chat_completion(self, messages: list, max_tokens: int = 500, temperature: float = 0.0, stop: list = ["\n\n"]): 
        openai.api_key = self.api_key
        return openai.ChatCompletion.create(
            model=self.id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop
        )["choices"][0]["message"]["content"]

    def openai_embedding(self, text: str): 
        openai.api_key = self.api_key
        return openai.Embedding.create(
            engine=self.id,
            input=text
        )["data"][0]["embedding"]

    def __call__(self, prompt, *args, **kwargs):
        if self.service == ServiceID.OPENAI.value:
            if self.id in [ModelID.GPT_3_5_TURBO.value, ModelID.GPT_3_5_TURBO_0301.value]:
                return self.openai_chat_completion(prompt, *args, **kwargs)
            else:
                return self.openai_embedding(prompt, *args, **kwargs)
        else: 
            raise NotImplementedError(f"Service {self.service} not implemented.")
