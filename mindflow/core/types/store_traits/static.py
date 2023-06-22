from typing import Type, TypeVar, Union
from mindflow.core.types import Collection
from mindflow.core.types.definitions.mind_flow_model import (
    MINDFLOW_MODEL_STATIC,
)
from mindflow.core.types.definitions.model import MODEL_STATIC
from mindflow.core.types.definitions.service import SERVICE_STATIC

T = TypeVar("T", bound="StaticStore")


class StaticStore:
    def __init__(self, id: Union[str, dict]):
        if isinstance(id, dict):
            if not "id" in id:
                raise ValueError("id is required")
            for key, value in id.items():
                setattr(self, key, value)
        else:
            self.id = id

    @classmethod
    def load(cls: Type[T], object_key: str) -> T:
        if cls.__name__ == Collection.SERVICE.value:
            return cls(SERVICE_STATIC[object_key])
        elif cls.__name__ == Collection.MODEL.value:
            return cls(MODEL_STATIC[object_key])
        elif cls.__name__ == Collection.MIND_FLOW_MODEL.value:
            return cls(MINDFLOW_MODEL_STATIC[object_key])
        else:
            raise ValueError(f"Unknown object collection: {cls.__name__}")
