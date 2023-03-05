from mindflow.db.objects.service import Service, ServiceConfig
from mindflow.db.objects.model import Model, ModelConfig
from mindflow.db.objects.mindflow_model import MindFlowModel, MindFlowModelConfig
from mindflow.db.objects.document import Document

DEFAULT_OBJECT_STORE: dict = {
    Service: Store.STATIC.value,
    ServiceConfig: Store.JSON,
    Model: Store.STATIC,
    ModelConfig: Store.JSON,
    MindFlowModel: Store.STATIC,
    MindFlowModelConfig: Store.JSON,
    Document: Store.JSON
}
