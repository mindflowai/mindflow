from typing import List
from typing import Optional
from typing import Union

from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.db.database import Collection


class StaticObject:
    id: str

    _collection: Optional[Collection] = None

    def __init__(self, id: Union[str, dict]):
        if isinstance(id, dict):
            if not "id" in id:
                raise ValueError("id is required")
            for key, value in id.items():
                setattr(self, key, value)
        else:
            self.id = id

    @classmethod
    def load(cls, id: str):
        if cls._collection is None:
            raise ValueError("Collection is not defined")

        object_dict: dict = DATABASE_CONTROLLER.databases.static.load(
            cls._collection.value, id
        )
        if object_dict is None:
            return None
        return cls(object_dict)


class BaseObject:
    id: str

    _collection: Optional[Collection] = None

    def __init__(self, id: Union[str, dict]):
        if isinstance(id, dict):
            if not "id" in id:
                raise ValueError("id is required")
            for key, value in id.items():
                setattr(self, key, value)
        else:
            self.id = id

    @classmethod
    def load(self, id: str):
        if self._collection is None:
            raise ValueError("Collection is not defined")

        object_dict: Optional[dict] = DATABASE_CONTROLLER.databases.json.load(
            self._collection.value, id
        )
        if object_dict is None:
            return None
        return self(object_dict)

    @classmethod
    def load_bulk(cls, ids: list) -> List:
        if cls._collection is None:
            raise ValueError("Collection is not defined")

        object_dict: Optional[
            List[dict]
        ] = DATABASE_CONTROLLER.databases.json.load_bulk(cls._collection.value, ids)
        if object_dict is None:
            return []
        return [cls(object) for object in object_dict if object is not None]

    @classmethod
    def delete_bulk(cls, ids: list):
        if cls._collection is None:
            raise ValueError("Collection is not defined")

        DATABASE_CONTROLLER.databases.json.delete_bulk(cls._collection.value, ids)

    def delete(self):
        DATABASE_CONTROLLER.databases.json.delete(self._collection.value, self.id)

    def save(self):
        DATABASE_CONTROLLER.databases.json.save(
            self._collection.value, self.todict(self)
        )

    def todict(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for k, v in obj.items():
                data[k] = self.todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.todict(obj._ast(), classkey)
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [self.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict(
                [
                    (key, self.todict(value, classkey))
                    for key, value in obj.__dict__.items()
                    if not callable(value) and not key.startswith("_")
                ]
            )
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj
