from mindflow.utils.enum import ExtendedEnum


class ObjectStoreType(ExtendedEnum):
    STATIC = "static"
    JSON = "json"
    NEO4J = "neo4j"


class Collection(ExtendedEnum):
    SERVICE = "service"
    MODEL = "model"
    DOCUMENT = "document"
    CONFIGURATIONS = "configurations"


class ObjectName(ExtendedEnum):
    SERVICE = "Service"
    SERVICE_CONFIG = "Service Configurations"
    MODEL = "Model"
    MODEL_CONFIG = "Model Configurations"
    MINDFLOW_MODEL_CONFIG = "Mindflow Model Configurations"
    DOCUMENT = "Document"
