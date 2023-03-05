from typing import Union
from mindflow.db.objects.static_definition.mind_flow_model import MindFlowModelStatic

from mindflow.db.objects.static_definition.service import ServiceStatic
from mindflow.db.objects.static_definition.model import ModelStatic

from mindflow.db.db.database import Database, Collection

ObjectStaticUnion = Union[ServiceStatic, ModelStatic, MindFlowModelStatic]

class Static(Database):
    @staticmethod
    def load(collection: str, object_key: str):
        match collection:
            case Collection.SERVICE.value:
                return getattr(ServiceStatic, object_key.upper()).value
            case Collection.MODEL.value:
                return getattr(ModelStatic, object_key.upper()).value
            case Collection.MIND_FLOW_MODEL.value:
                return getattr(MindFlowModelStatic, object_key.upper()).value
            case _:
                raise ValueError(f"Unknown object collection: {collection}")
