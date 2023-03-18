from typing import List
from typing import Optional
from typing import Union

from mindflow.db.db.database import Collection, Database


class BaseObject:
    id: str

    _collection: Collection
    _database: Database

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
        object_dict: Optional[dict] = self._database.load(self._collection.value, id)
        if object_dict is None:
            return None

        return self(object_dict)

    @classmethod
    def load_bulk(cls, ids: list) -> List:
        object_dict: List[Optional[dict]] = cls._database.load_bulk(
            cls._collection.value, ids
        )
        return [cls(object) if object is not None else None for object in object_dict]

    @classmethod
    def delete_bulk(cls, ids: list):
        cls._database.delete_bulk(cls._collection.value, ids)

    def delete(self):
        self._database.delete(self._collection.value, self.id)

    def save(self):
        self._database.save(self._collection.value, self.todict(self))

    @staticmethod
    def save_bulk(objects: List["BaseObject"]):
        object = objects[0]
        object._database.save_bulk(
            object._collection.value, [object.todict(object) for object in objects]
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
