from mindflow.db.objects.document import Document
from mindflow.db.objects.mindflow_model import MindFlowModel
from mindflow.db.objects.mindflow_model import MindFlowModelConfig
from mindflow.db.objects.model import Model
from mindflow.db.objects.model import ModelConfig
from mindflow.db.objects.service import Service
from mindflow.db.objects.service import ServiceConfig
from mindflow.utils.enum import ExtendedEnum


class ObjectID(ExtendedEnum):
    SERVICE = "service"
    SERVICE_CONFIG = "service_config"
    MODEL = "model"
    MODEL_CONFIG = "model_config"
    MINDFLOW_MODEL_CONFIG = "mindflow_model_config"
    DOCUMENT = "document"


class ObjectName(ExtendedEnum):
    SERVICE = "Service"
    SERVICE_CONFIG = "Service Configurations"
    MODEL = "Model"
    MODEL_CONFIG = "Model Configurations"
    MINDFLOW_MODEL_CONFIG = "Mindflow Model Configurations"
    DOCUMENT = "Document"


class ObjectType(ExtendedEnum):
    SERVICE = Service
    SERVICE_CONFIG = ServiceConfig
    MODEL = Model
    MODEL_CONFIG = ModelConfig
    MINDFLOW_MODEL = MindFlowModel
    MINDFLOW_MODEL_CONFIG = MindFlowModelConfig
    DOCUMENT = Document


# OBJECT_UNION = Union[Service, ServiceConfig, Model, ModelConfig, MindFlowModelConfig, Document]
