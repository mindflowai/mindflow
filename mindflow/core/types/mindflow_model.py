from functools import cached_property
import sys
from typing import Dict
from mindflow.core.types.definitions.model import ModelID
from mindflow.core.types.store_traits.static import StaticStore
from mindflow.core.types.store_traits.json import JsonStore

from mindflow.core.types.model import (
    ConfiguredEmbeddingModel,
    ConfiguredOpenAIChatCompletionModel,
    ConfiguredAnthropicChatCompletionModel,
    ConfiguredOpenAITextEmbeddingModel,
    ConfiguredTextCompletionModel,
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


class ConfiguredMindFlowModels:
    def __init__(self, configured_services: ConfiguredServices):
        self._configured_services = configured_services

    @cached_property
    def index(self) -> ConfiguredTextCompletionModel:
        if (
            model_id := getattr(
                MindFlowModelConfig.load(f"{MindFlowModelID.INDEX.value}_config"),
                "model",
                None,
            )
        ) is None:
            mindflow_model = MindFlowModel.load(MindFlowModelID.INDEX.value)
            model_id = self.get_default_model_id(
                MindFlowModelID.INDEX.value, mindflow_model.defaults
            )

        if model_id in [ModelID.GPT_3_5_TURBO.value, ModelID.GPT_4.value]:
            return ConfiguredOpenAIChatCompletionModel(model_id)
        elif model_id in [ModelID.CLAUDE_INSTANT_V1.value, ModelID.CLAUDE_V1.value]:
            return ConfiguredAnthropicChatCompletionModel(model_id)
        raise Exception("Unsupported model: " + model_id)

    @cached_property
    def query(self) -> ConfiguredTextCompletionModel:
        if (
            model_id := getattr(
                MindFlowModelConfig.load(f"{MindFlowModelID.QUERY.value}_config"),
                "model",
                None,
            )
        ) is None:
            mindflow_model = MindFlowModel.load(MindFlowModelID.QUERY.value)
            model_id = self.get_default_model_id(
                MindFlowModelID.QUERY.value, mindflow_model.defaults
            )

        if model_id in [ModelID.GPT_3_5_TURBO.value, ModelID.GPT_4.value]:
            return ConfiguredOpenAIChatCompletionModel(model_id)
        elif model_id in [ModelID.CLAUDE_INSTANT_V1.value, ModelID.CLAUDE_V1.value]:
            return ConfiguredAnthropicChatCompletionModel(model_id)
        raise Exception("Unsupported model: " + model_id)

    @cached_property
    def embedding(self) -> ConfiguredEmbeddingModel:
        if (
            model_id := getattr(
                MindFlowModelConfig.load(f"{MindFlowModelID.EMBEDDING.value}_config"),
                "model",
                None,
            )
        ) is None:
            mindflow_model = MindFlowModel.load(MindFlowModelID.EMBEDDING.value)
            model_id = self.get_default_model_id(
                MindFlowModelID.EMBEDDING.value, mindflow_model.defaults
            )

        if model_id == ModelID.TEXT_EMBEDDING_ADA_002.value:
            return ConfiguredOpenAITextEmbeddingModel(model_id)
        raise Exception("Unsupported model: " + model_id)

    def get_default_model_id(
        self, mindflow_model_id: str, defaults: Dict[str, str]
    ) -> str:
        services = {
            ServiceID.OPENAI.value: self._configured_services.openai,
            ServiceID.ANTHROPIC.value: self._configured_services.anthropic,
        }

        for service_id, service in services.items():
            if hasattr(service, ServiceConfigParameterKey.API_KEY.value):
                model_id = defaults.get(service_id)
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
