from typing import Union

from mindflow.db.objects.static_definition.service import ServiceStatic
from mindflow.db.objects.static_definition.model import ModelStatic
from mindflow.db.static_definition import Collection

ObjectStaticUnion = Union[ServiceStatic, ModelStatic]


class Static:
    @staticmethod
    def retrieve_object(collection: str, object_key: str):
        match collection:
            case Collection.SERVICE.value:
                return getattr(ServiceStatic, object_key.upper()).value
            case Collection.MODEL.value:
                return getattr(ModelStatic, object_key.upper()).value
            case _:
                raise ValueError(f"Unknown object collection: {collection}")
