from mindflow.db.db.database import Collection, Database
from mindflow.db.objects.static_definition.mind_flow_model import MINDFLOW_MODEL_STATIC
from mindflow.db.objects.static_definition.model import MODEL_STATIC
from mindflow.db.objects.static_definition.service import SERVICE_STATIC


class Static(Database):
    @staticmethod
    def load(collection: str, object_key: str):
        if collection == Collection.SERVICE.value:
            return SERVICE_STATIC[object_key]
        elif collection == Collection.MODEL.value:
            return MODEL_STATIC[object_key]
        elif collection == Collection.MIND_FLOW_MODEL.value:
            return MINDFLOW_MODEL_STATIC[object_key]
        else:
            raise ValueError(f"Unknown object collection: {collection}")
