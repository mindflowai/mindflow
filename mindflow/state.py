import sys

from typing import List, Optional
from mindflow.db.db import retrieve_object
from mindflow.db.objects.document import DocumentReference
from mindflow.db.objects.model import Model
from mindflow.db.objects.service import Service
from mindflow.db.objects.static_definition.mind_flow_model import (
    MindFlowModelID,
)
from mindflow.db.objects.static_definition.model import ModelID
from mindflow.db.objects.static_definition.service import ServiceID
from mindflow.resolving.resolve import resolve
from mindflow.input import Arguments, Command, DBConfig


class ConfiguredService:
    def __init__(self, db_config: DBConfig):
        self.openai = Service(
            retrieve_object(ServiceID.OPENAI.value, db_config.service),
            db_config.service_config,
        )


class ConfiguredModel:
    def __init__(
        self, command: str, configured_service: ConfiguredService, db_config: DBConfig
    ):
        self.index: Model = Model(
            retrieve_model_or_default(
                command, MindFlowModelID.INDEX.value, configured_service, db_config
            ),
            db_config.model_config,
        )
        self.query: Model = Model(
            retrieve_model_or_default(
                command, MindFlowModelID.QUERY.value, configured_service, db_config
            ),
            db_config.model_config,
        )
        self.embedding: Model = Model(
            retrieve_model_or_default(
                command, MindFlowModelID.EMBEDDING.value, configured_service, db_config
            ),
            db_config.model_config,
        )


def retrieve_model_or_default(
    command,
    mindflow_model_key: str,
    configured_service: ConfiguredService,
    db_config: DBConfig,
) -> dict:
    match command:
        case Command.CONFIG.value:
            return {}

    configured_mindflow_model = retrieve_object(
        mindflow_model_key, db_config.mindflow_model_config
    )
    if isinstance(configured_mindflow_model, str):
        configured_model = retrieve_object(configured_mindflow_model, db_config.model)

        if isinstance(configured_model, dict):
            return configured_model
        print("Configured model not found. Using default model.")
        sys.exit(1)

    if hasattr(configured_service.openai, "api_key"):
        match mindflow_model_key:
            case MindFlowModelID.QUERY.value:
                model = retrieve_object(
                    ModelID.TEXT_DAVINCI_003.value,
                    db_config.model,
                )
            case MindFlowModelID.INDEX.value:
                model = retrieve_object(ModelID.TEXT_CURIE_001.value, db_config.model)
            case MindFlowModelID.EMBEDDING.value:
                model = retrieve_object(
                    ModelID.TEXT_EMBEDDING_ADA_002.value, db_config.model
                )
            case _:
                raise ValueError(
                    "Unable to locate model. Please raise an issue on GitHub"
                )
        if isinstance(model, dict):
            return model
        print("Default model not found. Please raise an issue on GitHub.")
        sys.exit(1)
    print("API Key not found. Please configure API Key.")
    sys.exit(1)


def index_document(
    command: str, document_reference: DocumentReference, force: Optional[bool]
) -> bool:
    if command == Command.REFRESH.value:
        if not document_reference.old_hash:
            return False
        if document_reference.old_hash == document_reference.hash and not force:
            return False
        return True

    if document_reference.old_hash is None:
        return True
    return False


class State:
    """
    State of the application
    """

    configured_model: ConfiguredModel
    configured_service: ConfiguredService
    db_config: DBConfig
    arguments: Arguments
    command: str

    @property
    def document_references(self) -> List[DocumentReference]:
        document_references: List[DocumentReference] = []
        for document_path in self.arguments.document_paths:
            document_references.extend(resolve(document_path, self.db_config.document))
        return document_references

    @property
    def indexable_document_references(self) -> List[DocumentReference]:
        return [
            document_reference
            for document_reference in self.document_references
            if index_document(self.command, document_reference, self.arguments.force)
        ]


STATE = State()
