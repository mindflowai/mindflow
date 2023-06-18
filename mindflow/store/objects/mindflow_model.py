import sys
from typing import Dict
from typing import Optional
from mindflow.store.traits.static import StaticStore
from mindflow.store.traits.json import JsonStore

from mindflow.store.objects.model import ConfiguredModel
from mindflow.store.objects.service import ConfiguredServices
from mindflow.store.objects.static_definition.mind_flow_model import MindFlowModelID
from mindflow.store.objects.static_definition.service import (
    ServiceConfigParameterKey,
    ServiceID,
)


class MindFlowModel(StaticStore):
    id: str  # index, query, embedding
    name: str
    defaults: Dict[str, str]
    model: str


class MindFlowModelConfig(JsonStore):
    id: str
    model: str


class ConfiguredMindFlowModel:
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
        model_id: Optional[str] = None
        # print(configured_services.openai.__dict__)
        if hasattr(configured_services.openai, ServiceConfigParameterKey.API_KEY.value):
            service = configured_services.openai
            model_id = self.defaults.get(ServiceID.OPENAI.value, None)
        elif hasattr(
            configured_services.anthropic, ServiceConfigParameterKey.API_KEY.value
        ):
            service = configured_services.anthropic
            model_id = self.defaults.get(ServiceID.ANTHROPIC.value, None)
        else:
            print(
                "No service API key configured. Please configure an API key for at least one service."
            )
            sys.exit(1)

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
        self._configured_services = configured_services
        self._mind_flow_models: Dict[str, ConfiguredMindFlowModel] = {}

    @property
    def index(self):
        if MindFlowModelID.INDEX.value not in self._mind_flow_models:
            self._mind_flow_models[
                MindFlowModelID.INDEX.value
            ] = ConfiguredMindFlowModel(
                MindFlowModelID.INDEX.value, self._configured_services
            )
        return self._mind_flow_models[MindFlowModelID.INDEX.value]

    @property
    def query(self):
        if MindFlowModelID.QUERY.value not in self._mind_flow_models:
            self._mind_flow_models[
                MindFlowModelID.QUERY.value
            ] = ConfiguredMindFlowModel(
                MindFlowModelID.QUERY.value, self._configured_services
            )
        return self._mind_flow_models[MindFlowModelID.QUERY.value]

    @property
    def embedding(self):
        if MindFlowModelID.EMBEDDING.value not in self._mind_flow_models:
            self._mind_flow_models[
                MindFlowModelID.EMBEDDING.value
            ] = ConfiguredMindFlowModel(
                MindFlowModelID.EMBEDDING.value, self._configured_services
            )
        return self._mind_flow_models[MindFlowModelID.EMBEDDING.value]