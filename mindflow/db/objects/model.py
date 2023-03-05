from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject, StaticObject
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
    api: str
    name: str
    service: str
    model_type: str
    hard_token_limit: int
    token_cost: int
    token_cost_unit: str

    # Config
    soft_token_limit: int

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

class ConfiguredModels:
    @property
    def gpt_3_5_turbo(self):
        return ConfiguredModel(ModelID.GPT_3_5_TURBO.value)

    @property
    def gpt_3_5_turbo_0301(self):
        return ConfiguredModel(ModelID.GPT_3_5_TURBO_0301.value)

    @property
    def text_davinci_003(self):
        return ConfiguredModel(ModelID.TEXT_DAVINCI_003.value)

    @property
    def text_curie_001(self):
        return ConfiguredModel(ModelID.TEXT_CURIE_001.value)
    
    @property
    def text_babbage_001(self):
        return ConfiguredModel(ModelID.TEXT_BABBAGE_001.value)
    
    @property
    def text_ada_001(self):
        return ConfiguredModel(ModelID.TEXT_ADA_001.value)
    
    @property
    def text_embedding_ada_002(self):
        return ConfiguredModel(ModelID.TEXT_EMBEDDING_ADA_002.value)
