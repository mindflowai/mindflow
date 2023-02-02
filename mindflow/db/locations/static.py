from typing import Union

from mindflow.db.objects.static_definition.service import ServiceStatic
from mindflow.db.objects.static_definition.model import ModelStatic
from mindflow.db.static_definition import ObjectConfig, Collection


ObjectStaticUnion = Union[ServiceStatic, ModelStatic]


def retrieve_object_static(
    object_key: str, object_config: ObjectConfig
) -> ObjectStaticUnion:
    match object_config.collection:
        case Collection.SERVICE.value:
            return getattr(ServiceStatic, object_key.upper())
        case Collection.MODEL.value:
            return getattr(ModelStatic, object_key.upper())
        case _:
            raise ValueError(f"Unknown object collection: {object_config.collection}")
