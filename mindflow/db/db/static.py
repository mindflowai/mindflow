from typing import Union
from mindflow.db.objects.static_definition.mind_flow_model import MINDFLOW_MODEL_STATIC

from mindflow.db.objects.static_definition.service import SERVICE_STATIC
from mindflow.db.objects.static_definition.model import MODEL_STATIC

from mindflow.db.db.database import Database, Collection


class Static(Database):
    @staticmethod
    def load(collection: str, object_key: str):
        match collection:
            case Collection.SERVICE.value:
                return SERVICE_STATIC[object_key]
            case Collection.MODEL.value:
                return MODEL_STATIC[object_key]
            case Collection.MIND_FLOW_MODEL.value:
                return MINDFLOW_MODEL_STATIC[object_key]
            case _:
                raise ValueError(f"Unknown object collection: {collection}")
