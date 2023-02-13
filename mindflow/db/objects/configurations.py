from typing import Optional
from mindflow.db.db import DATABASE
from mindflow.db.static_definition import Collection


class ModelConfig(object):
    """Model config object."""

    soft_token_limit: int

    def __init__(self, params: Optional[dict]):
        if not params or params == {}:
            params = {}
        self.soft_token_limit = params.get("soft_token_limit", None)


class ModelConfigs(object):
    """Model config object."""

    openai: ModelConfig

    def __init__(self, params: Optional[dict]):
        if not params or params == {}:
            params = {}
        self.openai = ModelConfig(params.get("openai", None))


class ServiceConfig(object):
    """Service config object."""

    api_key: str
    api_secret: str

    def __init__(self, params: Optional[dict]):
        if not params or params == {}:
            params = {}
        self.api_key = params.get("api_key", None)
        self.api_secret = params.get("api_secret", None)


class ServiceConfigs(object):
    """Service config object."""

    openai: ServiceConfig

    def __init__(self, params: Optional[dict]):
        if not params or params == {}:
            params = {}
        self.openai = ServiceConfig(params.get("openai", None))


class MindFlowModelConfig(object):
    """MindFlow model config object."""

    query: str
    index: str
    embedding: str

    def __init__(self, params: dict):
        if not params or params == {}:
            params = {}
        self.query = params.get("query", None)
        self.index = params.get("index", None)
        self.embedding = params.get("embedding", None)


class Configurations:
    id = "configurations"
    service_config: ServiceConfigs
    model_config: ModelConfigs
    mindflow_model_config: MindFlowModelConfig

    @classmethod
    def initialize(cls, user_configurations: dict):
        obj = cls()

        obj.id = "configurations"
        obj.service_config = ServiceConfigs(
            user_configurations.get("service_config", {})
        )
        obj.model_config = ModelConfigs(user_configurations.get("model_config", {}))
        obj.mindflow_model_config = MindFlowModelConfig(
            user_configurations.get("mindflow_model_config", {})
        )

        return obj

    def todict(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.todict(obj._ast())
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [self.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict(
                [
                    (key, self.todict(value, classkey))
                    for key, value in obj.__dict__.items()
                    if not callable(value) and not key.startswith("_")
                ]
            )
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj

    def save(self):
        user_configurations = self.todict(self)
        DATABASE.json.set_object(Collection.CONFIGURATIONS.value, user_configurations)
