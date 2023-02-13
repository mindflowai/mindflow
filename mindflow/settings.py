import sys

from mindflow.db.db import DATABASE
from mindflow.db.static_definition import Collection

from mindflow.db.objects.model import Model
from mindflow.db.objects.service import Service
from mindflow.db.objects.static_definition.mind_flow_model import (
    MindFlowModelID,
)
from mindflow.db.objects.static_definition.model import ModelID
from mindflow.db.objects.static_definition.service import ServiceID
from mindflow.input import Command


class ConfiguredService:
    openai: Service

    @classmethod
    def initialize(cls, service_config: dict):
        obj = cls()
        obj.openai = Service.initialize(
            DATABASE.static.retrieve_object(
                Collection.SERVICE.value, ServiceID.OPENAI.value
            ),
            service_config.get(ServiceID.OPENAI.value, None),
        )
        return obj


class ConfiguredModel:
    index: Model
    query: Model
    embedding: Model

    @classmethod
    def initialize(
        cls,
        command,
        configured_service: ConfiguredService,
        model_config: dict,
        mindflow_model_config: dict,
    ):
        obj = cls()
        obj.index = retrieve_model_or_default(
            command,
            MindFlowModelID.INDEX.value,
            configured_service,
            model_config,
            mindflow_model_config,
        )
        obj.query = retrieve_model_or_default(
            command,
            MindFlowModelID.QUERY.value,
            configured_service,
            model_config,
            mindflow_model_config,
        )
        obj.embedding = retrieve_model_or_default(
            command,
            MindFlowModelID.EMBEDDING.value,
            configured_service,
            model_config,
            mindflow_model_config,
        )
        return obj


def retrieve_model_or_default(
    command,
    mindflow_model_key: str,
    configured_service: ConfiguredService,
    model_config: dict,
    mindflow_model_config: dict,
) -> Model:
    match command:
        case Command.CONFIG.value:
            return Model()

    configured_mindflow_model = mindflow_model_config.get(mindflow_model_key, None)
    if isinstance(configured_mindflow_model, str):
        model = DATABASE.static.retrieve_object(
            Collection.MODEL.value, configured_mindflow_model
        )

        if isinstance(model, dict):
            return Model.initialize(
                model, model_config.get(configured_mindflow_model, None)
            )
        print("Configured model not found. Using default model.")
        sys.exit(1)

    if hasattr(configured_service.openai, "api_key"):
        match mindflow_model_key:
            case MindFlowModelID.QUERY.value:
                model = DATABASE.static.retrieve_object(
                    Collection.MODEL.value,
                    ModelID.TEXT_DAVINCI_003.value,
                )
                config = model_config.get(ModelID.TEXT_DAVINCI_003.value, None)
            case MindFlowModelID.INDEX.value:
                model = DATABASE.static.retrieve_object(
                    Collection.MODEL.value, ModelID.TEXT_CURIE_001.value
                )
                config = model_config.get(ModelID.TEXT_CURIE_001.value, None)
            case MindFlowModelID.EMBEDDING.value:
                model = DATABASE.static.retrieve_object(
                    Collection.MODEL.value, ModelID.TEXT_EMBEDDING_ADA_002.value
                )
                config = model_config.get(ModelID.TEXT_EMBEDDING_ADA_002.value, None)
            case _:
                raise ValueError(
                    "Unable to locate model. Please raise an issue on GitHub"
                )
        if isinstance(model, dict):
            return Model.initialize(model, config)
        print("Default model not found. Please raise an issue on GitHub.")
        sys.exit(1)
    print("API Key not found. Please configure API Key.")
    sys.exit(1)


class Settings:
    services: ConfiguredService
    models: ConfiguredModel

    @classmethod
    def initialize(cls, command: str, user_configurations: dict):
        obj = cls()

        service_config = user_configurations.get("service_config", {})
        model_config = user_configurations.get("model_config", {})
        mindflow_model_config = user_configurations.get("mindflow_model_config", {})

        obj.services = ConfiguredService.initialize(service_config)
        obj.models = ConfiguredModel.initialize(
            command, obj.services, model_config, mindflow_model_config
        )

        return obj
