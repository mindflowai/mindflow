import sys
import logging

from typing import List
from mindflow.cli.run import cli
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


command, arguments, database, path = cli()

db_config = DBConfig(database, path)

class ConfiguredService:
    openai = Service(
        retrieve_object(ServiceID.OPENAI.value, db_config.service), db_config.service_config
    )

configured_service = ConfiguredService()

def retrieve_model_or_default(
    mindflow_model_key: str,
) -> dict:
    match command:
        case Command.CONFIG.value:
            return {}

    configured_mindflow_model = retrieve_object(
        mindflow_model_key, db_config.mindflow_model_config
    )
    if isinstance(configured_mindflow_model, str):
        configured_model = retrieve_object(
            configured_mindflow_model, db_config.model
        )

        if isinstance(configured_model, dict):
            return configured_model
        print("Configured model not found. Using default model.")
        sys.exit(1)
    
    if hasattr(configured_service.openai, "api_key"):
        match mindflow_model_key:
            case MindFlowModelID.QUERY.value:
                return retrieve_object(
                    ModelID.TEXT_DAVINCI_003.value,
                    db_config.model,
                )
            case MindFlowModelID.INDEX.value:
                return retrieve_object(
                    ModelID.TEXT_CURIE_001.value, db_config.model
                )
            case MindFlowModelID.EMBEDDING.value:
                return retrieve_object(
                    ModelID.TEXT_EMBEDDING_ADA_002.value, db_config.model
                )
            case _:
                raise ValueError(
                    "Unable to locate model. Please raise an issue on GitHub"
                )
    print("API Key not found. Please configure API Key.")
    sys.exit(1)

class ConfiguredModel:
    index: Model = Model(retrieve_model_or_default(MindFlowModelID.INDEX.value), db_config.model_config)
    query: Model = Model(retrieve_model_or_default(MindFlowModelID.QUERY.value), db_config.model_config)
    embedding: Model = Model(retrieve_model_or_default(MindFlowModelID.EMBEDDING.value), db_config.model_config)

def index_document(document_reference: DocumentReference) -> bool:
    if command == Command.REFRESH.value:
        if not document_reference.old_hash:
            return False
        if document_reference.old_hash == document_reference.hash and not STATE.arguments.force:
            return False
        return True

    if document_reference.old_hash is None:
        return True
    return False

class State:
    """
    State of the application
    """
    configured_model: ConfiguredModel = ConfiguredModel()
    configured_service: ConfiguredService = ConfiguredService()
    db_config: DBConfig = db_config
    arguments = Arguments(arguments)
    command = command
    logging = logging

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
            if index_document(document_reference)
        ]

STATE = State()
