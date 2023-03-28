from typing import Union
from mindflow.db.objects.base import BaseObject


def set_object_params(self, params: dict):
    for key, value in params.items():
        setattr(self, key, value)
    return self


def getOrCreateObject(objectType: BaseObject, params: Union[dict, str]):
    if isinstance(params, str):
        params = {"id": params}

    id = params.get("id", None)
    if id is None:
        raise Exception("ID is required")

    obj: BaseObject = objectType.load(id)
    if obj is None:
        obj = objectType(params)

    return obj
