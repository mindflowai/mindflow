import openai

from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject, StaticObject
from mindflow.db.objects.service import ServiceConfig
from mindflow.db.objects.static_definition.model import ModelID

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
        
        service_config = ServiceConfig.load(self.service)
        self.api_key = service_config.api_key

        self.__call__ = self.get_call()
    
    def openai_chat_completion(self, messages: list, max_tokens: int = 500, temperature: float = 0.0, stop: list = ["\n\n"]): 
        openai.api_key = self.api_key
        openai.ChatCompletion.create(
            model=self.id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop
        )

    def openai_embedding(self, text: str): 
        openai.api_key = self.api_key
        openai.Embedding.create(
            model=self.id,
            query=text
        )
    

    def get_call(self):
        if self.service == "openai":
            if self.id == ["gpt-3-5-turbo", "gpt-3-5-turbo-0301"]:
                return self.openai_chat_completion
            else:
                return self.openai_embedding
        else: 
            raise NotImplementedError(f"Service {self.service} not implemented.")

class ConfiguredModels:
    @property
    def gpt_3_5_turbo(self):
        return ConfiguredModel(ModelID.GPT_3_5_TURBO.value)

    @property
    def gpt_3_5_turbo_0301(self):
        return ConfiguredModel(ModelID.GPT_3_5_TURBO_0301.value)
    
    @property
    def text_embedding_ada_002(self):
        return ConfiguredModel(ModelID.TEXT_EMBEDDING_ADA_002.value)
