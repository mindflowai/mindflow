from enum import Enum


class Store(Enum):
    STATIC = "static"
    JSON = "json"
    PINECONE = "pinecone"


class Collection(Enum):
    SERVICE = "Service"
    MODEL = "Model"
    MIND_FLOW_MODEL = "MindFlowModel"
    CONFIGURATIONS = "Configurations"
    DOCUMENT = "Document"
    DOCUMENT_CHUNK = "DocumentChunk"
    CONVERSATION = "Conversation"
