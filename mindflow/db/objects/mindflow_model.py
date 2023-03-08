import sys
from typing import Dict
from typing import Optional

from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject
from mindflow.db.objects.base import StaticObject
from mindflow.db.objects.model import ConfiguredModel
from mindflow.db.objects.model import Model
from mindflow.db.objects.service import ConfiguredServices
from mindflow.db.objects.static_definition.mind_flow_model import MindFlowModelID


class MindFlowModel(StaticObject):
    """MindFlow model object."""

    id: str  # index, query, embedding
    name: str
    defaults: Dict[str, str]
    model: str

    _collection: Collection = Collection.MIND_FLOW_MODEL


class MindFlowModelConfig(BaseObject):
    """MindFlow model config object."""

    id: str
    model: str

    _collection: Collection = Collection.CONFIGURATIONS


class ConfiguredMindFlowModel:
    """MindFlow model object."""

    id: str  # index, query, embedding
    name: str
    defaults: Dict[str, str]
    model: ConfiguredModel

    def __init__(self, mindflow_model_id: str, configured_services: ConfiguredServices):
        self.id = mindflow_model_id

        mind_flow_model = MindFlowModel.load(mindflow_model_id)
        mind_flow_model_config = MindFlowModelConfig.load(f"{mindflow_model_id}_config")

        if mind_flow_model:
            for key, value in mind_flow_model.__dict__.items():
                setattr(self, key, value)

        model_id: Optional[str] = None
        if mind_flow_model_config:
            if hasattr(mind_flow_model_config, "model"):
                model_id = mind_flow_model_config.model

        if model_id is None:
            model_id = self.get_default_model_id(mindflow_model_id, configured_services)

        self.model = ConfiguredModel(model_id)

    def get_default_model_id(
        self, mindflow_model_id: str, configured_services: ConfiguredServices
    ) -> str:
        if hasattr(configured_services.openai, "api_key"):
            service = configured_services.openai
        else:
            print(
                "No service API key configured. Please configure an API key for at least one service."
            )
            sys.exit(1)

        model_id = self.defaults.get("openai", None)

        if model_id is None:
            raise Exception(
                "No default model configured for mindflow model: "
                + mindflow_model_id
                + " and service: "
                + service.id
            )

        return model_id


class ConfiguredMindFlowModels:
    def __init__(self, configured_services: ConfiguredServices):
        self.configured_services = configured_services

    @property
    def index(self):
        model = ConfiguredMindFlowModel(
            MindFlowModelID.INDEX.value, self.configured_services
        )
        return model

    @property
    def query(self):
        model = ConfiguredMindFlowModel(
            MindFlowModelID.QUERY.value, self.configured_services
        )
        return model

    @property
    def embedding(self):
        model = ConfiguredMindFlowModel(
            MindFlowModelID.EMBEDDING.value, self.configured_services
        )
        return model
