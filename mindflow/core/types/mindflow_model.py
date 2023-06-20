import sys
from typing import Dict, Generic, TypeVar, cast
from mindflow.core.types.definitions.model import ModelID
from mindflow.core.types.store_traits.static import StaticStore
from mindflow.core.types.store_traits.json import JsonStore

from mindflow.core.types.model import (
    ConfiguredModel,
    ConfiguredOpenAIChatCompletionModel,
    ConfiguredAnthropicChatCompletionModel,
    ConfiguredOpenAITextEmbeddingModel,
)
from mindflow.core.types.service import ConfiguredServices
from mindflow.core.types.definitions.mind_flow_model import MindFlowModelID
from mindflow.core.types.definitions.service import (
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


T = TypeVar("T", bound="ConfiguredModel")


class ConfiguredMindFlowModel(Generic[T]):
    id: str  # index, query, embedding
    name: str
    defaults: Dict[str, str]
    model: T

    def __init__(self, mindflow_model_id: str, configured_services: ConfiguredServices):
        self.id = mindflow_model_id

        if mind_flow_model := MindFlowModel.load(mindflow_model_id):
            for key, value in mind_flow_model.__dict__.items():
                setattr(self, key, value)

        if (
            model_id := getattr(
                MindFlowModelConfig.load(f"{mindflow_model_id}_config"), "model", None
            )
        ) is None:
            model_id = self.get_default_model_id(mindflow_model_id, configured_services)

        if model_id in [ModelID.GPT_3_5_TURBO.value, ModelID.GPT_4.value]:
            self.model = cast(T, ConfiguredOpenAIChatCompletionModel(model_id))
        elif model_id in [ModelID.CLAUDE_INSTANT_V1.value, ModelID.CLAUDE_V1.value]:
            self.model = cast(T, ConfiguredAnthropicChatCompletionModel(model_id))
        elif model_id == ModelID.TEXT_EMBEDDING_ADA_002.value:
            self.model = cast(T, ConfiguredOpenAITextEmbeddingModel(model_id))
        else:
            raise Exception("Unsupported model: " + model_id)

    def get_default_model_id(
        self, mindflow_model_id: str, configured_services: ConfiguredServices
    ) -> str:
        services = {
            ServiceID.OPENAI.value: configured_services.openai,
            ServiceID.ANTHROPIC.value: configured_services.anthropic,
        }

        for service_id, service in services.items():
            if hasattr(service, ServiceConfigParameterKey.API_KEY.value):
                model_id = self.defaults.get(service_id)
                if model_id is not None:
                    return model_id
                else:
                    raise Exception(
                        "No default model configured for mindflow model: "
                        + mindflow_model_id
                        + " and service: "
                        + service.id
                    )

        print(
            "No service API key configured. Please configure an API key for at least one service."
        )
        sys.exit(1)


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
