from mindflow.utils.enum import ExtendedEnum


class Store(ExtendedEnum):
    STATIC = "static"
    JSON = "json"
    PINECONE = "pinecone"


class Collection(ExtendedEnum):
    SERVICE = "Service"
    MODEL = "Model"
    MIND_FLOW_MODEL = "MindFlowModel"
    CONFIGURATIONS = "Configurations"
    DOCUMENT = "Document"
    DOCUMENT_CHUNK = "DocumentChunk"
    CONVERSATION = "Conversation"
