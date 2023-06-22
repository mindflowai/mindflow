from enum import Enum

from mindflow.core.types.document import Document
from mindflow.core.types.mindflow_model import MindFlowModel, MindFlowModelConfig
from mindflow.core.types.model import Model, ModelConfig
from mindflow.core.types.service import Service, ServiceConfig


class ObjectID(Enum):
    SERVICE = "service"
    SERVICE_CONFIG = "service_config"
    MODEL = "model"
    MODEL_CONFIG = "model_config"
    MINDFLOW_MODEL_CONFIG = "mindflow_model_config"
    DOCUMENT = "document"


class ObjectName(Enum):
    SERVICE = "Service"
    SERVICE_CONFIG = "Service Configurations"
    MODEL = "Model"
    MODEL_CONFIG = "Model Configurations"
    MINDFLOW_MODEL_CONFIG = "Mindflow Model Configurations"
    DOCUMENT = "Document"


class ObjectType(Enum):
    SERVICE = Service
    SERVICE_CONFIG = ServiceConfig
    MODEL = Model
    MODEL_CONFIG = ModelConfig
    MINDFLOW_MODEL = MindFlowModel
    MINDFLOW_MODEL_CONFIG = MindFlowModelConfig
    DOCUMENT = Document


# OBJECT_UNION = Union[Service, ServiceConfig, Model, ModelConfig, MindFlowModelConfig, Document]
